import hashlib
import os
import secrets
import shutil
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Optional

from embedded_assets import ensure_assets

from fastapi import Depends, FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from itsdangerous import BadSignature, URLSafeSerializer
from passlib.context import CryptContext
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Text, create_engine, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, sessionmaker

BASE_DIR = Path(__file__).resolve().parent
ensure_assets(BASE_DIR)
APP_NAME = os.getenv("APP_NAME", "JustifAbs AIBD SA")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-key-change-me")
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'data' / 'aibd_absences.db'}")
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", str(BASE_DIR / "data" / "uploads")))
MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "10"))
ALLOWED_EXTENSIONS = {x.strip().lower() for x in os.getenv("ALLOWED_EXTENSIONS", "pdf,jpg,jpeg,png,doc,docx").split(",")}
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").lower() == "true"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
if DATABASE_URL.startswith("sqlite:///"):
    sqlite_path = DATABASE_URL.removeprefix("sqlite:///")
    if sqlite_path and sqlite_path != ":memory:":
        Path(sqlite_path).expanduser().resolve().parent.mkdir(parents=True, exist_ok=True)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
serializer = URLSafeSerializer(SECRET_KEY, salt="aibd-session")


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    matricule: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(180), unique=True, index=True)
    department: Mapped[str] = mapped_column(String(150), default="")
    site: Mapped[str] = mapped_column(String(100), default="DIASS")
    role: Mapped[str] = mapped_column(String(20), default="agent")  # agent, manager, rh, admin
    password_hash: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    absences: Mapped[list["Absence"]] = relationship(back_populates="agent", foreign_keys="Absence.agent_id")


class Absence(Base):
    __tablename__ = "absences"
    id: Mapped[int] = mapped_column(primary_key=True)
    agent_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    absence_type: Mapped[str] = mapped_column(String(80))
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)
    reason: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(30), default="soumis", index=True)
    submitted_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    validated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    validated_by: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    decision_note: Mapped[str] = mapped_column(Text, default="")
    agent: Mapped[User] = relationship(back_populates="absences", foreign_keys=[agent_id])
    documents: Mapped[list["Document"]] = relationship(back_populates="absence", cascade="all, delete-orphan")
    messages: Mapped[list["Message"]] = relationship(back_populates="absence", cascade="all, delete-orphan", order_by="Message.created_at")
    events: Mapped[list["AuditEvent"]] = relationship(back_populates="absence", cascade="all, delete-orphan", order_by="AuditEvent.created_at")


class Document(Base):
    __tablename__ = "documents"
    id: Mapped[int] = mapped_column(primary_key=True)
    absence_id: Mapped[int] = mapped_column(ForeignKey("absences.id"), index=True)
    original_name: Mapped[str] = mapped_column(String(255))
    stored_name: Mapped[str] = mapped_column(String(255), unique=True)
    content_type: Mapped[str] = mapped_column(String(120), default="application/octet-stream")
    size_bytes: Mapped[int] = mapped_column(Integer)
    sha256: Mapped[str] = mapped_column(String(64))
    uploaded_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    absence: Mapped[Absence] = relationship(back_populates="documents")


class Message(Base):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(primary_key=True)
    absence_id: Mapped[int] = mapped_column(ForeignKey("absences.id"), index=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    body: Mapped[str] = mapped_column(Text)
    kind: Mapped[str] = mapped_column(String(30), default="commentaire")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    absence: Mapped[Absence] = relationship(back_populates="messages")
    author: Mapped[User] = relationship()


class AuditEvent(Base):
    __tablename__ = "audit_events"
    id: Mapped[int] = mapped_column(primary_key=True)
    absence_id: Mapped[int] = mapped_column(ForeignKey("absences.id"), index=True)
    actor_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    action: Mapped[str] = mapped_column(String(80))
    details: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    absence: Mapped[Absence] = relationship(back_populates="events")
    actor: Mapped[User] = relationship()


Base.metadata.create_all(engine)

app = FastAPI(title=APP_NAME)
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR.mkdir(parents=True, exist_ok=True)
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def current_user(request: Request, db: Session = Depends(db_session)) -> User:
    token = request.cookies.get("session")
    if not token:
        raise HTTPException(status_code=401)
    try:
        data = serializer.loads(token)
        user = db.get(User, int(data["uid"]))
    except (BadSignature, KeyError, TypeError, ValueError):
        raise HTTPException(status_code=401)
    if not user or not user.is_active:
        raise HTTPException(status_code=401)
    return user


def optional_user(request: Request, db: Session) -> Optional[User]:
    token = request.cookies.get("session")
    if not token:
        return None
    try:
        uid = int(serializer.loads(token)["uid"])
    except Exception:
        return None
    return db.get(User, uid)


def flash_redirect(url: str, message: str, level: str = "success"):
    return RedirectResponse(f"{url}?msg={message}&level={level}", status_code=303)


def can_access(user: User, absence: Absence) -> bool:
    return user.role in {"rh", "admin"} or absence.agent_id == user.id


def add_event(db: Session, absence: Absence, actor: User, action: str, details: str = ""):
    db.add(AuditEvent(absence_id=absence.id, actor_id=actor.id, action=action, details=details))


def save_upload(db: Session, absence: Absence, user: User, upload: UploadFile):
    original = Path(upload.filename or "document").name
    ext = original.rsplit(".", 1)[-1].lower() if "." in original else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"Type de fichier non autorisé: .{ext}")
    data = upload.file.read(MAX_UPLOAD_MB * 1024 * 1024 + 1)
    if len(data) > MAX_UPLOAD_MB * 1024 * 1024:
        raise HTTPException(400, f"Fichier supérieur à {MAX_UPLOAD_MB} Mo")
    digest = hashlib.sha256(data).hexdigest()
    stored = f"{absence.id}_{secrets.token_hex(12)}.{ext}"
    (UPLOAD_DIR / stored).write_bytes(data)
    db.add(Document(absence_id=absence.id, original_name=original, stored_name=stored,
                    content_type=upload.content_type or "application/octet-stream",
                    size_bytes=len(data), sha256=digest, uploaded_by=user.id))


def bootstrap_admin():
    """Crée le premier administrateur uniquement via les variables Render."""
    email = os.getenv("BOOTSTRAP_ADMIN_EMAIL", "").strip().lower()
    password = os.getenv("BOOTSTRAP_ADMIN_PASSWORD", "")
    if not email or not password:
        return
    if len(password) < 12:
        raise RuntimeError("BOOTSTRAP_ADMIN_PASSWORD doit contenir au moins 12 caractères")
    with SessionLocal() as db:
        if db.scalar(select(func.count(User.id))) > 0:
            return
        db.add(User(
            matricule=os.getenv("BOOTSTRAP_ADMIN_MATRICULE", "ADMIN001").strip(),
            full_name=os.getenv("BOOTSTRAP_ADMIN_NAME", "Administrateur AIBD SA").strip(),
            email=email,
            department="Administration",
            site="DIASS",
            role="admin",
            password_hash=pwd_context.hash(password),
        ))
        db.commit()


bootstrap_admin()


@app.exception_handler(401)
async def unauthorized(request: Request, exc):
    return RedirectResponse("/login", status_code=303)


@app.get("/health")
def health():
    return {"status": "ok", "application": APP_NAME}


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request, db: Session = Depends(db_session)):
    if optional_user(request, db):
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse("login.html", {"request": request, "app_name": APP_NAME})


@app.post("/login")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(db_session)):
    user = db.scalar(select(User).where(User.email == email.strip().lower()))
    if not user or not pwd_context.verify(password, user.password_hash):
        return flash_redirect("/login", "Identifiants incorrects", "danger")
    response = RedirectResponse("/", status_code=303)
    response.set_cookie("session", serializer.dumps({"uid": user.id}), httponly=True, secure=COOKIE_SECURE, samesite="lax", max_age=8 * 3600)
    return response


@app.get("/logout")
def logout():
    response = RedirectResponse("/login", status_code=303)
    response.delete_cookie("session")
    return response


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request, user: User = Depends(current_user), db: Session = Depends(db_session)):
    if user.role in {"rh", "admin"}:
        absences = db.scalars(select(Absence).order_by(Absence.submitted_at.desc()).limit(100)).all()
    else:
        absences = db.scalars(select(Absence).where(Absence.agent_id == user.id).order_by(Absence.submitted_at.desc())).all()
    counts = {s: sum(1 for a in absences if a.status == s) for s in ["soumis", "complement_requis", "en_cours", "valide", "rejete"]}
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user, "absences": absences, "counts": counts, "app_name": APP_NAME})


@app.get("/absences/nouvelle", response_class=HTMLResponse)
def new_absence_page(request: Request, user: User = Depends(current_user)):
    return templates.TemplateResponse("new_absence.html", {"request": request, "user": user, "app_name": APP_NAME})


@app.post("/absences/nouvelle")
def create_absence(
    absence_type: str = Form(...), start_date: date = Form(...), end_date: date = Form(...),
    reason: str = Form(""), documents: list[UploadFile] = File(default=[]),
    user: User = Depends(current_user), db: Session = Depends(db_session)
):
    if end_date < start_date:
        raise HTTPException(400, "La date de fin ne peut pas précéder la date de début")
    absence = Absence(agent_id=user.id, absence_type=absence_type, start_date=start_date, end_date=end_date, reason=reason.strip())
    db.add(absence)
    db.flush()
    for doc in documents:
        if doc.filename:
            save_upload(db, absence, user, doc)
    add_event(db, absence, user, "SOUMISSION", "Dossier d'absence soumis par l'agent")
    db.commit()
    return flash_redirect(f"/absences/{absence.id}", "Dossier soumis avec succès")


@app.get("/absences/{absence_id}", response_class=HTMLResponse)
def absence_detail(absence_id: int, request: Request, user: User = Depends(current_user), db: Session = Depends(db_session)):
    absence = db.get(Absence, absence_id)
    if not absence or not can_access(user, absence):
        raise HTTPException(404)
    return templates.TemplateResponse("detail.html", {"request": request, "user": user, "absence": absence, "app_name": APP_NAME})


@app.post("/absences/{absence_id}/documents")
def add_documents(absence_id: int, documents: list[UploadFile] = File(...), user: User = Depends(current_user), db: Session = Depends(db_session)):
    absence = db.get(Absence, absence_id)
    if not absence or not can_access(user, absence):
        raise HTTPException(404)
    if user.role == "agent" and absence.status in {"valide", "rejete"}:
        raise HTTPException(400, "Ce dossier est clôturé")
    for doc in documents:
        if doc.filename:
            save_upload(db, absence, user, doc)
    if absence.status == "complement_requis" and absence.agent_id == user.id:
        absence.status = "en_cours"
    add_event(db, absence, user, "AJOUT_DOCUMENT", f"{len([d for d in documents if d.filename])} document(s) ajouté(s)")
    db.commit()
    return flash_redirect(f"/absences/{absence_id}", "Document(s) ajouté(s)")


@app.get("/documents/{document_id}")
def download_document(document_id: int, user: User = Depends(current_user), db: Session = Depends(db_session)):
    doc = db.get(Document, document_id)
    if not doc or not can_access(user, doc.absence):
        raise HTTPException(404)
    path = UPLOAD_DIR / doc.stored_name
    if not path.exists():
        raise HTTPException(404, "Fichier introuvable")
    return FileResponse(path, media_type=doc.content_type, filename=doc.original_name)


@app.post("/absences/{absence_id}/message")
def add_message(absence_id: int, body: str = Form(...), user: User = Depends(current_user), db: Session = Depends(db_session)):
    absence = db.get(Absence, absence_id)
    if not absence or not can_access(user, absence):
        raise HTTPException(404)
    body = body.strip()
    if not body:
        raise HTTPException(400, "Message vide")
    db.add(Message(absence_id=absence.id, author_id=user.id, body=body, kind="reponse_agent" if user.id == absence.agent_id else "commentaire_rh"))
    add_event(db, absence, user, "MESSAGE", "Nouveau message dans le dossier")
    db.commit()
    return flash_redirect(f"/absences/{absence_id}", "Message envoyé")


@app.post("/absences/{absence_id}/complement")
def request_complement(absence_id: int, body: str = Form(...), user: User = Depends(current_user), db: Session = Depends(db_session)):
    if user.role not in {"rh", "admin"}:
        raise HTTPException(403)
    absence = db.get(Absence, absence_id)
    if not absence:
        raise HTTPException(404)
    absence.status = "complement_requis"
    db.add(Message(absence_id=absence.id, author_id=user.id, body=body.strip(), kind="demande_complement"))
    add_event(db, absence, user, "COMPLEMENT_REQUIS", body.strip())
    db.commit()
    return flash_redirect(f"/absences/{absence_id}", "Demande de complément envoyée")


@app.post("/absences/{absence_id}/decision")
def decision(absence_id: int, decision: str = Form(...), note: str = Form(""), user: User = Depends(current_user), db: Session = Depends(db_session)):
    if user.role not in {"rh", "admin"}:
        raise HTTPException(403)
    if decision not in {"valide", "rejete", "en_cours"}:
        raise HTTPException(400)
    absence = db.get(Absence, absence_id)
    if not absence:
        raise HTTPException(404)
    absence.status = decision
    absence.decision_note = note.strip()
    absence.validated_by = user.id
    absence.validated_at = datetime.utcnow() if decision in {"valide", "rejete"} else None
    add_event(db, absence, user, decision.upper(), note.strip())
    db.commit()
    return flash_redirect(f"/absences/{absence_id}", "Décision enregistrée")


@app.get("/admin/utilisateurs", response_class=HTMLResponse)
def users_page(request: Request, user: User = Depends(current_user), db: Session = Depends(db_session)):
    if user.role != "admin":
        raise HTTPException(403)
    users = db.scalars(select(User).order_by(User.full_name)).all()
    return templates.TemplateResponse("users.html", {"request": request, "user": user, "users": users, "app_name": APP_NAME})


@app.post("/admin/utilisateurs")
def create_user(matricule: str = Form(...), full_name: str = Form(...), email: str = Form(...), department: str = Form(""), site: str = Form("DIASS"), role: str = Form("agent"), password: str = Form(...), user: User = Depends(current_user), db: Session = Depends(db_session)):
    if user.role != "admin":
        raise HTTPException(403)
    if role not in {"agent", "manager", "rh", "admin"}:
        raise HTTPException(400)
    email = email.strip().lower()
    if db.scalar(select(User).where((User.email == email) | (User.matricule == matricule.strip()))):
        return flash_redirect("/admin/utilisateurs", "E-mail ou matricule déjà utilisé", "danger")
    db.add(User(matricule=matricule.strip(), full_name=full_name.strip(), email=email, department=department.strip(), site=site.strip(), role=role, password_hash=pwd_context.hash(password)))
    db.commit()
    return flash_redirect("/admin/utilisateurs", "Utilisateur créé")


@app.post("/admin/utilisateurs/{user_id}/etat")
def toggle_user_state(user_id: int, user: User = Depends(current_user), db: Session = Depends(db_session)):
    if user.role != "admin":
        raise HTTPException(403)
    target = db.get(User, user_id)
    if not target:
        raise HTTPException(404)
    if target.id == user.id:
        return flash_redirect("/admin/utilisateurs", "Vous ne pouvez pas désactiver votre propre compte", "danger")
    if target.role == "admin" and target.is_active:
        active_admins = db.scalar(select(func.count()).select_from(User).where(User.role == "admin", User.is_active.is_(True))) or 0
        if active_admins <= 1:
            return flash_redirect("/admin/utilisateurs", "Impossible de désactiver le dernier administrateur actif", "danger")
    target.is_active = not target.is_active
    db.commit()
    message = "Utilisateur réactivé" if target.is_active else "Utilisateur désactivé"
    return flash_redirect("/admin/utilisateurs", message)


@app.post("/admin/utilisateurs/{user_id}/supprimer")
def delete_user(user_id: int, user: User = Depends(current_user), db: Session = Depends(db_session)):
    if user.role != "admin":
        raise HTTPException(403)
    target = db.get(User, user_id)
    if not target:
        raise HTTPException(404)
    if target.id == user.id:
        return flash_redirect("/admin/utilisateurs", "Vous ne pouvez pas supprimer votre propre compte", "danger")
    if target.role == "admin":
        admin_count = db.scalar(select(func.count()).select_from(User).where(User.role == "admin")) or 0
        if admin_count <= 1:
            return flash_redirect("/admin/utilisateurs", "Impossible de supprimer le dernier administrateur", "danger")

    linked_records = sum([
        db.scalar(select(func.count()).select_from(Absence).where(Absence.agent_id == target.id)) or 0,
        db.scalar(select(func.count()).select_from(Absence).where(Absence.validated_by == target.id)) or 0,
        db.scalar(select(func.count()).select_from(Document).where(Document.uploaded_by == target.id)) or 0,
        db.scalar(select(func.count()).select_from(Message).where(Message.author_id == target.id)) or 0,
        db.scalar(select(func.count()).select_from(AuditEvent).where(AuditEvent.actor_id == target.id)) or 0,
    ])
    if linked_records:
        if target.is_active:
            target.is_active = False
            db.commit()
        return flash_redirect(
            "/admin/utilisateurs",
            "Ce compte est lié à l'historique des dossiers : il a été désactivé au lieu d'être supprimé",
            "danger",
        )

    db.delete(target)
    db.commit()
    return flash_redirect("/admin/utilisateurs", "Utilisateur supprimé définitivement")


@app.get("/rapports/export.csv")
def export_csv(user: User = Depends(current_user), db: Session = Depends(db_session)):
    if user.role not in {"rh", "admin"}:
        raise HTTPException(403)
    import csv
    from io import StringIO
    from fastapi.responses import StreamingResponse
    rows = db.scalars(select(Absence).order_by(Absence.submitted_at.desc())).all()
    output = StringIO()
    writer = csv.writer(output, delimiter=";")
    writer.writerow(["ID", "Matricule", "Agent", "Département", "Site", "Type", "Début", "Fin", "Jours", "Statut", "Soumis le"])
    for a in rows:
        writer.writerow([a.id, a.agent.matricule, a.agent.full_name, a.agent.department, a.agent.site, a.absence_type, a.start_date, a.end_date, (a.end_date-a.start_date).days+1, a.status, a.submitted_at.isoformat(timespec="minutes")])
    output.seek(0)
    return StreamingResponse(iter([output.getvalue()]), media_type="text/csv; charset=utf-8", headers={"Content-Disposition": "attachment; filename=justificatifs_absences.csv"})
