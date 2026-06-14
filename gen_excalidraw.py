#!/usr/bin/env python3
import json

elements = []
el_counter = [1]
seed_counter = [100001]

def next_id():
    id_str = f"el_{el_counter[0]:03d}"
    el_counter[0] += 1
    return id_str

def next_seed():
    s = seed_counter[0]
    seed_counter[0] += 1
    return s

def make_frame(frame_num):
    x = (frame_num - 1) * 2020
    return {
        "id": f"frame_{frame_num}",
        "type": "frame",
        "x": x,
        "y": 0,
        "width": 1920,
        "height": 1080,
        "angle": 0,
        "strokeColor": "#4fc3f7",
        "backgroundColor": "#1a237e",
        "fillStyle": "solid",
        "strokeWidth": 2,
        "strokeStyle": "solid",
        "roughness": 0,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": None,
        "seed": next_seed(),
        "version": 1,
        "versionNonce": 1,
        "isDeleted": False,
        "boundElements": None,
        "updated": 1,
        "link": None,
        "locked": False,
        "name": f"Slide {frame_num}"
    }

def make_rect(frame_id, frame_x, local_x, y, w, h, bg_color, stroke_color="#4fc3f7"):
    return {
        "id": next_id(),
        "type": "rectangle",
        "x": frame_x + local_x,
        "y": y,
        "width": w,
        "height": h,
        "angle": 0,
        "strokeColor": stroke_color,
        "backgroundColor": bg_color,
        "fillStyle": "solid",
        "strokeWidth": 2,
        "strokeStyle": "solid",
        "roughness": 0,
        "opacity": 100,
        "groupIds": [],
        "frameId": frame_id,
        "roundness": {"type": 3},
        "seed": next_seed(),
        "version": 1,
        "versionNonce": 1,
        "isDeleted": False,
        "boundElements": None,
        "updated": 1,
        "link": None,
        "locked": False
    }

def make_text(frame_id, frame_x, local_x, y, w, h, text, font_size, color="#ffffff", align="left"):
    return {
        "id": next_id(),
        "type": "text",
        "x": frame_x + local_x,
        "y": y,
        "width": w,
        "height": h,
        "angle": 0,
        "strokeColor": color,
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 1,
        "strokeStyle": "solid",
        "roughness": 0,
        "opacity": 100,
        "groupIds": [],
        "frameId": frame_id,
        "roundness": None,
        "seed": next_seed(),
        "version": 1,
        "versionNonce": 1,
        "isDeleted": False,
        "boundElements": None,
        "updated": 1,
        "link": None,
        "locked": False,
        "text": text,
        "fontSize": font_size,
        "fontFamily": 1,
        "textAlign": align,
        "verticalAlign": "top",
        "containerId": None,
        "originalText": text,
        "lineHeight": 1.25
    }

def add_control_boxes(frame_id, frame_x, title, controls, y_start=120, box_h=190, gap=10):
    """Add title and control boxes for detail slides."""
    # Title
    elements.append(make_rect(frame_id, frame_x, 60, 20, 1800, 80, "#1565c0"))
    elements.append(make_text(frame_id, frame_x, 70, 30, 1780, 60, title, 28, "#ffffff"))

    for i, ctrl in enumerate(controls):
        col = i % 2
        row = i // 2
        col_x = 60 if col == 0 else 970
        box_w = 890
        y = y_start + row * (box_h + gap)

        name = ctrl[0]
        outil = ctrl[1]
        mesure = ctrl[2]
        controle = ctrl[3]

        # Header rect
        elements.append(make_rect(frame_id, frame_x, col_x, y, box_w, 45, "#1565c0"))
        elements.append(make_text(frame_id, frame_x, col_x + 8, y + 8, box_w - 16, 30, name, 16, "#ffffff"))

        # Body rect
        body_h = box_h - 45
        elements.append(make_rect(frame_id, frame_x, col_x, y + 45, box_w, body_h, "#263238"))

        body_text = f"OUTIL: {outil}\nMESURE: {mesure}\nCONTROLE: {controle}"
        elements.append(make_text(frame_id, frame_x, col_x + 8, y + 50, box_w - 16, body_h - 10, body_text, 13, "#e3f2fd"))


# ── SLIDE 1 ──────────────────────────────────────────────────────────────────
fn = 1; fx = 0; fid = f"frame_{fn}"
elements.append(make_frame(fn))
elements.append(make_rect(fid, fx, 60, 30, 1800, 120, "#1565c0"))
elements.append(make_text(fid, fx, 70, 45, 1780, 80,
    "ISO/IEC 27001:2022 – Système de Management de la Sécurité de l'Information", 48, "#ffffff"))
elements.append(make_text(fid, fx, 70, 135, 1780, 40,
    "Structure des 7 clauses principales (4 à 10) – Cycle PDCA", 28, "#4fc3f7"))

plan_text = "PLAN\nClauses 4-6\n• Clause 4: Contexte\n• Clause 5: Leadership\n• Clause 6: Planification\n• Analyse des risques\n• Objectifs sécurité"
do_text = "DO\nClauses 7-8\n• Clause 7: Support\n• Clause 8: Opérations\n• Mise en œuvre\n• Contrôles Annexe A\n• Formation & sensibilisation"
check_text = "CHECK\nClause 9\n• Clause 9: Évaluation\n• Surveillance continue\n• Audit interne\n• Revue de direction\n• Métriques de performance"
act_text = "ACT\nClause 10\n• Clause 10: Amélioration\n• Non-conformités\n• Actions correctives\n• Amélioration continue\n• Boucle de retour"

for lx, bg, txt in [(60, "#0d47a1", plan_text), (520, "#263238", do_text),
                     (980, "#0d47a1", check_text), (1440, "#263238", act_text)]:
    elements.append(make_rect(fid, fx, lx, 220, 440, 380, bg))
    elements.append(make_text(fid, fx, lx+10, 230, 420, 360, txt, 18, "#e3f2fd"))

bottom_text = ("ANNEXE A – 93 Contrôles en 4 thèmes:\n"
               "A.5 Contrôles organisationnels (37) | A.6 Contrôles liés aux personnes (8) | "
               "A.7 Contrôles physiques (14) | A.8 Contrôles technologiques (34)\n"
               "Chaque contrôle inclut: OUTIL (solution technique) | MESURE (KPI/métrique) | CONTRÔLE (preuve d'audit)")
elements.append(make_rect(fid, fx, 60, 630, 1800, 400, "#263238"))
elements.append(make_text(fid, fx, 70, 640, 1780, 380, bottom_text, 18, "#e3f2fd"))


# ── SLIDE 2 ──────────────────────────────────────────────────────────────────
fn = 2; fx = 2020; fid = f"frame_{fn}"
elements.append(make_frame(fn))
elements.append(make_rect(fid, fx, 60, 20, 1800, 80, "#1565c0"))
elements.append(make_text(fid, fx, 70, 35, 1780, 60, "ANNEXE A – Vue d'ensemble des 93 contrôles", 32, "#ffffff"))

col1_text = ("A.5 – ORGANISATIONNELS (37)\n\nA.5.1 Politiques de sécurité\nA.5.2 Rôles et responsabilités\n"
             "A.5.3 Séparation des tâches\nA.5.4 Responsabilités de la direction\nA.5.5 Autorités compétentes\n"
             "A.5.6 Groupes d'intérêt spéciaux\nA.5.7 Threat intelligence\nA.5.8 Sécurité dans les projets\n"
             "A.5.9 Inventaire des actifs\nA.5.10 Utilisation acceptable\nA.5.11 Restitution des actifs\n"
             "A.5.12 Classification\nA.5.13 Étiquetage\nA.5.14 Transfert d'information\n"
             "A.5.15 Contrôle d'accès\nA.5.16 Gestion des identités\nA.5.17 Authentification\n"
             "A.5.18 Droits d'accès\nA.5.19 Sécurité fournisseurs\nA.5.20 Accords fournisseurs\n"
             "A.5.21 Chaîne d'approvisionnement\nA.5.22 Surveillance fournisseurs\nA.5.23 Cloud\n"
             "A.5.24 Gestion des incidents\nA.5.25 Évaluation des incidents\nA.5.26 Réponse aux incidents\n"
             "A.5.27 Leçons apprises\nA.5.28 Collecte de preuves\nA.5.29 Continuité\n"
             "A.5.30 Continuité TIC\nA.5.31 Exigences légales\nA.5.32 DPI\nA.5.33 Protection des données\n"
             "A.5.34 Vie privée\nA.5.35 Revue indépendante\nA.5.36 Conformité aux politiques\n"
             "A.5.37 Procédures opérationnelles")

col2_text = ("A.6 – PERSONNES (8)\n\nA.6.1 Filtrage\nA.6.2 Conditions d'emploi\nA.6.3 Sensibilisation\n"
             "A.6.4 Processus disciplinaire\nA.6.5 Fin de contrat\nA.6.6 Confidentialité\n"
             "A.6.7 Travail à distance\nA.6.8 Signalement des événements")

col3_text = ("A.7 – PHYSIQUES (14)\n\nA.7.1 Périmètres physiques\nA.7.2 Entrée physique\n"
             "A.7.3 Sécurité des bureaux\nA.7.4 Surveillance physique\n"
             "A.7.5 Protection contre menaces physiques\nA.7.6 Travail en zone sécurisée\n"
             "A.7.7 Bureau propre\nA.7.8 Emplacement équipements\nA.7.9 Sécurité hors site\n"
             "A.7.10 Supports de stockage\nA.7.11 Services généraux\nA.7.12 Câblage\n"
             "A.7.13 Maintenance\nA.7.14 Mise au rebut")

col4_text = ("A.8 – TECHNOLOGIQUES (34)\n\nA.8.1 Terminaux utilisateurs\nA.8.2 Privilèges\n"
             "A.8.3 Restriction d'accès\nA.8.4 Code source\nA.8.5 Authentification sécurisée\n"
             "A.8.6 Capacité\nA.8.7 Protection malware\nA.8.8 Vulnérabilités\nA.8.9 Configuration\n"
             "A.8.10 Suppression information\nA.8.11 Masquage données\nA.8.12 DLP\n"
             "A.8.13 Sauvegarde\nA.8.14 Redondance\nA.8.15 Journalisation\nA.8.16 Surveillance\n"
             "A.8.17 Synchronisation horloges\nA.8.18 Outils admin privilégiés\n"
             "A.8.19 Installation logiciels\nA.8.20 Sécurité réseaux\nA.8.21 Filtrage services réseau\n"
             "A.8.22 Cloisonnement réseaux\nA.8.23 Filtrage web\nA.8.24 Cryptographie\n"
             "A.8.25 Dev sécurisé\nA.8.26 Exigences sécurité\nA.8.27 Architecture sécurisée\n"
             "A.8.28 Codage sécurisé\nA.8.29 Tests sécurité\nA.8.30 Sous-traitance dev\n"
             "A.8.31 Séparation dev/prod\nA.8.32 Gestion changements\nA.8.33 Tests\n"
             "A.8.34 Protection systèmes en audit")

for lx, w, txt in [(60, 430, col1_text), (510, 430, col2_text), (960, 430, col3_text), (1410, 490, col4_text)]:
    elements.append(make_rect(fid, fx, lx, 120, w, 920, "#263238"))
    elements.append(make_text(fid, fx, lx+8, 128, w-16, 904, txt, 13, "#e3f2fd"))


# ── SLIDE 3 ──────────────────────────────────────────────────────────────────
fn = 3; fx = 4040; fid = f"frame_{fn}"
elements.append(make_frame(fn))
controls_3 = [
    ("A.5.1 – Politiques SI", "Confluence/SharePoint", "Taux de révision annuelle des politiques", "Politique signée, journal de révision"),
    ("A.5.2 – Rôles et responsabilités", "RACI Matrix/Organigramme", "% rôles documentés", "Fiches de poste, matrice RACI"),
    ("A.5.3 – Séparation des tâches", "IAM (Azure AD/Okta)", "% conflits de droits résolus", "Matrice SoD, revue accès"),
    ("A.5.4 – Responsabilités direction", "Tableau de bord gouvernance", "Nb réunions COMEX sécurité/an", "PV de réunion, engagement signé"),
    ("A.5.5 – Autorités compétentes", "Registre des contacts réglementaires", "Délai notification incident", "Liste contacts, log notifications"),
    ("A.5.6 – Groupes d'intérêt", "ISAC/CERT abonnements", "Nb alertes traitées/mois", "Abonnements actifs, rapports threat intel"),
    ("A.5.7 – Threat intelligence", "MISP/ThreatConnect", "Nb IoC intégrés/semaine", "Rapports TI, règles SIEM mises à jour"),
    ("A.5.8 – Sécurité dans les projets", "JIRA Security Gates", "% projets avec analyse sécurité", "Checklist sécurité projets, PIA"),
    ("A.5.9 – Inventaire des actifs", "ServiceNow CMDB/Lansweeper", "% actifs inventoriés", "Export CMDB, rapport de couverture"),
    ("A.5.10 – Utilisation acceptable", "DLP/Proxy/MDM", "Nb violations politique/mois", "Politique signée, logs DLP"),
]
add_control_boxes(fid, fx, "A.5 – Contrôles organisationnels (1/3)", controls_3)


# ── SLIDE 4 ──────────────────────────────────────────────────────────────────
fn = 4; fx = 6060; fid = f"frame_{fn}"
elements.append(make_frame(fn))
controls_4 = [
    ("A.5.11 – Restitution des actifs", "ITSM Offboarding workflow", "% actifs restitués à J0 départ", "Checklist offboarding signée"),
    ("A.5.12 – Classification info", "Microsoft Purview/Titus", "% documents classifiés", "Taxonomie, rapport classification"),
    ("A.5.13 – Étiquetage", "Azure Information Protection", "% fichiers étiquetés", "Labels appliqués, rapport AIP"),
    ("A.5.14 – Transfert information", "SFTP sécurisé/DLP email", "Nb transferts non conformes", "Accords NDA, logs transferts"),
    ("A.5.15 – Contrôle d'accès", "IAM/PAM (CyberArk)", "% comptes avec revue trimestrielle", "Politique accès, rapport revue"),
    ("A.5.16 – Gestion identités", "Active Directory/Okta", "Délai désactivation compte ex-employé", "Log AD, tickets offboarding"),
    ("A.5.17 – Authentification", "MFA (Duo/Azure MFA)", "% comptes avec MFA activé", "Rapport MFA, politique mdp"),
    ("A.5.18 – Droits d'accès", "SailPoint/Saviynt", "Nb accès orphelins détectés", "Rapport IGA, certification accès"),
    ("A.5.19 – Sécurité fournisseurs", "Questionnaire sécurité/TPRM", "% fournisseurs évalués/an", "Questionnaires complétés, scores"),
    ("A.5.20 – Accords fournisseurs", "CLM (ContractPodAi)", "% contrats avec clauses sécurité", "Contrats signés, SLA sécurité"),
]
add_control_boxes(fid, fx, "A.5 – Contrôles organisationnels (2/3)", controls_4)


# ── SLIDE 5 ──────────────────────────────────────────────────────────────────
fn = 5; fx = 8080; fid = f"frame_{fn}"
elements.append(make_frame(fn))
controls_5 = [
    ("A.5.21 – Chaîne approvisionnement", "SBOM/Dependency-Track", "Nb vulns supply chain détectées", "SBOM, rapports scan dépendances"),
    ("A.5.22 – Surveillance fournisseurs", "BitSight/SecurityScorecard", "Score moyen fournisseurs", "Rapports scoring, PV audits tiers"),
    ("A.5.23 – Cloud", "CASB/CSPM (Prisma Cloud)", "Nb dérives config cloud", "Rapport CSPM, politiques cloud"),
    ("A.5.24 – Gestion incidents", "TheHive/ServiceNow SecOps", "MTTD/MTTR incidents", "Plan réponse, playbooks incidents"),
    ("A.5.25 – Évaluation incidents", "SIEM (Splunk/Microsoft Sentinel)", "% incidents correctement classifiés", "Log incidents, matrice classification"),
    ("A.5.26 – Réponse incidents", "SOAR (Palo Alto XSOAR)", "Délai confinement moyen", "Rapports post-mortem, playbooks"),
    ("A.5.27 – Leçons apprises", "Confluence/Wiki", "Nb recommandations implémentées", "Rapports PIR, plan d'actions"),
    ("A.5.28 – Collecte preuves", "Forensic tools (FTK/Velociraptor)", "% incidents avec preuves collectées", "Chain of custody, rapports forensic"),
    ("A.5.29 – Continuité SI", "BCP/Plan continuité", "RTO/RPO atteints lors des tests", "Plan continuité, PV test BCP"),
    ("A.5.30 – Continuité TIC", "DR platform (Zerto/Veeam)", "RPO/RTO infrastructure", "Plan DR, rapports test failover"),
]
add_control_boxes(fid, fx, "A.5 – Contrôles organisationnels (3/3)", controls_5)


# ── SLIDE 6 ──────────────────────────────────────────────────────────────────
fn = 6; fx = 10100; fid = f"frame_{fn}"
elements.append(make_frame(fn))
controls_6 = [
    ("A.6.1 – Filtrage", "Prestataire vérification antécédents", "% employés vérifiés avant embauche", "Rapports vérification, politique filtrage"),
    ("A.6.2 – Conditions d'emploi", "SIRH/DocuSign", "% contrats avec clauses sécurité signés", "Contrats signés, chartes utilisateur"),
    ("A.6.3 – Sensibilisation formation", "KnowBe4/Proofpoint SAT", "Taux completion formations/taux clic phishing", "Rapports formation, certificats"),
    ("A.6.4 – Processus disciplinaire", "RH/Système gestion disciplinaire", "Nb incidents avec suites disciplinaires", "Procédure disciplinaire, PV RH"),
    ("A.6.5 – Fin de contrat", "ITSM Offboarding (ServiceNow)", "Délai révocation accès à J0", "Checklist offboarding, tickets ITSM"),
    ("A.6.6 – Confidentialité", "DocuSign/ContractPodAi", "% accords NDA signés", "NDA signés, registre confidentialité"),
    ("A.6.7 – Travail à distance", "VPN/MDM/Zero Trust (Zscaler)", "% télétravailleurs avec poste conforme", "Politique télétravail, rapports conformité MDM"),
    ("A.6.8 – Signalement événements", "Portail signalement/SIEM", "Nb événements signalés/mois", "Procédure signalement, log incidents"),
]
add_control_boxes(fid, fx, "A.6 – Contrôles liés aux personnes (8 contrôles)", controls_6)


# ── SLIDE 7 ──────────────────────────────────────────────────────────────────
fn = 7; fx = 12120; fid = f"frame_{fn}"
elements.append(make_frame(fn))
controls_7 = [
    ("A.7.1 – Périmètres physiques", "Contrôle accès (Lenel/Genetec)", "Nb tentatives accès non autorisé", "Logs badgeuse, rapports intrusion"),
    ("A.7.2 – Entrée physique", "Sas sécurisé/Biométrie", "% visiteurs enregistrés", "Registre visiteurs, logs accès"),
    ("A.7.3 – Sécurité bureaux", "Badge access/Serrures électroniques", "% zones sensibles avec contrôle accès", "Plan sécurité physique, audits locaux"),
    ("A.7.4 – Surveillance physique", "CCTV/Vidéosurveillance", "% zones couvertes par caméras", "Plan caméras, logs enregistrements"),
    ("A.7.5 – Menaces physiques", "Détecteurs incendie/eau/onduleurs", "Nb tests alarmes/an", "Rapports tests, certificats maintenance"),
    ("A.7.6 – Travail zone sécurisée", "Politique zone sécurisée", "Nb violations procédures zones sécurisées", "Procédures affichées, registre accès"),
    ("A.7.7 – Bureau propre", "Politique clean desk/Chiffrement poste", "% audits clean desk conformes", "Rapports audit physique, politique affichée"),
]
add_control_boxes(fid, fx, "A.7 – Contrôles physiques (1/2)", controls_7)


# ── SLIDE 8 ──────────────────────────────────────────────────────────────────
fn = 8; fx = 14140; fid = f"frame_{fn}"
elements.append(make_frame(fn))
controls_8 = [
    ("A.7.8 – Emplacement équipements", "DCIM (Data Center Infra Mgmt)", "% équipements dans zones approuvées", "Plan d'implantation, DCIM export"),
    ("A.7.9 – Sécurité hors site", "Politique actifs mobiles/MDM", "% actifs mobiles chiffrés", "Politique transport, rapports MDM"),
    ("A.7.10 – Supports de stockage", "Inventaire médias/Chiffrement", "% médias chiffrés et inventoriés", "Registre médias, certificats destruction"),
    ("A.7.11 – Services généraux", "UPS/Générateurs/Monitoring", "Disponibilité alimentation (%)", "Rapports maintenance, SLA services"),
    ("A.7.12 – Câblage", "Gestion câblage structuré", "% câbles étiquetés et documentés", "Plan réseau physique, audits câblage"),
    ("A.7.13 – Maintenance équipements", "GMAO (CMMS)/Contrats maintenance", "% maintenances préventives réalisées", "Planning maintenance, rapports interventions"),
    ("A.7.14 – Mise au rebut", "Outil effacement (Blancco)/Prestataire", "% équipements avec certificat destruction", "Certificats de destruction, registre rebut"),
]
add_control_boxes(fid, fx, "A.7 – Contrôles physiques (2/2)", controls_8)


# ── SLIDE 9 ──────────────────────────────────────────────────────────────────
fn = 9; fx = 16160; fid = f"frame_{fn}"
elements.append(make_frame(fn))
controls_9 = [
    ("A.8.1 – Terminaux utilisateurs", "MDM (Intune/Jamf)/EDR", "% terminaux gérés et conformes", "Rapports MDM, politique terminaux"),
    ("A.8.2 – Privilèges", "PAM (CyberArk/BeyondTrust)", "Nb comptes privilegiés actifs", "Rapport PAM, politique moindre privilège"),
    ("A.8.3 – Restriction d'accès", "IAM/RBAC/ABAC", "% accès conformes au profil métier", "Matrice droits, rapport revue accès"),
    ("A.8.4 – Code source", "GitHub/GitLab avec contrôle accès", "% repos avec accès restreint", "Politique gestion code, rapport accès SCM"),
    ("A.8.5 – Authentification sécurisée", "MFA + SSO (Okta/Azure AD)", "% systèmes avec MFA activé", "Rapport authentification, politique MFA"),
    ("A.8.6 – Capacité", "Monitoring (Datadog/Zabbix)", "% alertes capacité traitées sous 4h", "Rapports capacité, seuils définis"),
    ("A.8.7 – Protection malware", "EDR (CrowdStrike/SentinelOne)", "Taux détection malware", "Rapport EDR, politique antimalware"),
    ("A.8.8 – Vulnérabilités", "Tenable/Qualys/Rapid7", "Délai moyen correction CVE critique", "Rapports scan vuln, patch management"),
    ("A.8.9 – Configuration", "Ansible/Chef/CIS-CAT", "% systèmes conformes baseline", "Baseline configs, rapports CIS Benchmark"),
    ("A.8.10 – Suppression information", "Blancco/Shred-it", "% données supprimées selon procédure", "Certificats effacement, politique rétention"),
]
add_control_boxes(fid, fx, "A.8 – Contrôles technologiques (1/3)", controls_9)


# ── SLIDE 10 ─────────────────────────────────────────────────────────────────
fn = 10; fx = 18180; fid = f"frame_{fn}"
elements.append(make_frame(fn))
controls_10 = [
    ("A.8.11 – Masquage données", "Data masking (Delphix/IBM Optim)", "% données sensibles masquées en dev/test", "Rapport masquage, politique données de test"),
    ("A.8.12 – DLP", "Microsoft Purview DLP/Symantec DLP", "Nb incidents DLP/mois", "Rapport DLP, règles configurées"),
    ("A.8.13 – Sauvegarde", "Veeam/Commvault/AWS Backup", "% sauvegardes réussies/taux restauration", "Rapports sauvegarde, tests restauration"),
    ("A.8.14 – Redondance", "Load Balancer/HA Cluster", "Disponibilité services critiques (%)", "Architecture HA, tests failover"),
    ("A.8.15 – Journalisation", "SIEM (Splunk/Microsoft Sentinel)", "% systèmes avec logs collectés", "Politique logs, rapport couverture SIEM"),
    ("A.8.16 – Surveillance", "SOC/SIEM/NTA (Darktrace)", "Délai détection anomalies", "Rapports SOC, alertes traitées"),
    ("A.8.17 – Synchronisation horloges", "NTP/PTP synchronisé", "% systèmes synchronisés NTP", "Config NTP, rapport synchronisation"),
    ("A.8.18 – Outils admin privilégiés", "PAM + Journalisation sessions", "% sessions admin enregistrées", "Logs sessions PAM, politique outils admin"),
    ("A.8.19 – Installation logiciels", "Software deployment (SCCM/Intune)", "% logiciels non autorisés détectés", "Whitelist logiciels, rapports SCCM"),
    ("A.8.20 – Sécurité réseaux", "Firewall NGFW (Palo Alto/Fortinet)", "Nb règles firewall non conformes", "Politique réseau, audit règles FW"),
]
add_control_boxes(fid, fx, "A.8 – Contrôles technologiques (2/3)", controls_10)


# ── SLIDE 11 ─────────────────────────────────────────────────────────────────
fn = 11; fx = 20200; fid = f"frame_{fn}"
elements.append(make_frame(fn))
controls_11 = [
    ("A.8.21 – Filtrage services réseau", "WAF/Proxy/IPS", "Nb attaques bloquées/jour", "Rapport WAF/IPS, règles filtrage"),
    ("A.8.22 – Cloisonnement réseaux", "VLAN/Micro-segmentation (NSX)", "Nb flux non autorisés inter-zones", "Plan segmentation, audit flux réseau"),
    ("A.8.23 – Filtrage web", "Proxy web (Zscaler/BlueCoat)", "Nb sites bloqués/catégories", "Politique navigation, rapports proxy"),
    ("A.8.24 – Cryptographie", "PKI/HSM/KMS (AWS KMS)", "% données sensibles chiffrées", "Politique crypto, inventaire certificats"),
    ("A.8.25 – Dev sécurisé", "DevSecOps pipeline/SAST (SonarQube)", "Nb vulns code détectées/sprint", "Politique dev sécurisé, rapports SAST"),
    ("A.8.26 – Exigences sécurité", "Threat modeling (STRIDE/IriusRisk)", "% US avec exigences sécurité", "Threat models, exigences documentées"),
    ("A.8.27 – Architecture sécurisée", "Architecture review board", "% projets avec revue architecture", "Rapports ARB, patterns sécurité"),
    ("A.8.28 – Codage sécurisé", "SAST/DAST (Veracode/Checkmarx)", "Densité de vulns/KLOC", "Rapports SAST/DAST, standards codage"),
    ("A.8.29 – Tests sécurité", "Pentest/OWASP ZAP/Burp Suite", "Nb vulns critiques corrigées post-pentest", "Rapports pentest, plans de remédiation"),
    ("A.8.30 – Sous-traitance dev", "Audit code/Clauses contractuelles", "% sous-traitants avec audit sécurité", "Contrats dev, rapports audit code tiers"),
    ("A.8.31 – Séparation dev/prod", "Environnements séparés/CI-CD gates", "Nb déploiements directs en prod", "Pipeline CI/CD, règles promotion env"),
    ("A.8.32 – Gestion changements", "ITSM Change Management (ServiceNow)", "% changements avec CAB approuvé", "Tickets changement, PV CAB"),
    ("A.8.33 – Test information", "Données de test synthétiques", "% tests avec données masquées", "Politique données test, rapports masquage"),
    ("A.8.34 – Protection systèmes en audit", "Isolation outils audit/Read-only access", "Nb incidents pendant audits", "Procédure audit, accès temporaires journalisés"),
]
add_control_boxes(fid, fx, "A.8 – Contrôles technologiques (3/3)", controls_11, box_h=140)


# ── SLIDE 12 ─────────────────────────────────────────────────────────────────
fn = 12; fx = 22220; fid = f"frame_{fn}"
elements.append(make_frame(fn))
elements.append(make_rect(fid, fx, 60, 20, 1800, 80, "#1565c0"))
elements.append(make_text(fid, fx, 70, 35, 1780, 60, "Clauses 4 & 5 – Contexte et Leadership", 32, "#ffffff"))

elements.append(make_rect(fid, fx, 60, 120, 1800, 50, "#0d47a1"))
elements.append(make_text(fid, fx, 70, 128, 1780, 40, "CLAUSE 4 – CONTEXTE DE L'ORGANISATION", 24, "#4fc3f7"))

controls_c4 = [
    ("4.1 – Compréhension de l'organisation", "Analyse SWOT/PESTEL", "Nb enjeux identifiés et mis à jour", "Registre enjeux, comptes-rendus revue"),
    ("4.2 – Parties intéressées", "Registre parties prenantes", "Nb exigences parties prenantes documentées", "Registre PI, matrice exigences"),
    ("4.3 – Domaine d'application", "Document périmètre SMSI", "% actifs dans le périmètre documentés", "Déclaration d'applicabilité (SoA)"),
    ("4.4 – SMSI", "Plateforme GRC (ServiceNow/Archer)", "% processus SMSI opérationnels", "Procédures SMSI, cartographie processus"),
]
for i, ctrl in enumerate(controls_c4):
    col = i % 2; row = i // 2
    col_x = 60 if col == 0 else 970
    y = 180 + row * 170
    name, outil, mesure, controle = ctrl
    elements.append(make_rect(fid, fx, col_x, y, 890, 45, "#1565c0"))
    elements.append(make_text(fid, fx, col_x+8, y+8, 874, 30, name, 16, "#ffffff"))
    elements.append(make_rect(fid, fx, col_x, y+45, 890, 115, "#263238"))
    elements.append(make_text(fid, fx, col_x+8, y+50, 874, 105,
        f"OUTIL: {outil}\nMESURE: {mesure}\nCONTROLE: {controle}", 13, "#e3f2fd"))

elements.append(make_rect(fid, fx, 60, 530, 1800, 50, "#0d47a1"))
elements.append(make_text(fid, fx, 70, 538, 1780, 40, "CLAUSE 5 – LEADERSHIP", 24, "#4fc3f7"))

controls_c5 = [
    ("5.1 – Leadership et engagement", "Comité SMSI/Tableau de bord RSSI", "Nb réunions COMEX sécurité/an", "PV réunions, budget sécurité approuvé"),
    ("5.2 – Politique de sécurité", "Confluence/SharePoint", "Date dernière révision politique", "Politique signée DG, diffusion employés"),
    ("5.3 – Rôles et responsabilités", "Matrice RACI", "% rôles sécurité formellement assignés", "Fiches de poste, organigramme sécurité"),
]
for i, ctrl in enumerate(controls_c5):
    col = i % 2; row = i // 2
    col_x = 60 if col == 0 else 970
    y = 590 + row * 170
    name, outil, mesure, controle = ctrl
    elements.append(make_rect(fid, fx, col_x, y, 890, 45, "#1565c0"))
    elements.append(make_text(fid, fx, col_x+8, y+8, 874, 30, name, 16, "#ffffff"))
    elements.append(make_rect(fid, fx, col_x, y+45, 890, 115, "#263238"))
    elements.append(make_text(fid, fx, col_x+8, y+50, 874, 105,
        f"OUTIL: {outil}\nMESURE: {mesure}\nCONTROLE: {controle}", 13, "#e3f2fd"))


# ── SLIDE 13 ─────────────────────────────────────────────────────────────────
fn = 13; fx = 24240; fid = f"frame_{fn}"
elements.append(make_frame(fn))
elements.append(make_rect(fid, fx, 60, 20, 1800, 80, "#1565c0"))
elements.append(make_text(fid, fx, 70, 35, 1780, 60, "Clause 6 – Planification", 32, "#ffffff"))
elements.append(make_rect(fid, fx, 60, 120, 1800, 50, "#0d47a1"))
elements.append(make_text(fid, fx, 70, 128, 1780, 40, "CLAUSE 6 – PLANIFICATION", 24, "#4fc3f7"))

controls_c6 = [
    ("6.1.1 – Généralités risques/opportunités", "GRC Platform", "Nb risques évalués/traités", "Registre des risques, plan de traitement"),
    ("6.1.2 – Appréciation des risques", "EBIOS RM/ISO 27005/Archer", "Nb risques réévalués/an", "Rapport d'analyse des risques"),
    ("6.1.3 – Traitement des risques", "Plan de traitement (POA&M)", "% risques avec traitement défini", "Plan traitement signé, SoA"),
    ("6.2 – Objectifs de sécurité", "Balanced scorecard sécurité", "% objectifs atteints", "Tableau de bord, rapport objectifs"),
    ("6.3 – Planification des changements", "Change management ITSM", "% changements planifiés formellement", "Registre changements, impact assessments"),
]
for i, ctrl in enumerate(controls_c6):
    col = i % 2; row = i // 2
    col_x = 60 if col == 0 else 970
    y = 180 + row * 170
    name, outil, mesure, controle = ctrl
    elements.append(make_rect(fid, fx, col_x, y, 890, 45, "#1565c0"))
    elements.append(make_text(fid, fx, col_x+8, y+8, 874, 30, name, 16, "#ffffff"))
    elements.append(make_rect(fid, fx, col_x, y+45, 890, 115, "#263238"))
    elements.append(make_text(fid, fx, col_x+8, y+50, 874, 105,
        f"OUTIL: {outil}\nMESURE: {mesure}\nCONTROLE: {controle}", 13, "#e3f2fd"))


# ── SLIDE 14 ─────────────────────────────────────────────────────────────────
fn = 14; fx = 26260; fid = f"frame_{fn}"
elements.append(make_frame(fn))
elements.append(make_rect(fid, fx, 60, 20, 1800, 80, "#1565c0"))
elements.append(make_text(fid, fx, 70, 35, 1780, 60, "Clause 7 – Support", 32, "#ffffff"))
elements.append(make_rect(fid, fx, 60, 120, 1800, 50, "#0d47a1"))
elements.append(make_text(fid, fx, 70, 128, 1780, 40, "CLAUSE 7 – SUPPORT", 24, "#4fc3f7"))

controls_c7 = [
    ("7.1 – Ressources", "Budget/Headcount tracking", "Budget sécurité/CA (%)", "Budget approuvé, plan ressources"),
    ("7.2 – Compétences", "LMS/Matrice compétences", "% personnel certifié", "Matrice compétences, certifications"),
    ("7.3 – Sensibilisation", "KnowBe4/Proofpoint", "Taux completion/taux clic phishing", "Rapports formation, attestations"),
    ("7.4 – Communication", "Plan de communication sécurité", "Nb communications sécurité/an", "Plan comm, preuves diffusion"),
    ("7.5 – Information documentée", "Confluence/SharePoint DMS", "% documents revus dans les délais", "Registre documents, contrôle versions"),
]
for i, ctrl in enumerate(controls_c7):
    col = i % 2; row = i // 2
    col_x = 60 if col == 0 else 970
    y = 180 + row * 170
    name, outil, mesure, controle = ctrl
    elements.append(make_rect(fid, fx, col_x, y, 890, 45, "#1565c0"))
    elements.append(make_text(fid, fx, col_x+8, y+8, 874, 30, name, 16, "#ffffff"))
    elements.append(make_rect(fid, fx, col_x, y+45, 890, 115, "#263238"))
    elements.append(make_text(fid, fx, col_x+8, y+50, 874, 105,
        f"OUTIL: {outil}\nMESURE: {mesure}\nCONTROLE: {controle}", 13, "#e3f2fd"))


# ── SLIDE 15 ─────────────────────────────────────────────────────────────────
fn = 15; fx = 28280; fid = f"frame_{fn}"
elements.append(make_frame(fn))
elements.append(make_rect(fid, fx, 60, 20, 1800, 80, "#1565c0"))
elements.append(make_text(fid, fx, 70, 35, 1780, 60, "Clause 8 – Opérations", 32, "#ffffff"))
elements.append(make_rect(fid, fx, 60, 120, 1800, 50, "#0d47a1"))
elements.append(make_text(fid, fx, 70, 128, 1780, 40, "CLAUSE 8 – OPÉRATIONS", 24, "#4fc3f7"))

controls_c8 = [
    ("8.1 – Planification et contrôle", "ITSM/Procédures opérationnelles", "% processus avec procédures à jour", "Procédures documentées, audits opérationnels"),
    ("8.2 – Appréciation des risques SI", "GRC/EBIOS RM", "Fréquence réévaluation risques", "Rapports d'analyse risques datés"),
    ("8.3 – Traitement des risques SI", "Plan traitement risques/POA&M", "% actions de traitement réalisées", "Plan traitement mis à jour, preuves implémentation"),
]
for i, ctrl in enumerate(controls_c8):
    col = i % 2; row = i // 2
    col_x = 60 if col == 0 else 970
    y = 180 + row * 210
    name, outil, mesure, controle = ctrl
    elements.append(make_rect(fid, fx, col_x, y, 890, 45, "#1565c0"))
    elements.append(make_text(fid, fx, col_x+8, y+8, 874, 30, name, 16, "#ffffff"))
    elements.append(make_rect(fid, fx, col_x, y+45, 890, 155, "#263238"))
    elements.append(make_text(fid, fx, col_x+8, y+50, 874, 145,
        f"OUTIL: {outil}\nMESURE: {mesure}\nCONTROLE: {controle}", 13, "#e3f2fd"))


# ── SLIDE 16 ─────────────────────────────────────────────────────────────────
fn = 16; fx = 30300; fid = f"frame_{fn}"
elements.append(make_frame(fn))
elements.append(make_rect(fid, fx, 60, 20, 1800, 80, "#1565c0"))
elements.append(make_text(fid, fx, 70, 35, 1780, 60, "Clauses 9 & 10 – Évaluation et Amélioration", 32, "#ffffff"))

elements.append(make_rect(fid, fx, 60, 120, 1800, 50, "#0d47a1"))
elements.append(make_text(fid, fx, 70, 128, 1780, 40, "CLAUSE 9 – ÉVALUATION DES PERFORMANCES", 24, "#4fc3f7"))

controls_c9 = [
    ("9.1 – Surveillance et mesures", "SIEM/GRC Dashboard", "% métriques collectées automatiquement", "Tableau de bord KPI, rapports métriques"),
    ("9.2 – Audit interne", "AuditBoard/TeamMate", "% programme d'audit réalisé", "Programme audit, rapports d'audit"),
    ("9.3 – Revue de direction", "Rapport RSSI/Tableau de bord", "Fréquence revues direction (min 1/an)", "PV revue direction, décisions actées"),
]
for i, ctrl in enumerate(controls_c9):
    col = i % 2; row = i // 2
    col_x = 60 if col == 0 else 970
    y = 180 + row * 170
    name, outil, mesure, controle = ctrl
    elements.append(make_rect(fid, fx, col_x, y, 890, 45, "#1565c0"))
    elements.append(make_text(fid, fx, col_x+8, y+8, 874, 30, name, 16, "#ffffff"))
    elements.append(make_rect(fid, fx, col_x, y+45, 890, 115, "#263238"))
    elements.append(make_text(fid, fx, col_x+8, y+50, 874, 105,
        f"OUTIL: {outil}\nMESURE: {mesure}\nCONTROLE: {controle}", 13, "#e3f2fd"))

elements.append(make_rect(fid, fx, 60, 700, 1800, 50, "#0d47a1"))
elements.append(make_text(fid, fx, 70, 708, 1780, 40, "CLAUSE 10 – AMÉLIORATION", 24, "#4fc3f7"))

controls_c10 = [
    ("10.1 – Amélioration continue", "PDCA/Kaizen/Plan d'amélioration", "Nb initiatives amélioration/an", "Plan amélioration, indicateurs tendance"),
    ("10.2 – Non-conformités et actions correctives", "GRC/NCR tracking", "Délai moyen clôture non-conformités", "Registre NC, preuves correction"),
]
for i, ctrl in enumerate(controls_c10):
    col = i % 2; row = i // 2
    col_x = 60 if col == 0 else 970
    y = 760 + row * 170
    name, outil, mesure, controle = ctrl
    elements.append(make_rect(fid, fx, col_x, y, 890, 45, "#1565c0"))
    elements.append(make_text(fid, fx, col_x+8, y+8, 874, 30, name, 16, "#ffffff"))
    elements.append(make_rect(fid, fx, col_x, y+45, 890, 115, "#263238"))
    elements.append(make_text(fid, fx, col_x+8, y+50, 874, 105,
        f"OUTIL: {outil}\nMESURE: {mesure}\nCONTROLE: {controle}", 13, "#e3f2fd"))


# ── SLIDE 17 ─────────────────────────────────────────────────────────────────
fn = 17; fx = 32320; fid = f"frame_{fn}"
elements.append(make_frame(fn))
elements.append(make_rect(fid, fx, 60, 20, 1800, 80, "#1565c0"))
elements.append(make_text(fid, fx, 70, 35, 1780, 60, "Vue d'ensemble des outils par domaine", 32, "#ffffff"))

col1_17 = ("GOUVERNANCE & GRC\n\nGRC Platforms:\n• ServiceNow GRC\n• Archer\n• OneTrust\n• LogicGate\n\n"
           "Risk Management:\n• EBIOS RM\n• Mehari\n• ISO 27005 tools\n\n"
           "Policy Management:\n• Confluence\n• SharePoint\n• DocuSign\n\n"
           "Audit Management:\n• AuditBoard\n• TeamMate\n• MetricStream")
col2_17 = ("SÉCURITÉ TECHNIQUE\n\nIAM/PAM:\n• CyberArk, BeyondTrust\n• SailPoint, Okta, Azure AD\n\n"
           "SIEM/SOC:\n• Splunk\n• Microsoft Sentinel\n• IBM QRadar\n\n"
           "EDR/XDR:\n• CrowdStrike\n• SentinelOne\n• Microsoft Defender\n\n"
           "Vulnerability Mgmt:\n• Tenable, Qualys, Rapid7\n\n"
           "DLP:\n• Microsoft Purview\n• Symantec DLP, Forcepoint\n\n"
           "CASB/CSPM:\n• Prisma Cloud, Wiz, Orca Security")
col3_17 = ("DÉVELOPPEMENT & CLOUD\n\nSAST/DAST:\n• SonarQube, Veracode\n• Checkmarx, OWASP ZAP\n\n"
           "DevSecOps:\n• GitHub Advanced Security\n• GitLab SAST\n\n"
           "Backup/DR:\n• Veeam, Commvault\n• Zerto, AWS Backup\n\n"
           "Threat Intel:\n• MISP, ThreatConnect\n• Recorded Future\n\n"
           "PKI/Crypto:\n• HashiCorp Vault\n• AWS KMS, Azure Key Vault\n\n"
           "MDM:\n• Microsoft Intune\n• Jamf\n• VMware Workspace ONE")

for lx, w, txt in [(60, 580, col1_17), (660, 580, col2_17), (1260, 600, col3_17)]:
    elements.append(make_rect(fid, fx, lx, 120, w, 920, "#263238"))
    elements.append(make_text(fid, fx, lx+8, 128, w-16, 904, txt, 15, "#e3f2fd"))


# ── SLIDE 18 ─────────────────────────────────────────────────────────────────
fn = 18; fx = 34340; fid = f"frame_{fn}"
elements.append(make_frame(fn))
elements.append(make_rect(fid, fx, 60, 20, 1800, 80, "#1565c0"))
elements.append(make_text(fid, fx, 70, 35, 1780, 60, "FEUILLE DE ROUTE ISO 27001:2022", 32, "#ffffff"))

phases = [
    (60, "#0d47a1",
     "PHASE 1 – PLAN\n(0-3 mois)\n\n• Définir le périmètre et\n  le contexte (Clause 4)\n"
     "• Obtenir l'engagement\n  de la direction (Clause 5)\n• Réaliser l'analyse des\n  risques initiale (Clause 6)\n"
     "• Rédiger la politique\n  de sécurité"),
    (510, "#263238",
     "PHASE 2 – DO\n(3-9 mois)\n\n• Déployer les ressources\n  et compétences (Clause 7)\n"
     "• Implémenter les contrôles\n  Annexe A (Clause 8)\n• Former et sensibiliser\n  le personnel\n"
     "• Mettre en oeuvre les\n  outils techniques"),
    (960, "#0d47a1",
     "PHASE 3 – CHECK\n(9-12 mois)\n\n• Réaliser les mesures\n  et surveillances (9.1)\n"
     "• Conduire les audits\n  internes (Clause 9.2)\n• Organiser la revue\n  de direction (9.3)"),
    (1410, "#263238",
     "PHASE 4 – ACT\n(12-18 mois)\n\n• Traiter les\n  non-conformités (10.2)\n"
     "• Amélioration continue\n  (Clause 10.1)\n• Certification par\n  organisme accrédité"),
]
for lx, bg, txt in phases:
    elements.append(make_rect(fid, fx, lx, 120, 430, 380, bg))
    elements.append(make_text(fid, fx, lx+10, 130, 410, 360, txt, 16, "#e3f2fd"))

metrics_text = ("MÉTRIQUES CLÉS\n\n"
                "• Objectif RTO: < 4h pour systèmes critiques\n"
                "• Objectif RPO: < 1h pour données critiques\n"
                "• Taux de correction vulnérabilités critiques: > 95% sous 72h\n"
                "• Taux completion formation sécurité: > 95%\n"
                "• Disponibilité systèmes critiques: > 99.9%")
elements.append(make_rect(fid, fx, 60, 520, 1800, 300, "#263238"))
elements.append(make_text(fid, fx, 70, 530, 1780, 280, metrics_text, 16, "#e3f2fd"))


# ── OUTPUT ────────────────────────────────────────────────────────────────────
output = {
    "type": "excalidraw",
    "version": 2,
    "source": "https://excalidraw.com",
    "elements": elements,
    "appState": {
        "gridSize": None,
        "viewBackgroundColor": "#0d1117"
    },
    "files": {}
}

output_path = "/home/user/CyberResilience-/ISO27001_Presentation.excalidraw"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Generated {len(elements)} elements across 18 slides.")
print(f"Saved to: {output_path}")
