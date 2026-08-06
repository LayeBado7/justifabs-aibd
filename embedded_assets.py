"""Ressources intégrées de secours pour les déploiements où les dossiers sont omis."""
from pathlib import Path

ASSETS = {'static/style.css': ':root{--blue:#083b66;--blue2:#0b5b91;--gold:#d4a017;--bg:#f4f7fa;--text:#1d2a35;--muted:#6b7785;--border:#dce3e9;--white:#fff;--danger:#a4262c;--success:#197642}*{box-sizing:border-box}body{margin:0;font:15px/1.5 '
                     'Arial,Helvetica,sans-serif;background:var(--bg);color:var(--text)}header{background:linear-gradient(100deg,var(--blue),var(--blue2));color:#fff;min-height:74px;padding:12px '
                     '4%;display:flex;align-items:center;justify-content:space-between;gap:20px}.brand{display:flex;align-items:center;gap:12px}.mark{border:2px '
                     'solid var(--gold);padding:7px 9px;font-weight:900;letter-spacing:1px}.brand '
                     'b{font-size:20px}.brand '
                     'small{display:block;opacity:.8}nav{display:flex;gap:18px;flex-wrap:wrap}nav '
                     'a{color:#fff;text-decoration:none;font-weight:600}main{max-width:1200px;margin:0 '
                     'auto;padding:28px 20px '
                     '60px}footer{text-align:center;padding:22px;color:var(--muted);font-size:13px}.hero,.page-title{display:flex;justify-content:space-between;align-items:center;gap:20px;margin-bottom:22px}.hero '
                     'h1,.page-title h1{margin:0;font-size:28px}.hero p,.page-title p{margin:5px '
                     '0;color:var(--muted)}.button,button{display:inline-block;border:0;border-radius:7px;background:var(--blue2);color:#fff;padding:11px '
                     '16px;font-weight:700;text-decoration:none;cursor:pointer}.secondary{background:#e8edf2;color:var(--text)}.warning{background:#b36b00}.stats{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-bottom:22px}.stat{background:#fff;border:1px '
                     'solid var(--border);border-top:4px solid '
                     'var(--gold);border-radius:9px;padding:17px}.stat '
                     'span{font-size:26px;font-weight:800;display:block}.stat '
                     'small{color:var(--muted)}.panel{background:#fff;border:1px solid '
                     'var(--border);border-radius:10px;padding:22px;box-shadow:0 4px 12px '
                     'rgba(20,40,60,.04);margin-bottom:20px}.panel '
                     'h2{margin-top:0}.panel-head{display:flex;justify-content:space-between;align-items:center}.table-wrap{overflow:auto}table{width:100%;border-collapse:collapse}th,td{text-align:left;border-bottom:1px '
                     'solid var(--border);padding:13px '
                     '10px;vertical-align:top}th{font-size:12px;text-transform:uppercase;color:var(--muted)}td '
                     'small{display:block;color:var(--muted)}.badge{display:inline-block;padding:5px '
                     '9px;border-radius:20px;background:#e8edf2;font-size:12px;font-weight:800;text-transform:uppercase}.badge.big{font-size:14px;padding:9px '
                     '14px}.badge.valide{background:#dff3e8;color:#16633a}.badge.rejete{background:#f8dddd;color:#8a1f24}.badge.complement_requis{background:#fff0c7;color:#805c00}.badge.en_cours{background:#dceeff;color:#174f7b}.badge.soumis{background:#e9e3ff;color:#4a3288}.grid2,.detail-grid{display:grid;grid-template-columns:1fr '
                     '1fr;gap:18px}label{display:block;font-weight:700;margin-bottom:16px}input,select,textarea{width:100%;margin-top:6px;padding:11px '
                     '12px;border:1px solid #bdc9d4;border-radius:6px;background:#fff;font:inherit}label '
                     'small{font-weight:400;color:var(--muted)}textarea{resize:vertical}.actions{display:flex;justify-content:flex-end;gap:10px}.form-panel{max-width:850px}dl{display:grid;grid-template-columns:130px '
                     '1fr;gap:12px;margin:0}dt{font-weight:700;color:var(--muted)}dd{margin:0}.doc{display:flex;gap:12px;padding:12px;border:1px '
                     'solid '
                     'var(--border);border-radius:7px;margin-bottom:9px;color:var(--text);text-decoration:none}.doc '
                     'span{font-size:24px}.doc small,.message small,.timeline small,.user-row '
                     'small{display:block;color:var(--muted)}.upload{display:flex;gap:8px;margin-top:14px}.upload '
                     'input{margin:0}.message{border-left:4px solid '
                     'var(--blue2);background:#f7fafc;padding:12px;margin-bottom:10px;border-radius:4px}.message.demande_complement{border-left-color:#c27b00;background:#fff8e7}.message '
                     'p{margin-bottom:0}.timeline{list-style:none;padding:0}.timeline li{border-left:2px '
                     'solid var(--border);padding:0 0 16px 16px}.timeline p{margin:4px '
                     '0}.users{display:grid;gap:8px}.user-row{display:flex;justify-content:space-between;border-bottom:1px '
                     'solid var(--border);padding:10px '
                     '0}.login-wrap{min-height:70vh;display:grid;place-items:center}.login-card{width:min(430px,100%);background:#fff;padding:30px;border-radius:12px;border-top:6px '
                     'solid var(--gold);box-shadow:0 10px 35px rgba(10,45,70,.13)}.login-card '
                     'h1{margin-top:0}.demo{margin-top:20px;padding:12px;background:#f0f5f8;border-radius:7px;font-size:13px}.alert{padding:12px '
                     '15px;border-radius:7px;margin-bottom:18px;background:#dff3e8;color:#16633a}.alert.danger{background:#f8dddd;color:#8a1f24}.empty{color:var(--muted);text-align:center}hr{border:0;border-top:1px '
                     'solid var(--border);margin:22px '
                     '0}@media(max-width:800px){header,.hero,.page-title{align-items:flex-start;flex-direction:column}.stats{grid-template-columns:1fr '
                     '1fr}.grid2,.detail-grid{grid-template-columns:1fr}nav{gap:10px}.upload{flex-direction:column}dl{grid-template-columns:1fr}dt{margin-top:8px}}\n',
 'templates/base.html': '<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" '
                        'content="width=device-width,initial-scale=1"><title>{{ app_name }}</title><link '
                        'rel="stylesheet" href="/static/style.css"></head><body>\n'
                        '<header><div class="brand"><span '
                        'class="mark">AIBD</span><div><b>JustifAbs</b><small>Gestion des justificatifs '
                        'd\'absence</small></div></div>{% if user %}<nav><a href="/">Tableau de bord</a><a '
                        'href="/absences/nouvelle">Nouveau dossier</a>{% if user.role in [\'rh\',\'admin\'] '
                        '%}<a href="/rapports/export.csv">Exporter CSV</a>{% endif %}{% if '
                        'user.role==\'admin\' %}<a href="/admin/utilisateurs">Utilisateurs</a>{% endif %}<a '
                        'href="/logout">Déconnexion</a></nav>{% endif %}</header>\n'
                        '<main>{% if request.query_params.get(\'msg\') %}<div class="alert {{ '
                        'request.query_params.get(\'level\',\'success\') }}">{{ '
                        "request.query_params.get('msg') }}</div>{% endif %}{% block content %}{% endblock "
                        '%}</main>\n'
                        '<footer>AIBD SA — application interne de suivi administratif • Les pièces sont '
                        'accessibles uniquement aux personnes habilitées.</footer></body></html>\n',
 'templates/dashboard.html': "{% extends 'base.html' %}{% block content %}<div "
                             'class="hero"><div><h1>Bonjour, {{ user.full_name }}</h1><p>{{ user.department '
                             '}} • {{ user.site }} • Profil {{ user.role|upper }}</p></div><a class="button" '
                             'href="/absences/nouvelle">+ Soumettre un justificatif</a></div>\n'
                             '<div class="stats">{% for label,key in [(\'Soumis\',\'soumis\'),(\'Complément '
                             "requis','complement_requis'),('En "
                             "cours','en_cours'),('Validés','valide'),('Rejetés','rejete')] %}<div "
                             'class="stat"><span>{{ counts[key] }}</span><small>{{ label }}</small></div>{% '
                             'endfor %}</div>\n'
                             '<section class="panel"><div class="panel-head"><h2>{% if user.role in '
                             "['rh','admin'] %}Tous les dossiers{% else %}Mes dossiers{% endif "
                             '%}</h2><span>{{ absences|length }} dossier(s)</span></div><div '
                             'class="table-wrap"><table><thead><tr><th>Réf.</th>{% if user.role in '
                             "['rh','admin'] %}<th>Agent</th>{% endif "
                             '%}<th>Absence</th><th>Période</th><th>Pièces</th><th>Statut</th><th></th></tr></thead><tbody>{% '
                             "for a in absences %}<tr><td>#{{ '%05d'|format(a.id) }}</td>{% if user.role in "
                             "['rh','admin'] %}<td><b>{{ a.agent.full_name }}</b><small>{{ a.agent.matricule "
                             '}} · {{ a.agent.site }}</small></td>{% endif %}<td>{{ a.absence_type '
                             "}}</td><td>{{ a.start_date.strftime('%d/%m/%Y') }} → {{ "
                             "a.end_date.strftime('%d/%m/%Y') }}</td><td>{{ a.documents|length "
                             '}}</td><td><span class="badge {{ a.status }}">{{ a.status.replace(\'_\',\' \') '
                             '}}</span></td><td><a href="/absences/{{ a.id }}">Ouvrir</a></td></tr>{% else '
                             '%}<tr><td colspan="7" class="empty">Aucun dossier enregistré.</td></tr>{% '
                             'endfor %}</tbody></table></div></section>{% endblock %}\n',
 'templates/detail.html': '{% extends \'base.html\' %}{% block content %}<div class="hero"><div><h1>Dossier '
                          "#{{ '%05d'|format(absence.id) }}</h1><p>{{ absence.agent.full_name }} · {{ "
                          'absence.agent.matricule }} · {{ absence.agent.department }} · {{ '
                          'absence.agent.site }}</p></div><span class="badge big {{ absence.status }}">{{ '
                          "absence.status.replace('_',' ') }}</span></div>\n"
                          '<div class="detail-grid"><section '
                          'class="panel"><h2>Informations</h2><dl><dt>Type</dt><dd>{{ absence.absence_type '
                          "}}</dd><dt>Période</dt><dd>{{ absence.start_date.strftime('%d/%m/%Y') }} au {{ "
                          "absence.end_date.strftime('%d/%m/%Y') }}</dd><dt>Durée</dt><dd>{{ "
                          '(absence.end_date-absence.start_date).days+1 }} jour(s)</dd><dt>Motif</dt><dd>{{ '
                          "absence.reason or 'Non renseigné' }}</dd><dt>Soumis le</dt><dd>{{ "
                          "absence.submitted_at.strftime('%d/%m/%Y à %H:%M') }}</dd>{% if "
                          'absence.decision_note %}<dt>Note de décision</dt><dd>{{ absence.decision_note '
                          '}}</dd>{% endif %}</dl></section>\n'
                          '<section class="panel"><h2>Pièces justificatives</h2><div class="docs">{% for d '
                          'in absence.documents %}<a class="doc" href="/documents/{{ d.id '
                          '}}"><span>📄</span><div><b>{{ d.original_name }}</b><small>{{ '
                          '(d.size_bytes/1024)|round(1) }} Ko · SHA-256: {{ d.sha256[:12] '
                          '}}…</small></div></a>{% else %}<p class="empty">Aucune pièce déposée.</p>{% '
                          "endfor %}</div>{% if absence.status not in ['valide','rejete'] or user.role in "
                          '[\'rh\',\'admin\'] %}<form class="upload" method="post" action="/absences/{{ '
                          'absence.id }}/documents" enctype="multipart/form-data"><input type="file" '
                          'name="documents" multiple required><button>Ajouter</button></form>{% endif '
                          '%}</section></div>\n'
                          '<div class="detail-grid"><section class="panel"><h2>Échanges</h2><div '
                          'class="messages">{% for m in absence.messages %}<div class="message {{ m.kind '
                          '}}"><div><b>{{ m.author.full_name }}</b><small>{{ '
                          "m.created_at.strftime('%d/%m/%Y %H:%M') }} · {{ m.kind.replace('_',' ') "
                          '}}</small></div><p>{{ m.body }}</p></div>{% else %}<p class="empty">Aucun '
                          'échange.</p>{% endfor %}</div><form method="post" action="/absences/{{ absence.id '
                          '}}/message"><textarea name="body" rows="3" required placeholder="Écrire une '
                          'réponse ou une précision"></textarea><button>Envoyer le '
                          'message</button></form></section>\n'
                          '<section class="panel"><h2>Traitement</h2>{% if user.role in [\'rh\',\'admin\'] '
                          '%}<form method="post" action="/absences/{{ absence.id '
                          '}}/complement"><label>Demande de complément<textarea name="body" rows="3" '
                          'required placeholder="Précisez les informations ou pièces '
                          'attendues"></textarea></label><button class="warning">Demander un '
                          'complément</button></form><hr><form method="post" action="/absences/{{ absence.id '
                          '}}/decision"><label>Décision<select name="decision"><option '
                          'value="en_cours">Mettre en cours</option><option '
                          'value="valide">Valider</option><option '
                          'value="rejete">Rejeter</option></select></label><label>Note<textarea name="note" '
                          'rows="3"></textarea></label><button>Enregistrer la décision</button></form>{% '
                          'else %}<p>Le service RH peut demander un complément, valider ou rejeter le '
                          'dossier. Vous recevrez la demande directement dans cet espace.</p>{% endif '
                          '%}<hr><h3>Traçabilité</h3><ul class="timeline">{% for e in absence.events|reverse '
                          "%}<li><b>{{ e.action.replace('_',' ') }}</b><small>{{ e.actor.full_name }} · {{ "
                          "e.created_at.strftime('%d/%m/%Y %H:%M') }}</small>{% if e.details %}<p>{{ "
                          'e.details }}</p>{% endif %}</li>{% endfor %}</ul></section></div>{% endblock %}\n',
 'templates/login.html': '{% extends \'base.html\' %}{% block content %}<section class="login-wrap"><div '
                         'class="login-card"><h1>Connexion sécurisée</h1><p>Accédez à votre espace de dépôt '
                         'et de suivi.</p><form method="post" action="/login"><label>E-mail '
                         'professionnel<input type="email" name="email" required '
                         'placeholder="prenom.nom@aibd.sn"></label><label>Mot de passe<input type="password" '
                         'name="password" required></label><button>Se '
                         'connecter</button></form></div></section>{% endblock %}\n',
 'templates/new_absence.html': "{% extends 'base.html' %}{% block content %}<div "
                               'class="page-title"><h1>Nouveau justificatif d\'absence</h1><p>Renseignez la '
                               'période et joignez les pièces justificatives disponibles.</p></div><section '
                               'class="panel form-panel"><form method="post" '
                               'enctype="multipart/form-data"><div class="grid2"><label>Type '
                               'd\'absence<select name="absence_type" '
                               'required><option>Maladie</option><option>Accident du '
                               'travail</option><option>Événement familial</option><option>Autorisation '
                               "d'absence</option><option>Congé "
                               'exceptionnel</option><option>Autre</option></select></label><label>Agent<input '
                               'value="{{ user.full_name }} — {{ user.matricule }}" '
                               'disabled></label><label>Date de début<input type="date" name="start_date" '
                               'required></label><label>Date de fin<input type="date" name="end_date" '
                               'required></label></div><label>Motif ou précision<textarea name="reason" '
                               'rows="4" placeholder="Informations utiles au traitement du '
                               'dossier"></textarea></label><label>Pièces justificatives<input type="file" '
                               'name="documents" multiple '
                               'accept=".pdf,.jpg,.jpeg,.png,.doc,.docx"><small>PDF, image ou document '
                               'bureautique — 10 Mo maximum par fichier.</small></label><div '
                               'class="actions"><a class="button secondary" '
                               'href="/">Annuler</a><button>Soumettre le '
                               'dossier</button></div></form></section>{% endblock %}\n',
 'templates/users.html': "{% extends 'base.html' %}{% block content %}<div "
                         'class="page-title"><h1>Administration des utilisateurs</h1><p>Création des comptes '
                         'agents, RH et administrateurs.</p></div><div class="detail-grid"><section '
                         'class="panel"><h2>Nouvel utilisateur</h2><form method="post"><div '
                         'class="grid2"><label>Matricule<input name="matricule" required></label><label>Nom '
                         'complet<input name="full_name" required></label><label>E-mail<input type="email" '
                         'name="email" required></label><label>Département<input '
                         'name="department"></label><label>Site<select '
                         'name="site"><option>DIASS</option><option>YOFF</option><option>SAINT-LOUIS</option><option>ZIGUINCHOR</option><option>CAP-SKIRRING</option></select></label><label>Rôle<select '
                         'name="role"><option value="agent">Agent</option><option '
                         'value="manager">Manager</option><option value="rh">RH</option><option '
                         'value="admin">Administrateur</option></select></label></div><label>Mot de passe '
                         'initial<input type="password" name="password" required '
                         'minlength="8"></label><button>Créer le compte</button></form></section><section '
                         'class="panel"><h2>Comptes existants</h2><div class="users">{% for u in users '
                         '%}<div class="user-row"><div><b>{{ u.full_name }}</b><small>{{ u.email }} · {{ '
                         'u.matricule }}</small></div><span class="badge">{{ u.role }}</span></div>{% endfor '
                         '%}</div></section></div>{% endblock %}\n'}

def ensure_assets(base_dir: Path) -> None:
    for relative_path, content in ASSETS.items():
        target = base_dir / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            target.write_text(content, encoding="utf-8")
