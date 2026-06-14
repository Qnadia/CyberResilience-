#!/usr/bin/env python3
import json

SLIDE_W = 1920
SLIDE_H = 1080
GAP = 100

def frame_x(n):  # n is 1-based
    return (n - 1) * (SLIDE_W + GAP)

def mk_frame(n, title):
    fx = frame_x(n)
    return {
        "id": f"frame_{n}", "type": "frame",
        "x": fx, "y": 0, "width": SLIDE_W, "height": SLIDE_H,
        "angle": 0, "strokeColor": "#4fc3f7", "backgroundColor": "#0d1b4b",
        "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100, "groupIds": [], "frameId": None,
        "roundness": None, "seed": n*100, "version": 1, "versionNonce": 1,
        "isDeleted": False, "boundElements": None, "updated": 1,
        "link": None, "locked": False, "name": title
    }

def mk_rect(eid, n, rx, ry, rw, rh, bg="#1e3a5f", stroke="#4fc3f7", rounded=True):
    fx = frame_x(n)
    return {
        "id": eid, "type": "rectangle",
        "x": fx + rx, "y": ry, "width": rw, "height": rh,
        "angle": 0, "strokeColor": stroke, "backgroundColor": bg,
        "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100, "groupIds": [], "frameId": f"frame_{n}",
        "roundness": {"type": 3} if rounded else None,
        "seed": hash(eid) % 99999, "version": 1, "versionNonce": 1,
        "isDeleted": False, "boundElements": None, "updated": 1,
        "link": None, "locked": False
    }

def mk_text(eid, n, tx, ty, tw, th, text, size=14, color="#e3f2fd", align="left"):
    fx = frame_x(n)
    return {
        "id": eid, "type": "text",
        "x": fx + tx, "y": ty, "width": tw, "height": th,
        "angle": 0, "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100, "groupIds": [], "frameId": f"frame_{n}",
        "roundness": None, "seed": hash(eid) % 99999, "version": 1, "versionNonce": 1,
        "isDeleted": False, "boundElements": None, "updated": 1,
        "link": None, "locked": False,
        "text": text, "fontSize": size, "fontFamily": 1,
        "textAlign": align, "verticalAlign": "top",
        "containerId": None, "originalText": text, "lineHeight": 1.25
    }

def mk_control_slide(slide_num, section_title, controls):
    """Generate a slide for an Annex A section with controls.
    controls = list of (code, name, outil, mesure, ctrl_proof)
    """
    elems = []
    n = slide_num
    fx = frame_x(n)

    elems.append(mk_frame(n, section_title))
    elems.append(mk_text(f"s{n}_title", n, 60, 25, 1800, 55,
        section_title, size=30, color="#ffffff", align="center"))

    # Layout: up to 4 controls per row, 2 rows max (8 per slide)
    cols = min(len(controls), 4) if len(controls) > 0 else 1
    rows = (len(controls) + cols - 1) // cols

    cell_w = (1800 // cols) - 10
    cell_h = (960 // rows) - 10

    for i, (code, name, outil, mesure, ctrl_proof) in enumerate(controls):
        col = i % cols
        row = i // cols
        cx = 60 + col * (cell_w + 10)
        cy = 90 + row * (cell_h + 10)

        eid_prefix = f"s{n}_c{i}"

        elems.append(mk_rect(f"{eid_prefix}_bg", n, cx, cy, cell_w, cell_h,
                              bg="#102027", stroke="#546e7a"))

        # Control code & name header
        elems.append(mk_rect(f"{eid_prefix}_hdr", n, cx, cy, cell_w, 40,
                              bg="#1565c0", stroke="#4fc3f7", rounded=False))
        elems.append(mk_text(f"{eid_prefix}_hdr_t", n, cx+5, cy+5, cell_w-10, 30,
                             f"{code} – {name}", size=14, color="#ffffff"))

        # OUTIL
        elems.append(mk_rect(f"{eid_prefix}_o_lbl", n, cx, cy+40, cell_w, 22,
                              bg="#1b5e20", stroke="#66bb6a", rounded=False))
        elems.append(mk_text(f"{eid_prefix}_o_lbl_t", n, cx+5, cy+43, 70, 16,
                             "OUTIL :", size=12, color="#a5d6a7"))
        elems.append(mk_text(f"{eid_prefix}_outil", n, cx+5, cy+65, cell_w-10, 45,
                             outil, size=12, color="#c8e6c9"))

        # MESURE
        elems.append(mk_rect(f"{eid_prefix}_m_lbl", n, cx, cy+115, cell_w, 22,
                              bg="#e65100", stroke="#ffa726", rounded=False))
        elems.append(mk_text(f"{eid_prefix}_m_lbl_t", n, cx+5, cy+118, 80, 16,
                             "MESURE :", size=12, color="#ffe082"))
        elems.append(mk_text(f"{eid_prefix}_mesure", n, cx+5, cy+140, cell_w-10, 55,
                             mesure, size=12, color="#fff8e1"))

        # CONTRÔLE
        elems.append(mk_rect(f"{eid_prefix}_c_lbl", n, cx, cy+200, cell_w, 22,
                              bg="#4a148c", stroke="#ce93d8", rounded=False))
        elems.append(mk_text(f"{eid_prefix}_c_lbl_t", n, cx+5, cy+203, 90, 16,
                             "CONTRÔLE :", size=12, color="#e1bee7"))
        elems.append(mk_text(f"{eid_prefix}_ctrl", n, cx+5, cy+225, cell_w-10, 55,
                             ctrl_proof, size=12, color="#f3e5f5"))

    return elems

# === SLIDE DATA ===
slides_data = [
    # Slide 3: A.5 Politiques
    (3, "Slide 3 – A.5 Politiques de sécurité de l'information (2 contrôles)", [
        ("A.5.1", "Politiques pour la sécurité de l'information",
         "SharePoint / Google Docs\n(gestion documentaire versionnée)",
         "Rédiger une politique signée par la direction,\nrevue annuellement",
         "Document daté et signé, historique des versions,\nPV de revue"),
        ("A.5.2", "Revue des politiques de sécurité de l'information",
         "Calendrier Outlook / Trello / Jira\n(planification des revues)",
         "Planifier une revue annuelle avec les parties\nprenantes concernées",
         "Compte rendu de réunion, traçabilité des\nmodifications apportées"),
    ]),

    # Slide 4: A.6 Organisation
    (4, "Slide 4 – A.6 Organisation de la sécurité de l'information (8 contrôles)", [
        ("A.6.1", "Organisation interne",
         "Teams / Slack (canaux dédiés sécurité)",
         "Créer un comité de sécurité avec rôles définis",
         "Organigramme sécurité, PV de réunions"),
        ("A.6.2", "Mobilité et télétravail",
         "VPN (Fortinet, Palo Alto, OpenVPN)\nMDM (Intune, MobileIron)",
         "Politique de télétravail, MFA obligatoire",
         "Logs de connexion VPN, paramétrage MDM"),
        ("A.6.3", "Attribution des responsabilités",
         "Azure AD / Active Directory\n(délégation d'administration)",
         "Matrice RACI (Responsable, Approbateur,\nConsulté, Informé)",
         "Fiches de poste signées, matrices\nd'habilitation"),
        ("A.6.4", "Séparation des tâches",
         "SailPoint, OneIdentity\n(gestion des accès)",
         "Un utilisateur ne peut pas créer ET valider\nun virement",
         "Matrice d'incompatibilités, revue annuelle\ndes droits"),
        ("A.6.5", "Responsabilités vis-à-vis des autorités",
         "Registre des contacts\n(Excel sécurisé, ServiceNow)",
         "Identifier l'autorité nationale (ANSSI, DGSSI,\nCNDP...)",
         "Contact à jour, preuve de notification en\ncas d'incident"),
        ("A.6.6", "Contact avec groupes d'intérêt spécifiques",
         "Listes de diffusion (Mailchimp, Gmail groups)",
         "Adhésion à un CERT/CIRT, participation\naux forums (FIRST, GFCE)",
         "Attestation d'adhésion, PV de participation"),
        ("A.6.7", "Gestion des incidents en télétravail",
         "SIEM (Splunk, QRadar, Wazuh)",
         "Procédure de signalement à distance\n(hotline 24/7)",
         "Logs des incidents, tickets d'incident\nenregistrés"),
        ("A.6.8", "Gestion des capacités et performance",
         "Nagios, Zabbix, PRTG, Datadog",
         "Surveillance CPU, RAM, bande passante\navec seuils d'alerte",
         "Rapports de capacité mensuels, alertes\nconfigurées"),
    ]),

    # Slide 5: A.7 Ressources humaines
    (5, "Slide 5 – A.7 Sécurité liée aux ressources humaines (6 contrôles)", [
        ("A.7.1", "Avant embauche – Vérification des antécédents",
         "SIRH (Sage, Silae, ADP)",
         "Casier judiciaire, vérification des diplômes\n(selon sensibilité du poste)",
         "Formulaire de vérification signé, traçabilité\nRH"),
        ("A.7.2", "Avant embauche – Termes et conditions",
         "Signature électronique (Docusign, Yousign)",
         "Clause de confidentialité dans le contrat\nde travail (NDA)",
         "Contrat signé avec clause de confidentialité\narchivée"),
        ("A.7.3", "Pendant emploi – Responsabilités direction",
         "LMS (Moodle, 360Learning, Docebo)",
         "Sensibilisation annuelle obligatoire\nà la sécurité",
         "Taux de complétion des modules, attestations\nde formation"),
        ("A.7.4", "Pendant emploi – Processus disciplinaires",
         "Registre RH (Excel sécurisé, SIRH)",
         "Échelle de sanctions en cas de non-respect\nde la politique sécurité",
         "Registre des infractions et sanctions\nappliquées"),
        ("A.7.5", "Fin de contrat – Retour des actifs",
         "GLPI, Snipe-IT, ServiceNow\n(gestion des assets)",
         "Checklist de restitution : ordinateur, badge,\nclés, tokens",
         "Formulaire de restitution signé par\nl'employé et le manager"),
        ("A.7.6", "Fin de contrat – Révocation des droits d'accès",
         "IAM (Okta, Keycloak, Active Directory)",
         "Révocation de tous les accès dans les 24h\nsuivant le départ",
         "Logs de révocation, attestation de\nsuppression des comptes"),
    ]),

    # Slide 6: A.8 Gestion des actifs
    (6, "Slide 6 – A.8 Gestion des actifs (10 contrôles)", [
        ("A.8.1", "Inventaire des actifs",
         "GLPI, Snipe-IT, Lansweeper, ServiceNow",
         "Inventaire trimestriel des équipements\n(matériels et logiciels)",
         "Export de l'inventaire, taux de couverture\n>98%"),
        ("A.8.2", "Propriété des actifs",
         "GLPI avec champ 'propriétaire' obligatoire",
         "Désigner un propriétaire pour chaque actif\nenregistré",
         "Champ 'owner' renseigné dans l'inventaire\n(audit mensuel)"),
        ("A.8.3", "Utilisation acceptable des actifs",
         "Acceptation électronique (Docusign,\nGoogle Forms)",
         "Charte d'utilisation signée par tous\nles utilisateurs",
         "Taux de signature 100%, archivage des\nchartes signées"),
        ("A.8.4", "Restitution des actifs",
         "Workflow ServiceNow / GLPI",
         "Procédure formalisée de restitution en\nfin de contrat",
         "Checklist de restitution signée par les\ndeux parties"),
        ("A.8.5", "Classification des informations",
         "Microsoft Purview, Varonis\n(classification automatique)",
         "Grille : Public / Interne / Confidentiel /\nSecret",
         "Exemple de document classifié,\ntraçabilité de la classification"),
        ("A.8.6", "Étiquetage des informations",
         "Métadonnées SharePoint, Nextcloud\n(étiquettes auto)",
         "Apposer 'CONFIDENTIEL' sur tous les\ndocuments sensibles",
         "Capture d'écran d'un document étiqueté,\naudit documentaire"),
        ("A.8.7", "Gestion des supports amovibles",
         "DLP (Forcepoint, Symantec, Microsoft\nPurview)",
         "Interdire les clés USB non chiffrées,\nlogs des transferts",
         "Politique GPO interdisant USB non autorisées,\nalertes DLP"),
        ("A.8.8", "Effacement sécurisé des supports",
         "DBAN, Blancco, Eraser",
         "Effacement cryptographique avant réforme\nou don du matériel",
         "Certificat d'effacement pour chaque support\nréformé"),
        ("A.8.9", "Supports physiques en transit",
         "Transport sécurisé (colis plombé,\nsérigraphie discrète)",
         "Plombage des colis, envoi avec accusé\nde réception",
         "Bordereau d'envoi scellé, accusé de\nréception signé"),
        ("A.8.10", "Gestion du cloud – externalisation",
         "CASB (Netskope, McAfee MVISION,\nMicrosoft CASB)",
         "Vérifier la localisation des données (hors\nsol national si exigé)",
         "Contrat cloud avec clause de localisation\ndes données"),
    ]),

    # Slide 7: A.9 Maîtrise d'accès
    (7, "Slide 7 – A.9 Maîtrise d'accès (extraits – 8 contrôles clés)", [
        ("A.9.1", "Politique de contrôle d'accès",
         "Azure AD / Active Directory avec GPO",
         "Politique basée sur le 'moindre privilège',\ndocumentée et revue",
         "Document de politique + matrice\nd'habilitation signée"),
        ("A.9.2", "Accès réseaux et services réseau",
         "NAC (Cisco ISE, FortiNAC, PacketFence)",
         "Segmentation réseau (VLAN), authentification\n802.1X",
         "Schéma de segmentation, logs NAC,\nplan d'adressage"),
        ("A.9.3", "Gestion des mots de passe",
         "Keeper, Bitwarden, 1Password Entreprise",
         "Complexité : 12 caract. (maj/min/chiff./spéc.),\nchangement 90j",
         "Politique GPO, audit des mots de passe\n(outil de test)"),
        ("A.9.4", "Authentification forte (MFA)",
         "Microsoft Authenticator, Duo, Yubikey,\nGoogle Authenticator",
         "MFA obligatoire pour tout accès externe\n(VPN, O365, cloud)",
         "Taux d'activation MFA >95%, rapport de\nconsole IAM"),
        ("A.9.5", "Révocation des droits d'accès",
         "IAM (Okta, Keycloak, Active Directory)",
         "Suppression des comptes dans les 48h\nsuivant le départ",
         "Logs de suppression, revue trimestrielle\ndes accès"),
        ("A.9.6", "Accès privilégiés (administrateurs)",
         "PAM (CyberArk, BeyondTrust, Wallix)",
         "Comptes admin nominatifs, utilisation\n'juste à temps' (JIT)",
         "Traçabilité des actions admin, sessions\nenregistrées"),
        ("A.9.7", "Réexamen des droits d'accès",
         "SailPoint, OneIdentity\n(revue automatisée)",
         "Revue annuelle avec les managers\n(validation ou révocation)",
         "PV de revue signé, action sur droits\nobsolètes documentée"),
        ("A.9.8", "Gestion des comptes génériques",
         "ServiceNow (demande exceptionnelle\navec justification)",
         "Interdiction sauf exception dûment justifiée\navec traçabilité nominative",
         "Registre des comptes génériques et\njustifications associées"),
    ]),

    # Slide 8: A.10 Cryptographie
    (8, "Slide 8 – A.10 Cryptographie (2 contrôles)", [
        ("A.10.1", "Politique d'utilisation des mesures cryptographiques",
         "Venafi, Keyfactor\n(gestion des certificats)",
         "Choisir des algorithmes reconnus : AES-256,\nRSA-2048, SHA-256",
         "Document de politique cryptographique +\ninventaire des certificats"),
        ("A.10.2", "Gestion des clés cryptographiques",
         "AWS KMS, Azure Key Vault,\nHashiCorp Vault",
         "Cycle de vie des clés : génération, stockage\nsécurisé, renouvellement, destruction",
         "Traçabilité des accès aux clés, rotation\nannuelle documentée"),
    ]),

    # Slide 9: A.11 Sécurité physique
    (9, "Slide 9 – A.11 Sécurité physique et environnementale (extraits)", [
        ("A.11.1", "Périmètre de sécurité physique",
         "Badges RFID (HID, Kaba, Nedap)",
         "Zones sécurisées : publique, interne,\nrestreinte (datacenter)",
         "Plans des zones de sécurité + registre\ndes badges émis"),
        ("A.11.2", "Contrôle d'accès physique",
         "Portillon + lecteur badges (Axis, HID)",
         "Badge nominatif + code PIN pour les zones\ncritiques",
         "Logs des accès physiques (conservation\n3 mois minimum)"),
        ("A.11.3", "Vidéoprotection",
         "Caméras IP (Axis, Hikvision, Dahua) + NVR",
         "Couverture des zones sensibles (datacenter,\nsalles serveurs)",
         "Enregistrements conservés 30j, revue\nannuelle du dispositif"),
        ("A.11.4", "Sécurité incendie",
         "Détecteurs fumée + extincteurs FM200/Novec\n(salles serveurs)",
         "Système d'extinction automatique\n(gaz inerte)",
         "Certificat de conformité, maintenance\nannuelle du système"),
        ("A.11.5", "Protection dégâts des eaux",
         "Détecteurs d'eau + surélévateurs\n(racks surélevés)",
         "Passage des gaines hors zone sensible,\ndétecteurs au sol",
         "Test mensuel des détecteurs d'eau,\nrapport de contrôle"),
        ("A.11.6", "Onduleurs et groupes électrogènes",
         "APC, Eaton, Vertiv (onduleurs)\n+ groupes Caterpillar",
         "Autonomie min. 30 min (onduleur) + 48h\n(groupe électrogène)",
         "Test hebdomadaire des batteries, exercice\ntrimestriel du groupe"),
        ("A.11.7", "Climatisation salle serveurs",
         "Climatisation de précision (Stulz,\nSchneider Electric)",
         "Température 18-27°C, hygrométrie\n40-60% maintenues",
         "Relevés quotidiens automatisés,\nmaintenance semestrielle"),
        ("A.11.8", "Sécurité des câblages",
         "Goulottes, chemins de câbles\n(Legrand, D-Line)",
         "Séparation courant fort/faible,\nétiquetage systématique",
         "Plan des chemins de câbles, inspection\nannuelle"),
    ]),

    # Slide 10: A.12 Sécurité exploitation
    (10, "Slide 10 – A.12 Sécurité liée à l'exploitation (extraits)", [
        ("A.12.1", "Gestion des changements",
         "ServiceNow, Jira Service Management, iTop",
         "Processus formel : demande → validation\n→ test → déploiement → clôture",
         "Tickets de changement avec approbation\nsignée"),
        ("A.12.2", "Gestion des capacités",
         "Nagios, Zabbix, PRTG, Datadog",
         "Seuils d'alerte : CPU>80%, RAM>85%,\ndisque>90%",
         "Rapports de capacité mensuels,\npreuve d'upgrade si dépassement"),
        ("A.12.3", "Protection contre les logiciels malveillants",
         "EDR (CrowdStrike, SentinelOne, Microsoft\nDefender, TrendMicro)",
         "Mise à jour automatique des signatures\n(quotidienne)",
         "Rapport console antivirus (taux de mise\nà jour, détections)"),
        ("A.12.4", "Sauvegarde",
         "Veeam, Acronis, Commvault, Rubrik",
         "Stratégie 3-2-1 : 3 copies, 2 supports\ndifférents, 1 hors site",
         "Rapport de sauvegarde, test de restauration\nannuel documenté"),
        ("A.12.5", "Restauration (RPO/RTO)",
         "Veeam SureBackup (test automatisé\nde restauration)",
         "RPO < 4h, RTO < 24h\n(à adapter par processus critique)",
         "Procès-verbal de test de restauration\navec résultats"),
        ("A.12.6", "Journalisation des événements",
         "SIEM (Splunk, QRadar, Wazuh,\nMicrosoft Sentinel)",
         "Logs centralisés : systèmes, applications,\naccès, sécurité",
         "Conservation 12 mois, vérification de\nl'intégrité des logs"),
        ("A.12.7", "Gestion des vulnérabilités techniques",
         "Qualys, Tenable Nessus, Greenbone\n(scanners)",
         "Scan trimestriel + scan critique mensuel,\nplan de correction",
         "Rapport de scan, délais correction :\ncritique <72h, haute <14j"),
        ("A.12.8", "Gestion des correctifs",
         "WSUS, ManageEngine Patch Manager,\nAutomox",
         "Correctifs sécurité sous 14j (critique\nsous 48h)",
         "Rapport d'application des correctifs\n(taux de couverture)"),
    ]),

    # Slide 11: A.13 Communications
    (11, "Slide 11 – A.13 Sécurité des communications (7 contrôles)", [
        ("A.13.1", "Sécurité des réseaux",
         "Firewall NGF (FortiGate, Palo Alto,\nCheckPoint)",
         "Règle 'deny all' par défaut, ouverture\nau strict nécessaire",
         "Matrice des flux, revue semestrielle\ndes règles firewall"),
        ("A.13.2", "Séparation des réseaux",
         "VLAN, sous-réseaux, DMZ\n(switch managé Cisco/HP)",
         "Segmentation réseau : production ≠ test\n≠ administration",
         "Schéma d'architecture réseau, tests\nde segmentation"),
        ("A.13.3", "Séparation dev/production",
         "VLAN séparés ou réseaux physiquement\ndistincts",
         "Accès production ≠ accès développement\n(droits différenciés)",
         "Schéma réseau, matrice des droits par\nenvironnement"),
        ("A.13.4", "Transfert de l'information",
         "SFTP, FTPS, Kiteworks, GoAnywhere\n(transfert sécurisé)",
         "Chiffrement des flux (TLS 1.2 minimum),\ntraçabilité des échanges",
         "Logs de transfert, analyse DLP sur\nles flux sortants"),
        ("A.13.5", "Messagerie électronique",
         "Proofpoint, Mimecast, Microsoft Defender\nfor O365 (anti-spam)",
         "Protection antivirus, anti-phishing,\nfiltrage des pièces jointes",
         "Rapport de filtrage mensuel, alertes\nsur détections"),
        ("A.13.6", "Accès distants",
         "VPN SSL (FortiClient, Pulse Secure,\nOpenVPN)",
         "MFA obligatoire + session timeout\n(30 min d'inactivité)",
         "Logs de connexion VPN, revue trimestrielle\ndes accès distants"),
        ("A.13.7", "Réseaux sans fil (WiFi)",
         "WPA3 / WPA2-Enterprise, RADIUS\n(FreeRADIUS, Cisco ISE)",
         "Authentification individuelle, VLAN invité\nisolé du réseau interne",
         "Scan WiFi (détection rogues), logs\nd'authentification RADIUS"),
    ]),

    # Slide 12: A.14 Développement
    (12, "Slide 12 – A.14 Acquisition, développement et maintenance (extraits)", [
        ("A.14.1", "Analyse des exigences de sécurité",
         "Jira / Confluence (user stories\nde sécurité)",
         "Checklist d'exigences sécurité en amont\nde chaque projet",
         "User stories tracées, sign-off sécurité\nrequis avant dev"),
        ("A.14.2", "Sécurité des applications",
         "SAST (SonarQube, Checkmarx, Fortify)",
         "Revue de code, analyse statique avant\nla mise en production",
         "Rapport SAST (0 critique, 0 haute avant\ndéploiement)"),
        ("A.14.3", "Protection des transactions applicatives",
         "WAF (F5, Cloudflare, ModSecurity)",
         "Validation des inputs, protection injection\nSQL, anti-XSS",
         "Règles WAF actives, logs d'attaques\nblocquées"),
        ("A.14.4", "Tests de sécurité des applications",
         "DAST (Burp Suite, OWASP ZAP, Acunetix)",
         "Tests d'intrusion annuels + tests de\nnon-régression à chaque release",
         "Rapport de test (pentest), plan de\ncorrection signé"),
        ("A.14.5", "Environnements de développement sécurisés",
         "Docker, VMs isolées, Kubernetes\n(namespace séparés)",
         "Données de test anonymisées\n(pas de données réelles en dev)",
         "Preuve d'anonymisation, contrôle d'accès\nrestreint aux envs dev"),
        ("A.14.6", "Contrôle des changements de code",
         "Git + GitLab CI, GitHub Actions,\nAzure DevOps",
         "Peer review obligatoire, signature\ndes commits (GPG)",
         "Historique Git, validation avant merge,\npolitique de branches"),
        ("A.14.7", "Protection du code source",
         "Forge privée (GitLab on-prem,\nBitbucket Server)",
         "Dépôts privés, ACLs restrictives,\nlogs d'accès activés",
         "Politique d'accès aux dépôts, revue\ndes droits trimestrielle"),
    ]),

    # Slide 13: A.15 Fournisseurs
    (13, "Slide 13 – A.15 Relations avec les fournisseurs (5 contrôles)", [
        ("A.15.1", "Politique sécurité des relations fournisseurs",
         "Outil de gestion des contrats\n(Docusign CLM, Icertis)",
         "Clauses de sécurité dans tous les contrats\n(confidentialité, audit, incident)",
         "Modèle de contrat avec clauses sécurité\nvalidées par le RSSI"),
        ("A.15.2", "Exigences contractuelles de sécurité",
         "Questionnaire d'évaluation\n(Google Forms, Qualtrics)",
         "Droit d'audit, notification d'incident <24h,\nlocalisation des données",
         "Contrat signé avec checklist des clauses\nde sécurité cochées"),
        ("A.15.3", "Chaîne d'approvisionnement",
         "BitSight, SecurityScorecard\n(analyse risque fournisseurs)",
         "Évaluation de sécurité des sous-traitants\n(questionnaire + scoring)",
         "Registre des sous-traitants avec score\nde sécurité"),
        ("A.15.4", "Surveillance des services fournisseurs",
         "ServiceNow, GLPI\n(suivi des incidents fournisseurs)",
         "KPI de sécurité fournisseurs (délai\ncorrection vulnérabilités, SLA)",
         "Tableau de bord fournisseurs, revue\ntrimestrielle de performance"),
        ("A.15.5", "Gestion des incidents chez les fournisseurs",
         "Portail de déclaration\n(ServiceNow fournisseur)",
         "Notification d'incident dans les 24h,\nplan de continuité fournisseur",
         "Registre des incidents fournisseurs,\nPV de réunion post-incident"),
    ]),

    # Slide 14: A.16 Incidents
    (14, "Slide 14 – A.16 Gestion des incidents de sécurité (extraits)", [
        ("A.16.1", "Responsabilités et procédures",
         "ServiceNow, GLPI, TheHive (CERT)",
         "Procédure documentée : détection →\nqualification → réponse → clôture",
         "Document de procédure signé par\nle RSSI et la direction"),
        ("A.16.2", "Signalement des incidents",
         "Hotline sécurité, formulaire web\n(Jira Service Management)",
         "Tous les utilisateurs savent comment\nsignaler (affiche, email, formation)",
         "Tracé des signalements, temps de\nréponse initial <1h"),
        ("A.16.3", "Réponse aux incidents",
         "SOAR (TheHive+Cortex, Demisto,\nSplunk SOAR)",
         "Playbooks d'intervention : malware,\nintrusion, ransomware, DDoS",
         "Rapport d'incident (timeline des actions,\ndécisions prises)"),
        ("A.16.4", "Recueil des preuves numériques",
         "FTK Imager, Autopsy, EnCase\n(outils forensic)",
         "Chaîne de conservation des preuves\n(hash SHA256, signature)",
         "Rapport forensic avec hash de preuve,\nchaîne de custody"),
        ("A.16.5", "Remontée d'information post-incident (REX)",
         "Registre des incidents\n(ServiceNow, Excel sécurisé)",
         "Retour d'expérience (REX) après chaque\nincident majeur",
         "Rapport REX, actions correctives avec\nresponsables et délais"),
    ]),

    # Slide 15: A.17 Continuité
    (15, "Slide 15 – A.17 Continuité de l'activité (4 contrôles)", [
        ("A.17.1", "Planification de la continuité",
         "Outil de BIA (MyBIA, Castellan,\nResilient Systems)",
         "Analyse d'impact (BIA) réalisée pour\nchaque processus critique",
         "Document BIA, RTO/RPO définis et\nvalidés par la direction"),
        ("A.17.2", "Mise en œuvre de la continuité (PCA/PRA)",
         "PCA/PRA documenté + équipements\nredondants (cluster, réplication)",
         "Site de secours, bascule automatique,\ncluster HA configuré",
         "Test de bascule annuel, PV de test\navec constats et actions"),
        ("A.17.3", "Vérification des plans de continuité",
         "Veeam SureBackup, simulateur\nde crise (exercice sur table)",
         "Test technique trimestriel, test complet\nannuel avec simulation",
         "PV de test avec constats, mesures\ncorrectives documentées"),
        ("A.17.4", "Disponibilité des moyens de traitement",
         "Load balancer (F5, HAProxy),\ncluster (VMware vSphere, Nutanix)",
         "Architecture HA (High Availability) avec\nredondance matérielle (RAID, UPS)",
         "Schéma d'architecture HA validé,\ntaux de disponibilité mesuré"),
    ]),

    # Slide 16: A.18 Conformité
    (16, "Slide 16 – A.18 Conformité (extraits – 4 contrôles clés)", [
        ("A.18.1", "Conformité aux exigences légales et contractuelles",
         "Veille réglementaire (Legitech, Dalloz,\nJurisConsult)",
         "Registre des exigences légales (loi 05-20,\nRGPD, loi 09-08...)",
         "Registre tenu à jour, revue annuelle\npar le juriste"),
        ("A.18.2", "Conformité aux exigences de sécurité",
         "SharePoint, Confluence\n(gestion des politiques)",
         "Vérification des écarts de conformité\n(plan d'actions correctives)",
         "Rapport d'audit interne + plan de\ncorrection signé"),
        ("A.18.3", "Audit interne de conformité",
         "AuditBoard, Ideagen\n(outil d'audit)",
         "Audit interne au moins 1 fois par an\nselon programme défini",
         "Programme d'audit approuvé, rapport\nd'audit, plan d'actions"),
        ("A.18.4", "Protection des données personnelles (RGPD/09-08)",
         "OneTrust, DataMap\n(cartographie des données)",
         "Registre des traitements, désignation\ndu DPO ou correspondant CNDP",
         "Registre des traitements à jour,\navis/déclaration CNDP"),
    ]),
]

# === SLIDE 17 – Outils récapitulatifs ===
def mk_slide17():
    n = 17
    elems = []
    elems.append(mk_frame(n, "Slide 17 – Récapitulatif des outils par catégorie"))
    elems.append(mk_text(f"s{n}_title", n, 60, 20, 1800, 50,
        "Récapitulatif des outils par catégorie", size=30, color="#ffffff", align="center"))

    tools = [
        ("Gestion des actifs", "GLPI, Snipe-IT, ServiceNow, Lansweeper"),
        ("Gestion des accès (IAM)", "Active Directory, Azure AD, Okta, Keycloak"),
        ("PAM (comptes admin)", "CyberArk, BeyondTrust, Wallix"),
        ("MFA", "Microsoft Authenticator, Duo Security, Yubikey"),
        ("Antivirus / EDR", "CrowdStrike, SentinelOne, Microsoft Defender, TrendMicro"),
        ("SIEM", "Splunk, QRadar, Wazuh, Microsoft Sentinel"),
        ("Scanner vulnérabilités", "Qualys, Tenable Nessus, Greenbone OpenVAS"),
        ("Gestion des correctifs", "WSUS, ManageEngine Patch Manager, Automox"),
        ("Sauvegarde & restauration", "Veeam, Acronis, Commvault, Rubrik"),
        ("Firewall NGF", "FortiGate, Palo Alto Networks, CheckPoint"),
        ("VPN", "FortiClient VPN, Pulse Secure, OpenVPN"),
        ("WAF", "F5 Advanced WAF, Cloudflare WAF, ModSecurity"),
        ("SAST/DAST", "SonarQube, Checkmarx, OWASP ZAP, Burp Suite"),
        ("Gestion des incidents", "ServiceNow, TheHive, GLPI, Jira Service Mgmt"),
        ("Gestionnaire MDP", "Keeper, Bitwarden Enterprise, 1Password"),
        ("Gestion clés/certificats", "AWS KMS, Azure Key Vault, HashiCorp Vault, Venafi"),
        ("Sécurité physique", "Badges RFID HID, caméras Axis, onduleurs APC, Stulz"),
        ("DLP", "Forcepoint, Symantec DLP, Microsoft Purview"),
    ]

    cols = 3
    col_w = 590
    row_h = 52

    for i, (cat, outils) in enumerate(tools):
        col = i % cols
        row = i // cols
        cx = 60 + col * (col_w + 20)
        cy = 80 + row * (row_h + 5)

        elems.append(mk_rect(f"s{n}_r{i}_bg", n, cx, cy, col_w, row_h,
                              bg="#1a237e", stroke="#3949ab"))
        elems.append(mk_rect(f"s{n}_r{i}_lbl", n, cx, cy, 230, row_h,
                              bg="#1565c0", stroke="#3949ab", rounded=False))
        elems.append(mk_text(f"s{n}_r{i}_cat", n, cx+5, cy+5, 220, 42,
                             cat, size=13, color="#90caf9"))
        elems.append(mk_text(f"s{n}_r{i}_tools", n, cx+238, cy+5, col_w-250, 42,
                             outils, size=12, color="#e3f2fd"))

    return elems

# === SLIDE 18 – Fiche Mémo ===
def mk_slide18():
    n = 18
    elems = []
    elems.append(mk_frame(n, "Slide 18 – Fiche Mémo ISO 27001:2022"))
    elems.append(mk_text(f"s{n}_title", n, 60, 20, 1800, 50,
        "FICHE MÉMO – ISO/IEC 27001:2022", size=32, color="#ffffff", align="center"))

    # PDCA box
    elems.append(mk_rect(f"s{n}_pdca", n, 60, 85, 880, 280, bg="#1565c0", stroke="#4fc3f7"))
    elems.append(mk_text(f"s{n}_pdca_t", n, 70, 92, 860, 35,
        "Cycle PDCA", size=20, color="#90caf9"))
    elems.append(mk_text(f"s{n}_pdca_c", n, 70, 130, 860, 220,
        "PLAN  (Cl.4-6) → Contexte, Leadership, Planification des risques\n"
        "DO    (Cl.7-8) → Mise en oeuvre : formation, support, controles\n"
        "CHECK (Cl.9)   → Audit interne, surveillance, revue de direction\n"
        "ACT   (Cl.10)  → Non-conformites, actions correctives, amelioration",
        size=16, color="#e3f2fd"))

    # 4 Thèmes Annexe A
    elems.append(mk_rect(f"s{n}_th", n, 960, 85, 900, 280, bg="#1b5e20", stroke="#66bb6a"))
    elems.append(mk_text(f"s{n}_th_t", n, 970, 92, 880, 35,
        "4 Thèmes de l'Annexe A", size=20, color="#a5d6a7"))
    elems.append(mk_text(f"s{n}_th_c", n, 970, 130, 880, 220,
        "ORGANISATION   (A.5-A.8)  : Politiques, Org., RH, Actifs\n"
        "ACCES & CRYPTO  (A.9-A.10): Controle acces, Cryptographie\n"
        "PHYSIQUE & EXPL (A.11-A.14): Securite physique, Exploitation\n"
        "INCIDENTS & CONF(A.15-A.18): Fournisseurs, Incidents, Conformite",
        size=16, color="#e8f5e9"))

    # 3 Preuves incontournables
    elems.append(mk_rect(f"s{n}_pr", n, 60, 385, 880, 250, bg="#e65100", stroke="#ffa726"))
    elems.append(mk_text(f"s{n}_pr_t", n, 70, 392, 860, 35,
        "3 Preuves d'audit incontournables", size=20, color="#ffe082"))
    elems.append(mk_text(f"s{n}_pr_c", n, 70, 430, 860, 190,
        "1. POLITIQUES DOCUMENTEES\n   Politiques signees, datees, avec historique des versions\n\n"
        "2. LOGS ET TRACES\n   Journaux systemes, acces, incidents (conservation 12 mois)\n\n"
        "3. RAPPORTS DE TESTS\n   Tests de restauration, pentests, audits internes, exercices PCA",
        size=15, color="#fff8e1"))

    # 5 Outils essentiels
    elems.append(mk_rect(f"s{n}_ot", n, 960, 385, 900, 250, bg="#4a148c", stroke="#ce93d8"))
    elems.append(mk_text(f"s{n}_ot_t", n, 970, 392, 880, 35,
        "5 Outils à avoir absolument", size=20, color="#e1bee7"))
    elems.append(mk_text(f"s{n}_ot_c", n, 970, 430, 880, 190,
        "1. ANTIVIRUS / EDR     : CrowdStrike, SentinelOne, MS Defender\n"
        "2. SIEM                : Splunk, Wazuh, QRadar, MS Sentinel\n"
        "3. SAUVEGARDE          : Veeam (strategie 3-2-1)\n"
        "4. SCANNER VULNS       : Qualys, Tenable Nessus, Greenbone\n"
        "5. GESTION MFA         : Duo, Microsoft Authenticator, Yubikey",
        size=15, color="#f3e5f5"))

    # Footer
    elems.append(mk_rect(f"s{n}_foot", n, 60, 655, 1800, 390, bg="#102027", stroke="#546e7a"))
    elems.append(mk_text(f"s{n}_foot_t", n, 70, 665, 1780, 35,
        "Checklist d'audit ISO 27001 – Points de contrôle essentiels", size=20, color="#4fc3f7"))
    elems.append(mk_text(f"s{n}_foot_c", n, 70, 705, 875, 325,
        "[ ] Politique SMSI signée et datée par la direction\n"
        "[ ] Domaine d'application documenté et approuvé\n"
        "[ ] Analyse des risques réalisée (méthodo documentée)\n"
        "[ ] Déclaration d'Applicabilité (DdA) à jour\n"
        "[ ] Plan de traitement des risques (PTR) validé\n"
        "[ ] Programme de sensibilisation actif (taux >90%)\n"
        "[ ] Audits internes réalisés (programme annuel)\n"
        "[ ] Revue de direction documentée (PV signé)\n"
        "[ ] Non-conformités traitées avec actions correctives",
        size=15, color="#b0bec5"))
    elems.append(mk_text(f"s{n}_foot_c2", n, 965, 705, 875, 325,
        "[ ] MFA activé sur tous les accès distants (taux >95%)\n"
        "[ ] Sauvegardes testées (restauration documentée)\n"
        "[ ] Vulnérabilités scannées et patchées dans les délais\n"
        "[ ] Inventaire des actifs à jour (couverture >98%)\n"
        "[ ] Droits d'accès revus trimestriellement\n"
        "[ ] Journaux de sécurité centralisés et conservés 12 mois\n"
        "[ ] PCA/PRA testé annuellement\n"
        "[ ] Contrats fournisseurs avec clauses sécurité\n"
        "[ ] Registre des incidents tenu à jour",
        size=15, color="#b0bec5"))

    return elems

# Build all elements
all_elements = []

# Generate control slides
for (slide_num, title, controls) in slides_data:
    all_elements.extend(mk_control_slide(slide_num, title, controls))

# Slides 17 & 18
all_elements.extend(mk_slide17())
all_elements.extend(mk_slide18())

# Load existing file and merge
with open("/home/user/CyberResilience-/ISO27001_Presentation.excalidraw", "r") as f:
    existing = json.load(f)

existing["elements"].extend(all_elements)

with open("/home/user/CyberResilience-/ISO27001_Presentation.excalidraw", "w", encoding="utf-8") as f:
    json.dump(existing, f, ensure_ascii=False, indent=2)

print(f"Done! Total elements: {len(existing['elements'])}")
print(f"Slides generated: 1-18")
