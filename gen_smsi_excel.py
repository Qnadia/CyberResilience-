#!/usr/bin/env python3
"""
Générateur de fichiers Excel SMSI ISO 27001:2022 / Loi 05-20 / DNSSI v2 Maroc
Fichiers générés :
  1. DdA_ISO27001_2022.xlsx          – Déclaration d'Applicabilité (93 contrôles)
  2. Plan_Traitement_Risques.xlsx     – PTR avec évaluation et suivi
  3. Registre_Incidents.xlsx          – Gestion des incidents
  4. Programme_Audit_Interne.xlsx     – Programme et checklist d'audit
  5. Tableau_Bord_SMSI.xlsx           – KPIs et indicateurs de performance
"""

from openpyxl import Workbook
from openpyxl.styles import (
    PatternFill, Font, Alignment, Border, Side, GradientFill
)
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.chart import BarChart, Reference
from openpyxl.chart.series import DataPoint
import openpyxl

# ── Palette couleurs ──────────────────────────────────────────────────────────
NAVY    = "0D1B4B"
BLUE1   = "1565C0"
BLUE2   = "1E88E5"
LBLUE   = "BBDEFB"
GREEN1  = "1B5E20"
GREEN2  = "388E3C"
LGREEN  = "C8E6C9"
ORANGE1 = "E65100"
ORANGE2 = "F57C00"
LORANGE = "FFE0B2"
RED1    = "B71C1C"
LRED    = "FFCDD2"
GREY1   = "37474F"
GREY2   = "546E7A"
LGREY   = "ECEFF1"
WHITE   = "FFFFFF"
YELLOW  = "FFF9C4"
PURPLE  = "4A148C"
LPURPLE = "E1BEE7"

def fill(hex_color):
    return PatternFill("solid", fgColor=hex_color)

def font(bold=False, size=10, color="000000", italic=False):
    return Font(bold=bold, size=size, color=color, italic=italic,
                name="Calibri")

def align(h="left", v="center", wrap=True):
    return Alignment(horizontal=h, vertical=v, wrap_text=wrap)

def border_thin():
    s = Side(style="thin", color="BDBDBD")
    return Border(left=s, right=s, top=s, bottom=s)

def border_medium():
    s = Side(style="medium", color="546E7A")
    return Border(left=s, right=s, top=s, bottom=s)

def set_col_width(ws, col_letter, width):
    ws.column_dimensions[col_letter].width = width

def header_row(ws, row, headers, fill_color=NAVY, font_color=WHITE,
               font_size=10, bold=True, height=30):
    ws.row_dimensions[row].height = height
    for col, (title, width) in enumerate(headers, start=1):
        cell = ws.cell(row=row, column=col, value=title)
        cell.fill = fill(fill_color)
        cell.font = font(bold=bold, size=font_size, color=font_color)
        cell.alignment = align("center", "center")
        cell.border = border_thin()
        ws.column_dimensions[get_column_letter(col)].width = width

def title_block(ws, title, subtitle="", row=1):
    ws.row_dimensions[row].height = 40
    ws.merge_cells(f"A{row}:Z{row}")
    c = ws.cell(row=row, column=1, value=title)
    c.fill = fill(NAVY)
    c.font = font(bold=True, size=16, color=WHITE)
    c.alignment = align("center", "center")
    if subtitle:
        ws.row_dimensions[row+1].height = 22
        ws.merge_cells(f"A{row+1}:Z{row+1}")
        c2 = ws.cell(row=row+1, column=1, value=subtitle)
        c2.fill = fill(BLUE1)
        c2.font = font(bold=False, size=10, color=WHITE, italic=True)
        c2.alignment = align("center", "center")

def dv_list(ws, formula, sqref):
    dv = DataValidation(type="list", formula1=formula, allow_blank=True)
    dv.sqref = sqref
    ws.add_data_validation(dv)
    return dv

# ══════════════════════════════════════════════════════════════════════════════
# FICHIER 1 – Déclaration d'Applicabilité (DdA)
# ══════════════════════════════════════════════════════════════════════════════

CONTROLS_A = [
    # (code, nom_controle, theme, objectif_court, ref_loi0520, ref_dnssi)
    # A.5 – Politiques
    ("A.5.1","Politiques pour la SI","Politiques","Définir et communiquer les politiques de sécurité","Art. 5, 6","DNSSI-GOV-01"),
    ("A.5.2","Revue des politiques de SI","Politiques","Assurer la mise à jour régulière des politiques","Art. 5, 6","DNSSI-GOV-02"),
    # A.6 – Organisation
    ("A.6.1","Organisation interne","Organisation","Établir un cadre de gouvernance de la SI","Art. 7","DNSSI-GOV-03"),
    ("A.6.2","Mobilité et télétravail","Organisation","Sécuriser les accès distants et nomades","Art. 11","DNSSI-RES-01"),
    ("A.6.3","Attribution des responsabilités","Organisation","Définir clairement les rôles et responsabilités","Art. 7","DNSSI-GOV-04"),
    ("A.6.4","Séparation des tâches","Organisation","Éviter les conflits d'intérêts et la fraude","Art. 8","DNSSI-GOV-05"),
    ("A.6.5","Responsabilités vis-à-vis des autorités","Organisation","Maintenir les contacts avec DGSSI/ANSSI/CNDP","Art. 20","DNSSI-GOV-06"),
    ("A.6.6","Groupes d'intérêt spécifiques","Organisation","Participer aux réseaux CERT/CIRT","Art. 20","DNSSI-GOV-07"),
    ("A.6.7","Gestion incidents en télétravail","Organisation","Assurer la continuité de signalement à distance","Art. 16","DNSSI-INC-01"),
    ("A.6.8","Gestion des capacités","Organisation","Surveiller et planifier les capacités SI","Art. 12","DNSSI-EXP-01"),
    # A.7 – RH
    ("A.7.1","Vérification des antécédents","Ressources humaines","Contrôler les antécédents avant embauche","Art. 9","DNSSI-RH-01"),
    ("A.7.2","Termes et conditions d'embauche","Ressources humaines","Formaliser les obligations de sécurité contractuelles","Art. 9","DNSSI-RH-02"),
    ("A.7.3","Responsabilités de la direction (emploi)","Ressources humaines","Sensibiliser et former le personnel","Art. 10","DNSSI-RH-03"),
    ("A.7.4","Processus disciplinaires","Ressources humaines","Sanctionner les violations de la politique SI","Art. 10","DNSSI-RH-04"),
    ("A.7.5","Retour des actifs (fin contrat)","Ressources humaines","Assurer la restitution des équipements","Art. 11","DNSSI-RH-05"),
    ("A.7.6","Révocation des droits d'accès","Ressources humaines","Révoquer les accès dès la fin du contrat (<24h)","Art. 11","DNSSI-RH-06"),
    # A.8 – Actifs
    ("A.8.1","Inventaire des actifs","Gestion des actifs","Maintenir un inventaire exhaustif des actifs","Art. 12","DNSSI-ACT-01"),
    ("A.8.2","Propriété des actifs","Gestion des actifs","Désigner un propriétaire pour chaque actif","Art. 12","DNSSI-ACT-02"),
    ("A.8.3","Utilisation acceptable des actifs","Gestion des actifs","Définir les règles d'utilisation","Art. 12","DNSSI-ACT-03"),
    ("A.8.4","Restitution des actifs","Gestion des actifs","Formaliser la restitution en fin de contrat","Art. 12","DNSSI-ACT-04"),
    ("A.8.5","Classification des informations","Gestion des actifs","Classifier les informations selon leur sensibilité","Art. 13","DNSSI-ACT-05"),
    ("A.8.6","Étiquetage des informations","Gestion des actifs","Apposer les marquages de classification","Art. 13","DNSSI-ACT-06"),
    ("A.8.7","Gestion des supports amovibles","Gestion des actifs","Contrôler l'usage des supports amovibles","Art. 14","DNSSI-ACT-07"),
    ("A.8.8","Effacement sécurisé des supports","Gestion des actifs","Détruire/effacer les supports avant élimination","Art. 14","DNSSI-ACT-08"),
    ("A.8.9","Supports physiques en transit","Gestion des actifs","Protéger les supports lors du transport","Art. 14","DNSSI-ACT-09"),
    ("A.8.10","Externalisation cloud","Gestion des actifs","Contrôler la localisation et sécurité des données cloud","Art. 18","DNSSI-ACT-10"),
    # A.9 – Contrôle d'accès
    ("A.9.1","Politique de contrôle d'accès","Contrôle d'accès","Définir la politique de droits d'accès","Art. 15","DNSSI-ACC-01"),
    ("A.9.2","Accès aux réseaux","Contrôle d'accès","Contrôler l'accès aux réseaux et services","Art. 15","DNSSI-ACC-02"),
    ("A.9.3","Gestion des mots de passe","Contrôle d'accès","Imposer des mots de passe forts","Art. 15","DNSSI-ACC-03"),
    ("A.9.4","Authentification forte (MFA)","Contrôle d'accès","Déployer la MFA pour les accès sensibles","Art. 15","DNSSI-ACC-04"),
    ("A.9.5","Révocation des droits","Contrôle d'accès","Supprimer les accès dès le départ","Art. 15","DNSSI-ACC-05"),
    ("A.9.6","Accès privilégiés (PAM)","Contrôle d'accès","Gérer et tracer les comptes administrateurs","Art. 15","DNSSI-ACC-06"),
    ("A.9.7","Réexamen des droits d'accès","Contrôle d'accès","Revoir les droits régulièrement","Art. 15","DNSSI-ACC-07"),
    ("A.9.8","Comptes génériques","Contrôle d'accès","Interdire/encadrer les comptes partagés","Art. 15","DNSSI-ACC-08"),
    ("A.9.9","Droits d'accès aux systèmes","Contrôle d'accès","Appliquer le principe du moindre privilège","Art. 15","DNSSI-ACC-09"),
    ("A.9.10","Accès aux applications","Contrôle d'accès","Restreindre l'accès aux fonctions applicatives","Art. 15","DNSSI-ACC-10"),
    ("A.9.11","Accès aux codes sources","Contrôle d'accès","Protéger l'accès au code source","Art. 15","DNSSI-ACC-11"),
    ("A.9.12","Systèmes de gestion des mots de passe","Contrôle d'accès","Déployer un gestionnaire de mots de passe","Art. 15","DNSSI-ACC-12"),
    ("A.9.13","Contrôle des accès aux utilitaires","Contrôle d'accès","Limiter l'usage des utilitaires système","Art. 15","DNSSI-ACC-13"),
    ("A.9.14","Accès distant des prestataires","Contrôle d'accès","Tracer et contrôler les accès tiers","Art. 17","DNSSI-ACC-14"),
    # A.10 – Cryptographie
    ("A.10.1","Politique de cryptographie","Cryptographie","Définir les algorithmes et règles d'usage","Art. 16","DNSSI-CRY-01"),
    ("A.10.2","Gestion des clés cryptographiques","Cryptographie","Gérer le cycle de vie des clés (KMS)","Art. 16","DNSSI-CRY-02"),
    # A.11 – Sécurité physique
    ("A.11.1","Périmètre de sécurité physique","Sécurité physique","Délimiter les zones sécurisées","Art. 19","DNSSI-PHY-01"),
    ("A.11.2","Contrôle d'accès physique","Sécurité physique","Contrôler l'entrée dans les locaux","Art. 19","DNSSI-PHY-02"),
    ("A.11.3","Vidéoprotection","Sécurité physique","Surveiller les zones sensibles par caméra","Art. 19","DNSSI-PHY-03"),
    ("A.11.4","Protection incendie","Sécurité physique","Installer systèmes de détection et extinction","Art. 19","DNSSI-PHY-04"),
    ("A.11.5","Protection dégâts des eaux","Sécurité physique","Protéger les équipements contre l'eau","Art. 19","DNSSI-PHY-05"),
    ("A.11.6","Alimentation électrique (UPS/GE)","Sécurité physique","Assurer la continuité d'alimentation électrique","Art. 19","DNSSI-PHY-06"),
    ("A.11.7","Climatisation et environnement","Sécurité physique","Maintenir les conditions environnementales","Art. 19","DNSSI-PHY-07"),
    ("A.11.8","Sécurité du câblage","Sécurité physique","Protéger les câbles réseau et électriques","Art. 19","DNSSI-PHY-08"),
    ("A.11.9","Maintenance des équipements","Sécurité physique","Assurer la maintenance préventive","Art. 19","DNSSI-PHY-09"),
    ("A.11.10","Sécurité des équipements hors site","Sécurité physique","Protéger les équipements nomades","Art. 19","DNSSI-PHY-10"),
    ("A.11.11","Mise au rebut sécurisée","Sécurité physique","Effacer les données avant élimination","Art. 14","DNSSI-PHY-11"),
    ("A.11.12","Bureau propre / écran vide","Sécurité physique","Appliquer la politique clean desk","Art. 19","DNSSI-PHY-12"),
    ("A.11.13","Équipements sans surveillance","Sécurité physique","Verrouiller les sessions non utilisées","Art. 19","DNSSI-PHY-13"),
    ("A.11.14","Protection des documents papier","Sécurité physique","Sécuriser les documents physiques sensibles","Art. 13","DNSSI-PHY-14"),
    ("A.11.15","Zones de livraison et chargement","Sécurité physique","Contrôler les zones d'accès logistique","Art. 19","DNSSI-PHY-15"),
    # A.12 – Exploitation
    ("A.12.1","Gestion des changements","Sécurité exploitation","Formaliser le processus de gestion des changements","Art. 12","DNSSI-EXP-02"),
    ("A.12.2","Gestion des capacités","Sécurité exploitation","Surveiller et planifier les capacités","Art. 12","DNSSI-EXP-03"),
    ("A.12.3","Protection antimalware","Sécurité exploitation","Déployer et maintenir les solutions EDR/AV","Art. 12","DNSSI-EXP-04"),
    ("A.12.4","Sauvegarde","Sécurité exploitation","Appliquer la stratégie 3-2-1 de sauvegarde","Art. 12","DNSSI-EXP-05"),
    ("A.12.5","Restauration (RPO/RTO)","Sécurité exploitation","Tester la restauration régulièrement","Art. 12","DNSSI-EXP-06"),
    ("A.12.6","Journalisation des événements","Sécurité exploitation","Centraliser et conserver les logs (12 mois)","Art. 20","DNSSI-EXP-07"),
    ("A.12.7","Gestion des vulnérabilités","Sécurité exploitation","Scanner et corriger les vulnérabilités","Art. 12","DNSSI-EXP-08"),
    ("A.12.8","Gestion des correctifs","Sécurité exploitation","Appliquer les patches dans les délais","Art. 12","DNSSI-EXP-09"),
    ("A.12.9","Surveillance des systèmes","Sécurité exploitation","Monitorer les systèmes en temps réel (SIEM)","Art. 20","DNSSI-EXP-10"),
    ("A.12.10","Protection des réseaux en production","Sécurité exploitation","Segmenter et filtrer le trafic réseau","Art. 12","DNSSI-EXP-11"),
    ("A.12.11","Synchronisation des horloges","Sécurité exploitation","Synchroniser les horloges (NTP)","Art. 12","DNSSI-EXP-12"),
    ("A.12.12","Installation de logiciels","Sécurité exploitation","Contrôler les installations sur les systèmes","Art. 12","DNSSI-EXP-13"),
    ("A.12.13","Audit des systèmes d'information","Sécurité exploitation","Protéger les outils d'audit SI","Art. 20","DNSSI-EXP-14"),
    ("A.12.14","Maîtrise des logiciels opérationnels","Sécurité exploitation","Contrôler les logiciels en production","Art. 12","DNSSI-EXP-15"),
    # A.13 – Communications
    ("A.13.1","Sécurité des réseaux","Communications","Déployer et configurer les firewalls NGF","Art. 11","DNSSI-COM-01"),
    ("A.13.2","Séparation des réseaux","Communications","Segmenter les réseaux (VLAN, DMZ)","Art. 11","DNSSI-COM-02"),
    ("A.13.3","Séparation dev/production","Communications","Isoler les environnements de développement","Art. 11","DNSSI-COM-03"),
    ("A.13.4","Transfert sécurisé d'informations","Communications","Chiffrer les transferts (SFTP, TLS 1.2+)","Art. 11","DNSSI-COM-04"),
    ("A.13.5","Messagerie électronique","Communications","Filtrer les emails (spam, phishing, malware)","Art. 11","DNSSI-COM-05"),
    ("A.13.6","Accès distants (VPN)","Communications","Sécuriser les connexions VPN avec MFA","Art. 11","DNSSI-COM-06"),
    ("A.13.7","Réseaux sans fil","Communications","Sécuriser les réseaux WiFi (WPA3, RADIUS)","Art. 11","DNSSI-COM-07"),
    # A.14 – Développement
    ("A.14.1","Exigences de sécurité SI","Dév. & maintenance","Intégrer la sécurité dès la conception (SecByDesign)","Art. 12","DNSSI-DEV-01"),
    ("A.14.2","Sécurité des applications (SAST)","Dév. & maintenance","Analyser le code source (analyse statique)","Art. 12","DNSSI-DEV-02"),
    ("A.14.3","Protection des transactions","Dév. & maintenance","Déployer WAF, anti-injection, anti-XSS","Art. 12","DNSSI-DEV-03"),
    ("A.14.4","Tests de sécurité (DAST/Pentest)","Dév. & maintenance","Réaliser des tests d'intrusion annuels","Art. 12","DNSSI-DEV-04"),
    ("A.14.5","Environnements sécurisés","Dév. & maintenance","Cloisonner les environnements (dev/test/prod)","Art. 12","DNSSI-DEV-05"),
    ("A.14.6","Contrôle des changements de code","Dév. & maintenance","Imposer peer review et signature des commits","Art. 12","DNSSI-DEV-06"),
    ("A.14.7","Protection du code source","Dév. & maintenance","Héberger le code sur forge privée sécurisée","Art. 12","DNSSI-DEV-07"),
    ("A.14.8","Données de test","Dév. & maintenance","Anonymiser les données utilisées en test","Art. 13","DNSSI-DEV-08"),
    ("A.14.9","Externalisation du développement","Dév. & maintenance","Encadrer contractuellement les prestataires dev","Art. 17","DNSSI-DEV-09"),
    ("A.14.10","Packages et bibliothèques","Dév. & maintenance","Contrôler les dépendances logicielles (SCA)","Art. 12","DNSSI-DEV-10"),
    ("A.14.11","Déploiement sécurisé (CI/CD)","Dév. & maintenance","Sécuriser les pipelines de déploiement","Art. 12","DNSSI-DEV-11"),
    ("A.14.12","Revue après déploiement","Dév. & maintenance","Valider la conformité post-déploiement","Art. 12","DNSSI-DEV-12"),
    ("A.14.13","Sécurité des API","Dév. & maintenance","Authentifier et filtrer les appels API","Art. 12","DNSSI-DEV-13"),
    # A.15 – Fournisseurs
    ("A.15.1","Politique fournisseurs","Fournisseurs","Définir les exigences SI dans les contrats","Art. 17","DNSSI-FOU-01"),
    ("A.15.2","Exigences contractuelles SI","Fournisseurs","Inclure droit d'audit et clauses de notification","Art. 17","DNSSI-FOU-02"),
    ("A.15.3","Chaîne d'approvisionnement","Fournisseurs","Évaluer la sécurité des sous-traitants","Art. 17","DNSSI-FOU-03"),
    ("A.15.4","Surveillance des services fournisseurs","Fournisseurs","Mesurer les KPIs de sécurité fournisseurs","Art. 17","DNSSI-FOU-04"),
    ("A.15.5","Incidents chez les fournisseurs","Fournisseurs","Exiger notification d'incident <24h","Art. 17","DNSSI-FOU-05"),
    # A.16 – Incidents
    ("A.16.1","Responsabilités et procédures incidents","Gestion incidents","Documenter la procédure de gestion des incidents","Art. 16","DNSSI-INC-02"),
    ("A.16.2","Signalement des incidents","Gestion incidents","Former et outiller les utilisateurs au signalement","Art. 16","DNSSI-INC-03"),
    ("A.16.3","Réponse aux incidents","Gestion incidents","Déployer des playbooks de réponse (SOAR)","Art. 16","DNSSI-INC-04"),
    ("A.16.4","Recueil des preuves numériques","Gestion incidents","Appliquer les techniques forensic","Art. 16","DNSSI-INC-05"),
    ("A.16.5","Remontée post-incident (REX)","Gestion incidents","Réaliser un retour d'expérience après chaque incident","Art. 16","DNSSI-INC-06"),
    ("A.16.6","Notification aux autorités (DGSSI)","Gestion incidents","Notifier la DGSSI dans les délais légaux (<72h)","Art. 20, Loi 05-20","DNSSI-INC-07"),
    ("A.16.7","Recueil des failles de sécurité","Gestion incidents","Mettre en place un canal de signalement interne","Art. 16","DNSSI-INC-08"),
    # A.17 – Continuité
    ("A.17.1","Planification de la continuité (BIA)","Continuité","Réaliser l'Analyse d'Impact (BIA)","Art. 18","DNSSI-CON-01"),
    ("A.17.2","Mise en oeuvre du PCA/PRA","Continuité","Déployer le Plan de Continuité d'Activité","Art. 18","DNSSI-CON-02"),
    ("A.17.3","Vérification des plans de continuité","Continuité","Tester le PCA/PRA au moins 1 fois par an","Art. 18","DNSSI-CON-03"),
    ("A.17.4","Disponibilité des moyens de traitement","Continuité","Architecturer en haute disponibilité (HA)","Art. 18","DNSSI-CON-04"),
    # A.18 – Conformité
    ("A.18.1","Conformité exigences légales","Conformité","Maintenir un registre des exigences légales","Art. 1, 20, Loi 05-20","DNSSI-CON-05"),
    ("A.18.2","Conformité exigences sécurité","Conformité","Vérifier l'adéquation avec les politiques SI","Art. 20","DNSSI-CON-06"),
    ("A.18.3","Audit interne de conformité","Conformité","Programmer et réaliser des audits internes","Art. 20","DNSSI-CON-07"),
    ("A.18.4","Protection données personnelles (09-08)","Conformité","Désigner un DPO, tenir le registre des traitements","Loi 09-08, CNDP","DNSSI-CON-08"),
    ("A.18.5","Revue de direction","Conformité","Réaliser la revue de direction annuelle (entrées/sorties)","Art. 20","DNSSI-CON-09"),
    ("A.18.6","Gestion des licences logicielles","Conformité","Contrôler la conformité des licences","Art. 12","DNSSI-CON-10"),
]

# Statut applicabilité, conformité, priorité
STATUS_APPLIC = '"Applicable,Non applicable,Applicable avec exclusion"'
STATUS_CONF   = '"Conforme,Partiellement conforme,Non conforme,Non évalué"'
STATUS_PRIOR  = '"Critique,Haute,Moyenne,Faible"'
STATUS_PHASE  = '"Réalisé,En cours,Planifié,Non démarré"'

def build_dda():
    wb = Workbook()
    ws = wb.active
    ws.title = "DdA – Déclaration Applicabilité"

    # Figer les volets
    ws.freeze_panes = "A5"

    # Titre
    title_block(ws,
        "DÉCLARATION D'APPLICABILITÉ (DdA) – ISO/IEC 27001:2022",
        "Organisme : ___________________  |  Version : 1.0  |  Date : ___/___/______  |  RSSI : ___________________",
        row=1)

    # Légende couleurs
    ws.row_dimensions[3].height = 18
    legend = [
        ("A", "Conforme", LGREEN), ("B", "Partiellement conforme", LORANGE),
        ("C", "Non conforme", LRED), ("D", "Non applicable", LGREY),
    ]
    for i, (col_l, txt, clr) in enumerate(legend):
        c1 = ws.cell(row=3, column=i*3+1, value=txt)
        c1.fill = fill(clr); c1.font = font(size=9); c1.alignment = align("center")
        ws.merge_cells(start_row=3, start_column=i*3+1,
                       end_row=3, end_column=i*3+3)

    # En-têtes colonnes
    headers = [
        ("Code", 10), ("Contrôle ISO 27001:2022", 40),
        ("Thème", 20), ("Objectif", 45),
        ("Applicable ?", 15), ("Justification d'exclusion", 35),
        ("Niveau conformité", 18), ("Propriétaire", 22),
        ("Outil(s) déployé(s)", 35), ("Mesure mise en œuvre", 40),
        ("Preuve d'audit", 35), ("Priorité", 12),
        ("Échéance", 14), ("Statut avancement", 16),
        ("Réf. Loi 05-20", 18), ("Réf. DNSSI v2", 16),
        ("Commentaires", 35),
    ]
    header_row(ws, 4, headers, fill_color=NAVY, font_size=9)
    ws.row_dimensions[4].height = 35

    # Data validations
    last_row = 4 + len(CONTROLS_A)
    dv_list(ws, STATUS_APPLIC,   f"E5:E{last_row}")
    dv_list(ws, STATUS_CONF,     f"G5:G{last_row}")
    dv_list(ws, STATUS_PRIOR,    f"L5:L{last_row}")
    dv_list(ws, STATUS_PHASE,    f"N5:N{last_row}")

    # Remplissage des contrôles
    theme_colors = {
        "Politiques":       (LBLUE, BLUE1),
        "Organisation":     ("D1ECF1", "0C5460"),
        "Ressources humaines": (LGREEN, GREEN1),
        "Gestion des actifs":  (YELLOW, "827717"),
        "Contrôle d'accès":    (LORANGE, ORANGE1),
        "Cryptographie":       (LPURPLE, PURPLE),
        "Sécurité physique":   ("F5F5F5", GREY1),
        "Sécurité exploitation": ("FFF3E0", "BF360C"),
        "Communications":      ("E3F2FD", "0D47A1"),
        "Dév. & maintenance":  ("F3E5F5", "6A1B9A"),
        "Fournisseurs":        ("E8F5E9", "1B5E20"),
        "Gestion incidents":   (LRED, RED1),
        "Continuité":          ("FCE4EC", "880E4F"),
        "Conformité":          ("E0F2F1", "004D40"),
    }

    prev_theme = None
    for r, (code, nom, theme, obj, ref_loi, ref_dnssi) in enumerate(CONTROLS_A, start=5):
        ws.row_dimensions[r].height = 38
        bg, fg = theme_colors.get(theme, (LGREY, GREY1))

        row_data = [code, nom, theme, obj, "Applicable", "",
                    "Non évalué", "", "", "", "", "Moyenne",
                    "", "Non démarré", ref_loi, ref_dnssi, ""]

        for c, val in enumerate(row_data, start=1):
            cell = ws.cell(row=r, column=c, value=val)
            # Alternance légère
            if c in (1, 3, 15, 16):
                cell.fill = fill(bg)
                cell.font = font(bold=(c==1), size=9, color=fg)
            else:
                cell.fill = fill(LGREY if r % 2 == 0 else WHITE)
                cell.font = font(size=9)
            cell.alignment = align("left" if c > 2 else "center", "center")
            cell.border = border_thin()

            # Coloration code
            if c == 1:
                cell.font = font(bold=True, size=9, color=WHITE)
                cell.fill = fill(BLUE1 if r % 2 == 0 else NAVY)
                cell.alignment = align("center", "center")

        # Mise en couleur colonne conformité (G)
        conf_cell = ws.cell(row=r, column=7)
        conf_cell.fill = fill(LGREY)

    # Onglet Statistiques
    ws2 = wb.create_sheet("Statistiques DdA")
    title_block(ws2, "Tableau de bord – Déclaration d'Applicabilité", row=1)
    stats_headers = [("Thème", 30), ("Nb contrôles", 15), ("Applicables", 15),
                     ("Conformes", 15), ("Part. conformes", 18),
                     ("Non conformes", 16), ("Non évalués", 15), ("% Conformité", 15)]
    header_row(ws2, 3, stats_headers, fill_color=BLUE1)

    themes_count = {}
    for _, _, theme, _, _, _ in CONTROLS_A:
        themes_count[theme] = themes_count.get(theme, 0) + 1

    for r, (theme, cnt) in enumerate(themes_count.items(), start=4):
        ws2.row_dimensions[r].height = 25
        ws2.cell(row=r, column=1, value=theme).font = font(size=10)
        ws2.cell(row=r, column=2, value=cnt).font = font(size=10)
        for c in range(3, 8):
            cell = ws2.cell(row=r, column=c, value=0)
            cell.font = font(size=10)
            if r % 2 == 0: cell.fill = fill(LGREY)
        ws2.cell(row=r, column=8, value=0).number_format = "0%"

    # Instructions
    ws3 = wb.create_sheet("Guide d'utilisation")
    title_block(ws3, "Guide d'utilisation – DdA ISO 27001:2022", row=1)
    instructions = [
        (3, "COMMENT REMPLIR LA DÉCLARATION D'APPLICABILITÉ ?", NAVY, WHITE, True, 14),
        (5, "1. COLONNE 'APPLICABLE ?'", BLUE1, WHITE, True, 11),
        (6, "   • Applicable : le contrôle s'applique à votre périmètre SMSI", "", "", False, 10),
        (7, "   • Non applicable : le contrôle est exclu (justification obligatoire en colonne F)", "", "", False, 10),
        (8, "   • Applicable avec exclusion : partiellement applicable", "", "", False, 10),
        (10, "2. COLONNE 'NIVEAU DE CONFORMITÉ'", BLUE1, WHITE, True, 11),
        (11, "   • Conforme : le contrôle est pleinement mis en œuvre et prouvable", "", "", False, 10),
        (12, "   • Partiellement conforme : mis en œuvre mais incomplet ou sans preuve suffisante", "", "", False, 10),
        (13, "   • Non conforme : le contrôle n'est pas mis en œuvre (action corrective requise)", "", "", False, 10),
        (14, "   • Non évalué : à évaluer lors du prochain audit", "", "", False, 10),
        (16, "3. COLONNES 'OUTIL / MESURE / PREUVE D'AUDIT'", BLUE1, WHITE, True, 11),
        (17, "   • Outil : logiciel ou solution technique déployée (ex : Veeam, Splunk, CrowdStrike)", "", "", False, 10),
        (18, "   • Mesure : action concrète mise en œuvre (ex : scan hebdomadaire, MFA activé)", "", "", False, 10),
        (19, "   • Preuve d'audit : document, rapport, log prouvant la mise en œuvre", "", "", False, 10),
        (21, "4. RÉFÉRENCES RÉGLEMENTAIRES MAROC", BLUE1, WHITE, True, 11),
        (22, "   • Loi 05-20 : Loi relative à la cybersécurité (DGSSI, opérateurs d'importance vitale)", "", "", False, 10),
        (23, "   • Loi 09-08 : Protection des données personnelles (CNDP)", "", "", False, 10),
        (24, "   • DNSSI v2 : Directive Nationale de la Sécurité des Systèmes d'Information v2", "", "", False, 10),
        (26, "5. MISE À JOUR", BLUE1, WHITE, True, 11),
        (27, "   • La DdA doit être revue au moins 1 fois par an et après chaque changement majeur", "", "", False, 10),
        (28, "   • Chaque révision doit être documentée (version, date, validée par le RSSI et la direction)", "", "", False, 10),
    ]
    for row_n, text, bg_c, fg_c, bold, sz in instructions:
        ws3.merge_cells(f"A{row_n}:P{row_n}")
        c = ws3.cell(row=row_n, column=1, value=text)
        if bg_c:
            c.fill = fill(bg_c)
            c.font = font(bold=bold, size=sz, color=fg_c)
        else:
            c.font = font(bold=bold, size=sz)
        c.alignment = align("left", "center")
        ws3.row_dimensions[row_n].height = 20

    wb.save("/home/user/CyberResilience-/1_DdA_ISO27001_2022.xlsx")
    print("✓ 1_DdA_ISO27001_2022.xlsx généré")


# ══════════════════════════════════════════════════════════════════════════════
# FICHIER 2 – Plan de Traitement des Risques (PTR)
# ══════════════════════════════════════════════════════════════════════════════
def build_ptr():
    wb = Workbook()
    ws = wb.active
    ws.title = "Plan de Traitement des Risques"
    ws.freeze_panes = "A5"

    title_block(ws,
        "PLAN DE TRAITEMENT DES RISQUES (PTR) – ISO/IEC 27001:2022 / Loi 05-20",
        "Organisme : ___________________  |  Cycle : ______  |  Responsable risques : ___________________",
        row=1)

    headers = [
        ("ID Risque", 12), ("Actif concerné", 28),
        ("Menace", 30), ("Vulnérabilité", 30),
        ("Impact (1-5)", 13), ("Probabilité (1-5)", 17),
        ("Criticité brute\n(I×P)", 15), ("Niveau risque brut", 18),
        ("Option traitement", 20), ("Contrôle(s) A.X.X", 22),
        ("Mesure(s) prévue(s)", 38), ("Responsable action", 20),
        ("Échéance", 14), ("Priorité", 12),
        ("Statut", 15), ("Impact résiduel", 16),
        ("Probabilité résiduelle", 22), ("Criticité résiduelle", 18),
        ("Risque résiduel acceptable ?", 25), ("Preuve de traitement", 35),
        ("Réf. Loi 05-20 / DNSSI", 22), ("Commentaires", 30),
    ]
    header_row(ws, 4, headers, fill_color=NAVY, font_size=9)
    ws.row_dimensions[4].height = 40

    last = 104  # 100 lignes de risques
    dv_list(ws, '"1,2,3,4,5"', f"E5:E{last}")
    dv_list(ws, '"1,2,3,4,5"', f"F5:F{last}")
    dv_list(ws, '"Très élevé,Élevé,Moyen,Faible,Très faible"', f"H5:H{last}")
    dv_list(ws, '"Réduction,Transfert,Acceptation,Évitement"', f"I5:I{last}")
    dv_list(ws, STATUS_PRIOR, f"N5:N{last}")
    dv_list(ws, STATUS_PHASE, f"O5:O{last}")
    dv_list(ws, '"Oui,Non,En cours d\'évaluation"', f"S5:S{last}")

    # Exemples pré-remplis de risques
    sample_risks = [
        ("R-001","Système ERP","Ransomware","Absence de sauvegarde hors-site",5,4,"Réduction","A.12.4, A.12.5","Stratégie sauvegarde 3-2-1 + test de restauration","RSSI","2024-Q1","Critique","Non démarré","Art.12, DNSSI-EXP-05"),
        ("R-002","Active Directory","Usurpation d'identité","MFA non activé",5,4,"Réduction","A.9.4","Déploiement MFA (Microsoft Authenticator/Duo)","DSI","2024-Q1","Critique","Non démarré","Art.15, DNSSI-ACC-04"),
        ("R-003","Data center","Panne électrique","Absence d'onduleur/groupe électrogène",5,2,"Réduction","A.11.6","Installation UPS + groupe électrogène (30min+48h)","Responsable infra","2024-Q2","Haute","Non démarré","Art.19, DNSSI-PHY-06"),
        ("R-004","Messagerie","Phishing","Absence de filtre anti-phishing",4,5,"Réduction","A.13.5","Déploiement Proofpoint/Mimecast + sensibilisation","RSSI","2024-Q1","Critique","Non démarré","Art.11, DNSSI-COM-05"),
        ("R-005","Contrats fournisseurs","Fuite de données","Clauses sécurité absentes",4,3,"Réduction","A.15.2","Révision des contrats avec clause de sécurité","Juriste","2024-Q2","Haute","Non démarré","Art.17, DNSSI-FOU-02"),
        ("R-006","Accès VPN","Accès non autorisé","Authentification simple facteur",5,3,"Réduction","A.9.4, A.13.6","MFA obligatoire sur VPN + log des connexions","DSI","2024-Q1","Critique","Non démarré","Art.11, DNSSI-COM-06"),
        ("R-007","Données RH (SIRH)","Violation RGPD/09-08","Absence registre des traitements",3,4,"Réduction","A.18.4","Désignation DPO + registre traitements CNDP","DPO","2024-Q2","Haute","Non démarré","Loi 09-08, CNDP"),
        ("R-008","Serveurs web","Exploitation vulnérabilité","Absence de gestion des patchs",5,4,"Réduction","A.12.7, A.12.8","Scan mensuel Nessus + patching sous 72h (critique)","DSI","2024-Q1","Critique","Non démarré","Art.12, DNSSI-EXP-08"),
        ("R-009","Personnel","Erreur humaine","Absence de sensibilisation","3,3","","Réduction","A.7.3","Programme de sensibilisation annuel (LMS + phishing simulé)","RSSI","2024-Q2","Moyenne","Non démarré","Art.10, DNSSI-RH-03"),
        ("R-010","Site de production","Sinistre physique","Absence de PCA/PRA",5,2,"Réduction","A.17.1, A.17.2","Réalisation BIA + rédaction PCA/PRA + test annuel","RSSI","2024-Q3","Haute","Non démarré","Art.18, DNSSI-CON-01"),
    ]

    for r_idx, risk in enumerate(sample_risks, start=5):
        ws.row_dimensions[r_idx].height = 38
        id_r, actif, menace, vuln, impact, proba, option, ctrl, mesure, resp, ech, prior, statut, ref = risk
        row_bg = LGREY if r_idx % 2 == 0 else WHITE

        vals = [id_r, actif, menace, vuln, impact, proba, f"={impact}*{proba}" if isinstance(impact, int) else "", "",
                option, ctrl, mesure, resp, ech, prior, statut, "", "", "", "", "", ref, ""]

        # Criticité formule
        if isinstance(impact, int) and isinstance(proba, int):
            crit = impact * proba
            niveau = "Très élevé" if crit >= 20 else "Élevé" if crit >= 12 else "Moyen" if crit >= 6 else "Faible"
            vals[6] = crit
            vals[7] = niveau

        for c_idx, val in enumerate(vals, start=1):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.font = font(size=9)
            cell.alignment = align("center" if c_idx in (1,5,6,7,8,12,13,14,15) else "left", "center")
            cell.border = border_thin()

            if c_idx == 1:
                cell.fill = fill(NAVY); cell.font = font(bold=True, size=9, color=WHITE)
            elif c_idx in (5,6):
                cell.fill = fill(LORANGE)
            elif c_idx == 7:
                v = val if isinstance(val, int) else 0
                clr = RED1 if v >= 20 else ORANGE1 if v >= 12 else "FFA000" if v >= 6 else GREEN1
                cell.fill = fill(clr); cell.font = font(bold=True, size=10, color=WHITE)
            else:
                cell.fill = fill(row_bg)

    # Lignes vides pour saisie
    for r_idx in range(5+len(sample_risks), last+1):
        ws.row_dimensions[r_idx].height = 30
        id_val = f"R-{r_idx-4:03d}"
        ws.cell(row=r_idx, column=1, value=id_val).fill = fill(LGREY)
        ws.cell(row=r_idx, column=1).font = font(size=9, color=GREY2)
        for c_idx in range(2, len(headers)+1):
            cell = ws.cell(row=r_idx, column=c_idx)
            cell.fill = fill(WHITE if r_idx % 2 == 0 else LGREY)
            cell.border = border_thin()

    # Onglet Matrice des risques
    ws_mat = wb.create_sheet("Matrice des risques")
    title_block(ws_mat, "MATRICE DES RISQUES – Carte thermique (Impact × Probabilité)", row=1)
    ws_mat.row_dimensions[3].height = 22

    impacts = ["1 – Négligeable", "2 – Mineur", "3 – Modéré", "4 – Majeur", "5 – Catastrophique"]
    probas  = ["5 – Quasi certain", "4 – Probable", "3 – Possible", "2 – Improbable", "1 – Rare"]

    ws_mat.cell(row=3, column=1, value="Impact ↓ / Probabilité →").font = font(bold=True, size=10)
    for j, p in enumerate(probas, start=2):
        c = ws_mat.cell(row=3, column=j, value=p)
        c.font = font(bold=True, size=9, color=WHITE)
        c.fill = fill(NAVY); c.alignment = align("center")
        ws_mat.column_dimensions[get_column_letter(j)].width = 18

    ws_mat.column_dimensions["A"].width = 22
    heat_colors = {
        range(1,6):   "4CAF50",
        range(6,11):  "FFC107",
        range(11,16): "FF9800",
        range(16,21): "F44336",
        range(21,26): "B71C1C",
    }
    def heat_color(score):
        for rng, clr in heat_colors.items():
            if score in rng: return clr
        return "B71C1C"

    for i, imp_lbl in enumerate(impacts, start=4):
        imp_val = i - 3
        ws_mat.row_dimensions[i].height = 35
        c = ws_mat.cell(row=i, column=1, value=imp_lbl)
        c.font = font(bold=True, size=9, color=WHITE); c.fill = fill(NAVY)
        c.alignment = align("center")
        for j, prob_lbl in enumerate(probas, start=2):
            prob_val = 6 - j
            score = imp_val * prob_val
            cell = ws_mat.cell(row=i, column=j, value=score)
            cell.fill = fill(heat_color(score))
            cell.font = font(bold=True, size=12, color=WHITE)
            cell.alignment = align("center", "center")
            cell.border = border_medium()

    # Légende
    ws_mat.cell(row=10, column=1, value="Légende :").font = font(bold=True, size=10)
    legend_items = [
        (11, "4CAF50", "1-5  : Risque FAIBLE – Acceptation possible"),
        (12, "FFC107", "6-10 : Risque MOYEN – Plan d'action requis"),
        (13, "FF9800", "11-15: Risque ÉLEVÉ – Action prioritaire"),
        (14, "F44336", "16-20: Risque TRÈS ÉLEVÉ – Action immédiate"),
        (15, "B71C1C", "21-25: Risque CRITIQUE – Traitement urgent / Direction"),
    ]
    for row_n, clr, txt in legend_items:
        ws_mat.cell(row=row_n, column=1, value="").fill = fill(clr)
        c = ws_mat.cell(row=row_n, column=2, value=txt)
        c.font = font(size=10)
        ws_mat.merge_cells(f"B{row_n}:G{row_n}")

    wb.save("/home/user/CyberResilience-/2_Plan_Traitement_Risques.xlsx")
    print("✓ 2_Plan_Traitement_Risques.xlsx généré")


# ══════════════════════════════════════════════════════════════════════════════
# FICHIER 3 – Registre des Incidents
# ══════════════════════════════════════════════════════════════════════════════
def build_incidents():
    wb = Workbook()
    ws = wb.active
    ws.title = "Registre des Incidents"
    ws.freeze_panes = "A5"

    title_block(ws,
        "REGISTRE DES INCIDENTS DE SÉCURITÉ – ISO 27001 A.16 / Loi 05-20 Art.20",
        "Organisme : ___________________  |  RSSI : ___________________  |  Notification DGSSI <72h (incidents critiques)",
        row=1)

    headers = [
        ("ID Incident", 12), ("Date détection", 16), ("Date clôture", 14),
        ("Catégorie", 22), ("Sous-catégorie", 25), ("Description", 45),
        ("Actif(s) impacté(s)", 28), ("Source détection", 22),
        ("Gravité", 12), ("Impact métier", 22), ("Durée indisponibilité", 20),
        ("Déclarant", 20), ("Responsable traitement", 22),
        ("Statut", 15), ("Actions immédiates", 40), ("Actions correctives", 40),
        ("Preuve(s) forensic", 30), ("Notification DGSSI ?", 18),
        ("Date notification DGSSI", 22), ("REX réalisé ?", 14),
        ("Contrôle(s) A.X.X concerné(s)", 28), ("Réf. Loi 05-20", 18),
        ("Leçons apprises", 40),
    ]
    header_row(ws, 4, headers, fill_color=RED1, font_size=9)
    ws.row_dimensions[4].height = 40

    last = 204
    dv_list(ws, '"Malware/Ransomware,Phishing/Social Eng.,Accès non autorisé,Fuite de données,DDoS,Erreur humaine,Panne système,Violation physique,Fraude interne,Autre"', f"D5:D{last}")
    dv_list(ws, '"Critique,Élevée,Moyenne,Faible"', f"I5:I{last}")
    dv_list(ws, '"Ouvert,En cours,Résolu,Clôturé,Escaladé DGSSI"', f"N5:N{last}")
    dv_list(ws, '"Oui – notifié,Oui – en cours,Non – sous seuil,Non évalué"', f"R5:R{last}")
    dv_list(ws, '"Oui,Non,En cours"', f"T5:T{last}")

    # Exemples d'incidents
    sample = [
        ("INC-001","2024-01-15","2024-01-18","Malware/Ransomware","Ransomware LockBit",
         "Chiffrement de 3 serveurs de fichiers suite à un email de phishing",
         "Serveurs FS01, FS02, FS03","SIEM (alerte EDR CrowdStrike)","Critique",
         "Indisponibilité des fichiers partagés – 250 utilisateurs impactés","72h",
         "J. Martin","RSSI + DSI","Clôturé",
         "Isolation réseau immédiate, restauration depuis sauvegarde Veeam",
         "Déploiement MFA, revue des règles firewall, scan de vulnérabilités",
         "Hash SHA256 des fichiers chiffrés, logs EDR, image disque FTK",
         "Oui – notifié","2024-01-16","Oui",
         "A.12.3, A.12.4, A.13.5","Art.20 Loi 05-20",
         "Renforcer la segmentation réseau et activer MFA sur tous les accès"),
        ("INC-002","2024-02-03","2024-02-05","Phishing/Social Eng.","Spear phishing RH",
         "Email frauduleux usurpant l'identité du DG demandant un virement",
         "Messagerie Exchange","Signalement utilisateur","Élevée",
         "Tentative de fraude – virement bloqué","0h",
         "K. Alami","RSSI","Clôturé",
         "Blocage de l'email, alerte à la direction",
         "Simulation de phishing + formation anti-fraude",
         "En-têtes email, logs Proofpoint","Non – sous seuil","","Oui",
         "A.13.5, A.7.3","Art.16 Loi 05-20",
         "Mettre en place procédure de double validation pour virements >50kDH"),
        ("INC-003","2024-03-20","","Accès non autorisé","Compte compromis",
         "Connexion depuis IP étrangère (Russie) sur compte utilisateur",
         "Azure AD / O365","Azure AD Identity Protection","Élevée",
         "Accès potentiel aux emails et fichiers SharePoint","En cours",
         "Azure AD","RSSI","En cours",
         "Désactivation immédiate du compte, réinitialisation MDP",
         "Activation MFA, revue des journaux d'accès 30 derniers jours",
         "Logs Azure AD, rapport Azure Sentinel","Non évalué","","Non",
         "A.9.4, A.9.5, A.12.6","Art.20 Loi 05-20",
         "Activer la protection Azure AD pour tous les comptes en priorité"),
    ]

    for r_idx, inc in enumerate(sample, start=5):
        ws.row_dimensions[r_idx].height = 55
        for c_idx, val in enumerate(inc, start=1):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.alignment = align("left" if c_idx > 3 else "center", "top")
            cell.border = border_thin()
            cell.font = font(size=9)
            if c_idx == 1:
                cell.fill = fill(RED1); cell.font = font(bold=True, size=9, color=WHITE)
            elif c_idx == 9:  # Gravité
                clr = {"Critique": RED1, "Élevée": ORANGE1, "Moyenne": "FFC107", "Faible": GREEN2}.get(val, LGREY)
                cell.fill = fill(clr); cell.font = font(bold=True, size=9, color=WHITE)
            elif r_idx % 2 == 0:
                cell.fill = fill(LGREY)

    # Lignes vides
    for r_idx in range(5+len(sample), last+1):
        ws.row_dimensions[r_idx].height = 35
        ws.cell(row=r_idx, column=1, value=f"INC-{r_idx-4:03d}").fill = fill(LGREY)
        ws.cell(row=r_idx, column=1).font = font(size=9, color=GREY2)
        for c_idx in range(2, len(headers)+1):
            cell = ws.cell(row=r_idx, column=c_idx)
            cell.border = border_thin()
            cell.fill = fill(WHITE if r_idx % 2 == 0 else LGREY)

    # Onglet : Tableau de bord incidents
    ws_dash = wb.create_sheet("Tableau de bord")
    title_block(ws_dash, "TABLEAU DE BORD – Incidents de Sécurité", row=1)

    kpis = [
        ("Nb incidents total (mois)", 0, "A.16.1"),
        ("Nb incidents critiques", 0, "A.16.1"),
        ("Délai moyen de détection (heures)", 0, "A.12.9"),
        ("Délai moyen de résolution (heures)", 0, "A.16.3"),
        ("Taux incidents avec REX (%)", "0%", "A.16.5"),
        ("Nb notifications DGSSI envoyées", 0, "Loi 05-20 Art.20"),
        ("Délai moyen notification DGSSI (heures)", 0, "Loi 05-20 Art.20"),
        ("Nb incidents récurrents", 0, "A.10.2"),
    ]
    header_row(ws_dash, 3, [("Indicateur", 45), ("Valeur (période)", 20), ("Réf. contrôle", 22)],
               fill_color=RED1)
    for r_idx, (kpi, val, ref) in enumerate(kpis, start=4):
        ws_dash.row_dimensions[r_idx].height = 28
        ws_dash.cell(row=r_idx, column=1, value=kpi).font = font(size=10)
        ws_dash.cell(row=r_idx, column=2, value=val).font = font(bold=True, size=12)
        ws_dash.cell(row=r_idx, column=3, value=ref).font = font(size=9, italic=True)
        for c in range(1, 4):
            ws_dash.cell(row=r_idx, column=c).border = border_thin()
            if r_idx % 2 == 0:
                ws_dash.cell(row=r_idx, column=c).fill = fill(LGREY)

    wb.save("/home/user/CyberResilience-/3_Registre_Incidents.xlsx")
    print("✓ 3_Registre_Incidents.xlsx généré")


# ══════════════════════════════════════════════════════════════════════════════
# FICHIER 4 – Programme d'Audit Interne
# ══════════════════════════════════════════════════════════════════════════════
def build_audit():
    wb = Workbook()
    ws = wb.active
    ws.title = "Programme Audit"
    ws.freeze_panes = "A5"

    title_block(ws,
        "PROGRAMME D'AUDIT INTERNE SMSI – ISO/IEC 27001:2022 / Loi 05-20",
        "Cycle d'audit : ______  |  Auditeur chef de file : ___________________  |  Approuvé par : ___________________",
        row=1)

    headers = [
        ("ID Audit", 12), ("Domaine audité", 28), ("Clauses / Annexe A", 22),
        ("Auditeur(s)", 25), ("Date planifiée", 16), ("Date réelle", 14),
        ("Type d'audit", 18), ("Méthode", 20), ("Périmètre", 35),
        ("Statut", 14), ("Nb constats", 12), ("Nb NC majeures", 15),
        ("Nb NC mineures", 15), ("Nb points à améliorer", 20),
        ("Rapport disponible ?", 20), ("Date remise rapport", 18),
        ("Plan d'actions associé", 25), ("Date clôture actions", 18),
        ("Commentaires", 30),
    ]
    header_row(ws, 4, headers, fill_color=PURPLE, font_color=WHITE, font_size=9)
    ws.row_dimensions[4].height = 40

    last = 54
    dv_list(ws, '"Audit documentaire,Audit terrain,Audit technique,Audit fournisseur,Mixte"', f"G5:G{last}")
    dv_list(ws, '"Entretiens,Observation,Revue documentaire,Tests techniques,Mixte"', f"H5:H{last}")
    dv_list(ws, '"Planifié,En cours,Réalisé,Reporté,Annulé"', f"J5:J{last}")
    dv_list(ws, '"Oui,Non,En cours de rédaction"', f"O5:O{last}")

    sample_audits = [
        ("AUD-001","Politique & Gouvernance SI","Cl.4,5,6,7 + A.5,A.6","RSSI + Auditeur interne",
         "2024-02-15","2024-02-15","Audit documentaire","Revue documentaire + Entretiens",
         "Politiques SI, organisation SMSI, rôles et responsabilités",
         "Réalisé","8","1","3","2","Oui","2024-02-20","PAC-001","2024-04-30",""),
        ("AUD-002","Contrôle d'accès & Identités","A.9, A.10","DSI + Auditeur interne",
         "2024-03-10","2024-03-12","Mixte","Entretiens + Tests techniques",
         "IAM, MFA, revue des droits, PAM, comptes génériques",
         "Réalisé","12","2","5","4","Oui","2024-03-20","PAC-002","2024-05-31",""),
        ("AUD-003","Sécurité physique Datacenter","A.11","Auditeur externe",
         "2024-04-05","","Audit terrain","Observation + Revue documentaire",
         "Datacenter principal et site de secours",
         "Planifié","","","","","Non","","","",""),
        ("AUD-004","Gestion des vulnérabilités & patchs","A.12.7, A.12.8","DSI + RSSI",
         "2024-04-20","","Audit technique","Tests techniques (scan Nessus)",
         "Serveurs, postes de travail, équipements réseau",
         "Planifié","","","","","Non","","","",""),
        ("AUD-005","Gestion des incidents","A.16","RSSI",
         "2024-05-15","","Audit documentaire","Revue du registre + entretiens",
         "Procédures, registre incidents, délais notification DGSSI",
         "Planifié","","","","","Non","","","",""),
        ("AUD-006","Continuité d'activité (PCA/PRA)","A.17","RSSI + DG",
         "2024-06-10","","Mixte","Test de bascule + revue documentaire",
         "PCA, PRA, résultats tests de restauration, BIA",
         "Planifié","","","","","Non","","","",""),
        ("AUD-007","Conformité légale (Loi 05-20, 09-08)","A.18","Juriste + RSSI",
         "2024-07-08","","Audit documentaire","Revue + entretiens DPO",
         "Registre des traitements, conformité CNDP, notification DGSSI",
         "Planifié","","","","","Non","","","",""),
        ("AUD-008","Relations fournisseurs","A.15","Responsable achats + RSSI",
         "2024-08-15","","Audit fournisseur","Entretiens + revue contrats",
         "Top 10 fournisseurs critiques, clauses sécurité, questionnaires",
         "Planifié","","","","","Non","","","",""),
    ]

    for r_idx, aud in enumerate(sample_audits, start=5):
        ws.row_dimensions[r_idx].height = 42
        for c_idx, val in enumerate(aud, start=1):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.border = border_thin()
            cell.font = font(size=9)
            cell.alignment = align("center" if c_idx in (1,5,6,10,11,12,13,14) else "left", "center")
            if c_idx == 1:
                cell.fill = fill(PURPLE); cell.font = font(bold=True, size=9, color=WHITE)
            elif c_idx == 10:
                clr = {"Réalisé": GREEN1, "Planifié": BLUE1, "En cours": ORANGE1, "Reporté": RED1}.get(val, LGREY)
                cell.fill = fill(clr); cell.font = font(bold=True, size=9, color=WHITE)
            elif r_idx % 2 == 0:
                cell.fill = fill(LGREY)

    # Onglet Checklist d'audit
    ws_chk = wb.create_sheet("Checklist Audit")
    ws_chk.freeze_panes = "A4"
    title_block(ws_chk, "CHECKLIST D'AUDIT ISO 27001:2022 – Questions par Contrôle", row=1)

    chk_headers = [
        ("Code", 10), ("Contrôle", 38), ("Question d'audit", 55),
        ("Éléments de preuve attendus", 45), ("Constat", 18),
        ("Note (1-5)", 12), ("Observations", 40),
    ]
    header_row(ws_chk, 3, chk_headers, fill_color=PURPLE, font_size=9)
    ws_chk.row_dimensions[3].height = 32

    last_chk = 3 + len(CONTROLS_A) + 10
    dv_list(ws_chk, '"Conforme,Partiellement conforme,Non conforme,Non applicable,Non évalué"', f"E4:E{last_chk}")
    dv_list(ws_chk, '"1,2,3,4,5"', f"F4:F{last_chk}")

    audit_questions = {
        "A.5.1": ("La politique de sécurité est-elle documentée, signée et communiquée ?",
                  "Politique signée par DG, historique versions, preuve de diffusion"),
        "A.5.2": ("La politique a-t-elle été revue dans les 12 derniers mois ?",
                  "PV de revue daté, liste des participants, modifications apportées"),
        "A.6.1": ("Un comité de sécurité existe-t-il avec des réunions documentées ?",
                  "Organigramme SI, PV de réunions (min. 4/an)"),
        "A.9.4": ("La MFA est-elle activée sur tous les accès distants (VPN, cloud) ?",
                  "Rapport console IAM (taux MFA >95%), configuration"),
        "A.12.4": ("La stratégie de sauvegarde 3-2-1 est-elle appliquée et testée ?",
                  "Rapport Veeam, PV de test de restauration daté de moins de 12 mois"),
        "A.16.6": ("Les incidents critiques sont-ils notifiés à la DGSSI dans les 72h ?",
                  "Registre incidents avec dates de notification, accusés réception DGSSI"),
        "A.18.1": ("Un registre des exigences légales est-il tenu à jour (Loi 05-20, 09-08) ?",
                  "Registre des exigences légales revue annuellement"),
    }

    for r_idx, (code, nom, theme, obj, ref_loi, ref_dnssi) in enumerate(CONTROLS_A, start=4):
        ws_chk.row_dimensions[r_idx].height = 38
        q, ev = audit_questions.get(code, (
            f"Le contrôle {code} est-il mis en œuvre et documenté ?",
            "Politique, procédure ou preuve technique d'application"
        ))

        row_data = [code, nom, q, ev, "", "", ""]
        for c_idx, val in enumerate(row_data, start=1):
            cell = ws_chk.cell(row=r_idx, column=c_idx, value=val)
            cell.border = border_thin()
            cell.font = font(size=9)
            cell.alignment = align("center" if c_idx == 1 else "left", "center")
            if c_idx == 1:
                cell.fill = fill(PURPLE); cell.font = font(bold=True, size=9, color=WHITE)
            elif r_idx % 2 == 0:
                cell.fill = fill(LGREY)

    # Onglet Plan d'actions correctives
    ws_pac = wb.create_sheet("Plan d'Actions Correctives")
    ws_pac.freeze_panes = "A5"
    title_block(ws_pac,
        "PLAN D'ACTIONS CORRECTIVES (PAC) – Post-Audit",
        "À compléter après chaque audit interne ou externe", row=1)

    pac_headers = [
        ("ID Action", 12), ("ID Audit source", 15), ("Contrôle concerné", 18),
        ("Type de constat", 20), ("Description de la non-conformité", 50),
        ("Cause racine", 40), ("Action corrective prévue", 45),
        ("Responsable", 20), ("Priorité", 12), ("Échéance", 14),
        ("Statut", 15), ("Preuve de clôture", 35), ("Date clôture", 14),
        ("Efficacité vérifiée ?", 20), ("Commentaires", 30),
    ]
    header_row(ws_pac, 4, pac_headers, fill_color=PURPLE, font_size=9)
    ws_pac.row_dimensions[4].height = 38

    last_pac = 104
    dv_list(ws_pac, '"Non-conformité majeure,Non-conformité mineure,Point d\'amélioration,Observation"', f"D5:D{last_pac}")
    dv_list(ws_pac, STATUS_PRIOR, f"I5:I{last_pac}")
    dv_list(ws_pac, STATUS_PHASE, f"K5:K{last_pac}")
    dv_list(ws_pac, '"Oui – efficace,Oui – partiellement efficace,Non – réouvert,En cours de vérification"', f"N5:N{last_pac}")

    for r_idx in range(5, last_pac+1):
        ws_pac.row_dimensions[r_idx].height = 32
        ws_pac.cell(row=r_idx, column=1, value=f"PAC-{r_idx-4:03d}").fill = fill(LPURPLE)
        ws_pac.cell(row=r_idx, column=1).font = font(size=9, color=PURPLE, bold=True)
        for c_idx in range(2, len(pac_headers)+1):
            cell = ws_pac.cell(row=r_idx, column=c_idx)
            cell.border = border_thin()
            cell.fill = fill(WHITE if r_idx % 2 == 0 else LGREY)

    wb.save("/home/user/CyberResilience-/4_Programme_Audit_Interne.xlsx")
    print("✓ 4_Programme_Audit_Interne.xlsx généré")


# ══════════════════════════════════════════════════════════════════════════════
# FICHIER 5 – Tableau de Bord SMSI (KPIs)
# ══════════════════════════════════════════════════════════════════════════════
def build_dashboard():
    wb = Workbook()
    ws = wb.active
    ws.title = "Tableau de Bord SMSI"

    title_block(ws,
        "TABLEAU DE BORD SMSI – KPIs ISO 27001:2022 / Loi 05-20 / DNSSI v2",
        "Organisme : ___________________  |  Période : ___/___  |  RSSI : ___________________",
        row=1)

    ws.row_dimensions[3].height = 22
    ws.cell(row=3, column=1, value="⚠ Ce tableau de bord est à mettre à jour mensuellement et présenté en revue de direction (Clause 9.3)").font = font(italic=True, size=10, color=ORANGE1)
    ws.merge_cells("A3:P3")

    # Section 1 : KPIs Gouvernance
    sections = [
        ("GOUVERNANCE & POLITIQUE", NAVY, [
            ("Politique SI signée et à jour", "Oui/Non", "", "A.5.1", "100% = Oui"),
            ("DdA validée et à jour", "Oui/Non", "", "A.5.1", "100% = Oui"),
            ("Revue de direction réalisée", "Oui/Non / Date", "", "Cl.9.3", "1x/an minimum"),
            ("Nb audits internes réalisés vs planifiés", "x/y", "", "Cl.9.2", ">= 100% du plan"),
            ("Nb non-conformités ouvertes", "Nombre", "", "Cl.10.1", "< 5 NC majeures"),
            ("Taux de sensibilisation (% personnel formé)", "%", "", "A.7.3", ">= 90%"),
        ]),
        ("CONTRÔLE D'ACCÈS & IDENTITÉS", BLUE1, [
            ("Taux d'activation MFA (accès distants)", "%", "", "A.9.4", ">= 95%"),
            ("Nb comptes non révoqués après départ", "Nombre", "", "A.9.5", "= 0"),
            ("Nb comptes génériques non justifiés", "Nombre", "", "A.9.8", "= 0"),
            ("Délai moyen révocation (heures)", "h", "", "A.9.5", "<= 24h"),
            ("Nb accès privilégiés sans PAM", "Nombre", "", "A.9.6", "= 0"),
            ("Taux de revue des droits d'accès", "%", "", "A.9.7", "100% trimestriel"),
        ]),
        ("GESTION DES VULNÉRABILITÉS & PATCHS", GREEN1, [
            ("Taux de couverture scan vulnérabilités", "%", "", "A.12.7", ">= 95%"),
            ("Nb vulnérabilités critiques ouvertes >72h", "Nombre", "", "A.12.7", "= 0"),
            ("Nb vulnérabilités hautes ouvertes >14j", "Nombre", "", "A.12.7", "< 5"),
            ("Taux application patchs critiques (<48h)", "%", "", "A.12.8", ">= 95%"),
            ("Taux application patchs standards (<14j)", "%", "", "A.12.8", ">= 90%"),
            ("Délai moyen correction vulnérabilités (j)", "jours", "", "A.12.7", "<= 7j (critique)"),
        ]),
        ("SAUVEGARDE & CONTINUITÉ", ORANGE1, [
            ("Taux de succès des sauvegardes", "%", "", "A.12.4", ">= 99%"),
            ("Date dernier test de restauration", "Date", "", "A.12.5", "< 12 mois"),
            ("RPO objectif atteint lors du test", "Oui/Non", "", "A.12.5", "Oui"),
            ("RTO objectif atteint lors du test", "Oui/Non", "", "A.12.5", "Oui"),
            ("Date dernier test PCA/PRA", "Date", "", "A.17.3", "< 12 mois"),
            ("Disponibilité systèmes critiques", "%", "", "A.17.4", ">= 99.5%"),
        ]),
        ("INCIDENTS DE SÉCURITÉ", RED1, [
            ("Nb incidents (mois en cours)", "Nombre", "", "A.16.1", "< 10 (hors critiques)"),
            ("Nb incidents critiques", "Nombre", "", "A.16.1", "= 0 idéal"),
            ("Délai moyen détection (heures)", "h", "", "A.12.9", "<= 4h"),
            ("Délai moyen résolution (heures)", "h", "", "A.16.3", "<= 24h"),
            ("Taux incidents avec REX", "%", "", "A.16.5", "100% incidents critiques"),
            ("Nb notifications DGSSI envoyées / requises", "x/y", "", "Loi 05-20 Art.20", "100% dans <72h"),
        ]),
        ("CONFORMITÉ LÉGALE (LOI 05-20 / 09-08)", PURPLE, [
            ("Registre des exigences légales à jour", "Oui/Non / Date", "", "A.18.1", "Revue annuelle"),
            ("Registre CNDP (traitements) à jour", "Oui/Non / Date", "", "A.18.4", "Continu"),
            ("DPO désigné et opérationnel", "Oui/Non", "", "Loi 09-08", "Oui"),
            ("Audits de conformité 05-20 réalisés", "Nb/an", "", "Loi 05-20", ">= 1/an"),
            ("Nb violations données déclarées CNDP", "Nombre", "", "Loi 09-08", "= 0 idéal"),
            ("Taux contrats fournisseurs avec clauses SI", "%", "", "A.15.1", ">= 100%"),
        ]),
    ]

    current_row = 5
    for section_title, color, kpis in sections:
        # Titre de section
        ws.row_dimensions[current_row].height = 30
        ws.merge_cells(f"A{current_row}:P{current_row}")
        c = ws.cell(row=current_row, column=1, value=f"  {section_title}")
        c.fill = fill(color); c.font = font(bold=True, size=12, color=WHITE)
        c.alignment = align("left", "center")
        current_row += 1

        # En-têtes KPI
        kpi_headers = [("Indicateur de performance (KPI)", 45), ("Valeur actuelle", 18),
                       ("Valeur N-1", 16), ("Réf. contrôle", 22),
                       ("Cible / Seuil", 25), ("Tendance", 12),
                       ("Statut", 14), ("Action si écart", 35)]
        header_row(ws, current_row, kpi_headers, fill_color=GREY1, font_size=9)
        ws.row_dimensions[current_row].height = 28
        current_row += 1

        # KPIs
        dv_list(ws, '"↑ Amélioration,→ Stable,↓ Dégradation"', f"F{current_row}:F{current_row+len(kpis)}")
        dv_list(ws, '"✅ Conforme,⚠ À surveiller,❌ Non conforme,⬜ Non mesuré"', f"G{current_row}:G{current_row+len(kpis)}")

        for kpi_name, unit, val_n1, ref, target in kpis:
            ws.row_dimensions[current_row].height = 30
            row_data = [kpi_name, f"[{unit}]", val_n1, ref, target, "→ Stable", "⬜ Non mesuré", ""]
            for c_idx, val in enumerate(row_data, start=1):
                cell = ws.cell(row=current_row, column=c_idx, value=val)
                cell.border = border_thin()
                cell.font = font(size=9)
                cell.alignment = align("center" if c_idx in (2,3,6,7) else "left", "center")
                if current_row % 2 == 0: cell.fill = fill(LGREY)
            current_row += 1

        current_row += 1  # ligne vide entre sections

    # Onglet : Historique mensuel
    ws_hist = wb.create_sheet("Historique mensuel")
    title_block(ws_hist, "HISTORIQUE MENSUEL DES KPIs – SMSI", row=1)

    months = ["Jan", "Fév", "Mar", "Avr", "Mai", "Jun",
              "Jul", "Aoû", "Sep", "Oct", "Nov", "Déc"]
    hist_kpis = [
        "Taux MFA (%)", "Nb incidents critiques", "Taux sauvegarde (%)",
        "Nb vulns critiques ouvertes", "Taux sensibilisation (%)",
        "Disponibilité systèmes (%)", "Délai détection incidents (h)",
        "Nb NC ouvertes post-audit",
    ]

    ws_hist.cell(row=3, column=1, value="KPI / Mois").font = font(bold=True, size=10)
    ws_hist.column_dimensions["A"].width = 38
    for j, m in enumerate(months, start=2):
        c = ws_hist.cell(row=3, column=j, value=m)
        c.fill = fill(NAVY); c.font = font(bold=True, size=10, color=WHITE)
        c.alignment = align("center")
        ws_hist.column_dimensions[get_column_letter(j)].width = 10

    ws_hist.cell(row=3, column=14, value="Cible").fill = fill(GREEN1)
    ws_hist.cell(row=3, column=14).font = font(bold=True, size=10, color=WHITE)
    ws_hist.column_dimensions["N"].width = 12
    ws_hist.cell(row=3, column=15, value="Tendance").fill = fill(BLUE1)
    ws_hist.cell(row=3, column=15).font = font(bold=True, size=10, color=WHITE)
    ws_hist.column_dimensions["O"].width = 14

    targets = [95, 0, 99, 0, 90, 99.5, 4, 0]
    for r_idx, kpi in enumerate(hist_kpis, start=4):
        ws_hist.row_dimensions[r_idx].height = 28
        c = ws_hist.cell(row=r_idx, column=1, value=kpi)
        c.font = font(size=10, bold=True)
        c.fill = fill(LGREY if r_idx % 2 == 0 else WHITE)
        for j in range(2, 14):
            cell = ws_hist.cell(row=r_idx, column=j)
            cell.border = border_thin()
            cell.fill = fill(LGREY if r_idx % 2 == 0 else WHITE)
            cell.alignment = align("center")
        ws_hist.cell(row=r_idx, column=14, value=targets[r_idx-4]).font = font(bold=True, size=10, color=GREEN2)
        ws_hist.cell(row=r_idx, column=14).alignment = align("center")

    # Onglet Revue de direction
    ws_rd = wb.create_sheet("Revue de Direction")
    title_block(ws_rd,
        "ORDRE DU JOUR – REVUE DE DIRECTION SMSI (Clause 9.3)",
        "Date : ___/___/______  |  Lieu : ___________________  |  Animateur : RSSI",
        row=1)

    inputs = [
        ("ENTRÉES OBLIGATOIRES (ISO 27001 Cl.9.3)", NAVY, [
            ("1.", "État des actions issues des revues précédentes", "Tableau de suivi PAC"),
            ("2.", "Changements dans le contexte externe/interne", "Rapport de contexte (SWOT, PESTEL mis à jour)"),
            ("3.", "Retours sur la performance du SMSI (KPIs)", "Tableau de bord mensuel"),
            ("4.", "Résultats des audits internes et externes", "Rapports d'audit + PAC"),
            ("5.", "Non-conformités et actions correctives", "Registre des NC"),
            ("6.", "Résultats de la surveillance et des mesures", "Rapports de monitoring SIEM, scans"),
            ("7.", "Résultats de l'appréciation des risques", "PTR mis à jour"),
            ("8.", "Opportunités d'amélioration continue", "Liste des propositions RSSI + métiers"),
        ]),
        ("SORTIES ATTENDUES (Décisions de direction)", BLUE1, [
            ("A.", "Opportunités d'amélioration du SMSI", "Actions décidées avec responsables et délais"),
            ("B.", "Besoins de modifier le SMSI (politique, périmètre)", "Décisions documentées"),
            ("C.", "Besoins en ressources (budget, personnel)", "Allocations budgétaires validées"),
            ("D.", "Décisions sur la politique et objectifs SI", "Politique mise à jour si nécessaire"),
        ]),
    ]

    current_row = 4
    for section_t, color, items in inputs:
        ws_rd.merge_cells(f"A{current_row}:E{current_row}")
        c = ws_rd.cell(row=current_row, column=1, value=section_t)
        c.fill = fill(color); c.font = font(bold=True, size=12, color=WHITE)
        ws_rd.row_dimensions[current_row].height = 28
        current_row += 1

        header_row(ws_rd, current_row,
                   [("N°", 5), ("Point à l'ordre du jour", 55),
                    ("Documents d'entrée requis", 45), ("Décision / Commentaire", 45),
                    ("Responsable / Délai", 22)],
                   fill_color=GREY1, font_size=9)
        ws_rd.row_dimensions[current_row].height = 28
        current_row += 1

        for num, point, docs in items:
            ws_rd.row_dimensions[current_row].height = 35
            for c_idx, val in enumerate([num, point, docs, "", ""], start=1):
                cell = ws_rd.cell(row=current_row, column=c_idx, value=val)
                cell.border = border_thin()
                cell.font = font(size=9)
                cell.alignment = align("center" if c_idx == 1 else "left", "center")
                if current_row % 2 == 0: cell.fill = fill(LGREY)
            current_row += 1
        current_row += 1

    # Signature
    ws_rd.merge_cells(f"A{current_row}:B{current_row}")
    ws_rd.cell(row=current_row, column=1, value="Approuvé par (Direction Générale) :").font = font(bold=True, size=11)
    ws_rd.merge_cells(f"D{current_row}:E{current_row}")
    ws_rd.cell(row=current_row, column=4, value="Signature RSSI :").font = font(bold=True, size=11)

    wb.save("/home/user/CyberResilience-/5_Tableau_Bord_SMSI.xlsx")
    print("✓ 5_Tableau_Bord_SMSI.xlsx généré")


if __name__ == "__main__":
    print("Génération des fichiers Excel SMSI ISO 27001:2022 / Loi 05-20 / DNSSI v2...")
    build_dda()
    build_ptr()
    build_incidents()
    build_audit()
    build_dashboard()
    print("\n✅ Tous les fichiers ont été générés avec succès !")
    print("   1_DdA_ISO27001_2022.xlsx")
    print("   2_Plan_Traitement_Risques.xlsx")
    print("   3_Registre_Incidents.xlsx")
    print("   4_Programme_Audit_Interne.xlsx")
    print("   5_Tableau_Bord_SMSI.xlsx")
