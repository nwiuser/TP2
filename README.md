# 🎯 Jumia SEO Audit - Système Complet de Scraping et d'Analyse

## 📋 Vue d'ensemble

Ce projet automatise le scraping des données produit depuis **Jumia.ma** (catégorie Électronique) et fournit un audit complet des critères SEO pour optimiser la crawlabilité de Googlebot.

**Architecture modulaire & professionnelle:**
- ✅ **Scraper.py** (265 lignes) - Extraction 13 métriques SEO
- ✅ **Validator.py** (450+ lignes) - Validation 6 critères SEO  
- ✅ **Analyzer.py** (500+ lignes) - Analyse & 5 visualisations
- ✅ **main.py** (230 lignes) - Orchestration workflow complet

---

## 🚀 Installation Rapide

### 1. Prérequis
```bash
Python 3.8+  # Vérifier: python --version
```

### 2. Installation des dépendances
```bash
pip install -r requirements.txt
```

Ou installation manuelle:
```bash
pip install requests beautifulsoup4 pandas matplotlib plotly
```

### 3. Dépendances installées
```
✅ requests        >= 2.28.0   (HTTP requests)
✅ beautifulsoup4  >= 4.11.0   (HTML parsing)
✅ pandas          >= 1.5.0    (Data processing)
✅ matplotlib      >= 3.6.0    (Static plots)
✅ plotly          >= 5.11.0   (Interactive charts)
```

---

## 💻 Utilisation - Démarrage Rapide

### Mode 1: Execution Complète (Recommandé)
```bash
python main.py

# Workflow automatique:
# 1. Demande le nombre de pages (1-100)
# 2. Scrape les données
# 3. Valide les critères SEO
# 4. Génère rapports & visualisations
# 5. Affiche résumé final
```

**Exemple d'exécution:**
```
🎯 JUMIA SEO AUDIT - SYSTÈME COMPLET
Nombre de pages à scraper (1-100, défaut: 5): 5

[1/3] SCRAPING - Extraction des données Jumia
🕷️  Scraping 5 pages depuis jumia.ma/electronique/
✅ Scraping complété
  • 40 produits extraits

[2/3] VALIDATION - Vérification des critères SEO
✅ Validation 40 produits
✅ Validation complétée
  • Taux réussite: 70%
  • Produits avec erreurs: 12

[3/3] ANALYSE - Génération des rapports et visualisations
📊 Analyse 40 produits
✅ WORKFLOW COMPLET TERMINÉ!

📁 FICHIERS GÉNÉRÉS:
  • CSV: seo_analysis_output/jumia_audit_seo.csv
  • PNG: seo_analysis_output/jumia_dashboard.png
  • JSON: seo_validation_report.json
```

### Mode 2: Tests Individuels
```bash
# Tester le scraper seul (5 pages)
python test_scraper.py
# Génère: jumia_audit.json, jumia_audit.csv

# Tester le validateur seul
python test_seo_validator.py
# Génère: seo_validation_report.json

# Tester l'analyseur seul
python test_seo_analyzer.py
# Génère: seo_analysis_output/ avec tous les rapports
```

---

## 📂 Structure du Projet

```
├── scraper.py                    # Classe JumiaScraper
├── validator.py                  # Classes LogValidator & SEOValidator
├── analyzer.py                   # Classes LogAnalyzer & SEOAnalyzer
│
├── test_scraper.py              # Test du scraper (5 pages)
├── test_seo_validator.py        # Test du validateur SEO
├── test_seo_analyzer.py         # Test de l'analyseur SEO
│
├── jumia_audit.json             # Données brutes scrappées
├── jumia_audit.csv              # Données en format CSV
│
└── seo_analysis_output/         # Répertoire d'analyse
    ├── jumia_audit_seo.csv      # Données avec statuts SEO
    ├── error_distribution.html  # Histogramme des erreurs
    ├── top_problematic_pages.html
    ├── error_types_pie.html     # Pie chart des erreurs
    ├── score_distribution.html
    ├── simulation_improvements.html
    └── jumia_dashboard.png      # Dashboard complet
```

---

## 🔍 **Module 1: JumiaScraper**

### Description
Scrape les données des produits depuis `https://www.jumia.ma/electronique/`

### Utilisation
```python
from scraper import JumiaScraper

# Initialiser
scraper = JumiaScraper()

# Scraper 5 pages
products = scraper.scrape_products(max_pages=5)

# Exporter
scraper.save_to_json('jumia_audit.json')
scraper.save_to_csv('jumia_audit.csv')
```

### Données extraites (13 métriques)
| Métrique | Description |
|----------|-------------|
| `url` | URL du produit |
| `title` | Titre du produit |
| `title_length` | Longueur du titre (caractères) |
| `meta_description` | Description meta |
| `meta_description_length` | Longueur meta (caractères) |
| `h1_count` | Nombre de balises H1 |
| `h1_content` | Contenu des H1 |
| `h2_count` | Nombre de balises H2 |
| `total_images` | Total images page |
| `images_without_alt` | Images sans attribut ALT |
| `word_count` | Nombre total de mots |
| `description_word_count` | Mots dans description |
| `price` | Prix du produit |
| `category` | Catégorie produit |

### Exécution
```bash
python test_scraper.py
```

---

## ✔️ **Module 2: SEOValidator**

### Description
Valide les critères SEO selon les bonnes pratiques

### Règles SEO
| Critère | Règle | Status |
|---------|-------|--------|
| **Title** | 40-70 caractères | ✓/✗ |
| **Meta Description** | ≥120 caractères, présente | ✓/✗ |
| **H1** | Exactement 1 par page | ✓/✗ |
| **H2** | Minimum 2 | ✓/✗ |
| **Images ALT** | Max 30% sans ALT | ✓/✗ |
| **Contenu** | Minimum 150 mots | ✓/✗ |

### Utilisation
```python
from validator import SEOValidator

# Initialiser avec les données
validator = SEOValidator(products_list)

# Valider tous les produits
results = validator.validate_all_products()

# Récupérer les données
failed = validator.get_failed_products()
summary = validator.get_error_summary()

# Exporter
validator.save_validation_report('seo_validation.json')
```

### Output
Pour chaque produit:
- ✅ **Score global** (0-100%)
- ✅ **Nombre d'erreurs** (0-6)
- ✅ **Statut** (OK/ERREUR)
- ✅ **Détail par critère**

### Exécution
```bash
python test_seo_validator.py
```

---

## 📊 **Module 3: SEOAnalyzer**

### Description
Analyse les résultats de validation et génère rapports & visualisations

### Fonctionnalités

#### 1. **CSV Export**
```
jumia_audit_seo.csv
- URL, Title, Score Global, Nombre Erreurs, Statut
- Colonnes séparées pour chaque critère SEO
```

#### 2. **Visualisations Interactives (HTML)**

##### 📈 Error Distribution
- Histogramme du nombre d'erreurs par produit
- Identifie les patterns d'erreurs courants

##### 🔴 Top Problematic Pages
- Bar chart des 15 pages avec le plus d'erreurs
- Coloration par score SEO (gradient)

##### 🥧 Error Types Pie Chart
- Répartition des erreurs par type
- Identifie les critères les plus problématiques

##### 📉 Score Distribution
- Histogramme des scores SEO
- Visualise la qualité globale

##### 🚀 Simulation d'Amélioration
- Projette l'impact des corrections
- Avant/après overlay
- Statistiques d'amélioration potentielle

#### 3. **Dashboard PNG**
```
jumia_dashboard.png (2000x1500px @ 150dpi)
- Distribution des scores (histogramme)
- Erreurs par type (bar chart)
- Top 10 pages problématiques
- Répartition OK/ERREUR (pie chart)
- Statistiques globales
```

### Utilisation
```python
from analyzer import SEOAnalyzer

# Initialiser avec les résultats de validation
analyzer = SEOAnalyzer(validation_results)

# Générer TOUT
analyzer.generate_all_analysis()

# Ou individuellement:
analyzer.save_to_csv()
analyzer.plot_error_distribution()
analyzer.plot_top_problematic_pages(n=15)
analyzer.plot_error_types_pie()
analyzer.simulate_improvements()
analyzer.create_dashboard_png()
```

### Statistiques Générées
```
- Total produits analysés
- Produits avec erreurs
- Taux de réussite global (%)
- Score moyen / min / max
- Nombre moyen d'erreurs
- Détails par type d'erreur
```

### Exécution
```bash
python test_seo_analyzer.py
```

---

## 🎯 **Workflow Complet**

### Étape 1: Scraper les données
```bash
python test_scraper.py
# Génère: jumia_audit.json, jumia_audit.csv
```

### Étape 2: Valider SEO
```bash
python test_seo_validator.py
# Génère: seo_validation_report.json
```

### Étape 3: Analyser & Générer Rapports
```bash
python test_seo_analyzer.py
# Génère tout dans seo_analysis_output/
```

---

## 📈 Exemple d'Output

### Console Output
```
✓ 40 produits chargés depuis jumia_audit.json

[2/2] VALIDATION SEO

======================================================================
VALIDATION SEO DE TOUS LES PRODUITS
======================================================================

Produit 1/40: OK | Score: 83.3% | Erreurs: 1
Produit 2/40: OK | Score: 100.0% | Erreurs: 0
...

======================================================================
RÉSUMÉ DES ERREURS
======================================================================
  Meta Description: 8 erreurs (20.0%)
  Images ALT: 5 erreurs (12.5%)
  Content: 3 erreurs (7.5%)
  ...
  Taux de réussite global: 78.5%
======================================================================
```

### Fichiers Générés
```
✓ Données sauvegardées dans seo_analysis_output/jumia_audit_seo.csv
✓ Graphique créé: seo_analysis_output/error_distribution.html
✓ Graphique créé: seo_analysis_output/top_problematic_pages.html
✓ Graphique créé: seo_analysis_output/error_types_pie.html
✓ Graphique créé: seo_analysis_output/score_distribution.html
✓ Graphique de simulation créé: seo_analysis_output/simulation_improvements.html
✓ Dashboard PNG créé: seo_analysis_output/jumia_dashboard.png
```

---

## 🔧 Configuration Avancée

### Modifier le nombre de pages
```python
scraper.scrape_products(max_pages=100)  # 100 pages au lieu de 5
```

### Ajouter de nouveaux critères SEO
```python
# Dans validator.py, ajouter à RULES:
'nouveau_critere': {
    'param': 'valeur',
    'description': '...'
}

# Ajouter méthode:
def validate_nouveau_critere(self, product: Dict) -> Dict:
    # ...
```

### Personnaliser l'analyse
```python
analyzer.plot_error_distribution()  # Seulement distribution
analyzer.create_dashboard_png('custom_dashboard.png')  # Custom nom
```

---

## 📋 Critères de Succès

- ✅ Score SEO > 80% = Page optimisée
- ⚠️ Score SEO 50-80% = Nécessite améliorations
- ❌ Score SEO < 50% = Problèmes majeurs

### Recommandations d'amélioration
1. **Title** - Viser 50-60 caractères
2. **Meta Description** - Min 120, idéal 150-160
3. **H1** - Exactement 1, unique par page
4. **H2** - Min 2-3, structurer le contenu
5. **Images ALT** - 100% couverture ALT recommandée
6. **Contenu** - Min 300 mots pour produit

---

## 🐛 Dépannage

### Erreur: "No products found"
- Vérifier la disponibilité de jumia.ma
- Augmenter le timeout dans requests

### JSON parse error
- Vérifier la structure du JSON
- Vérifier l'encodage UTF-8

### PNG not created
- Vérifier les permissions d'écriture
- Vérifier matplotlib installation

---

## 📝 Notes

- **Rate limiting**: 2 secondes entre les requêtes
- **User-Agent**: JumiaSEOAudit/1.0 (custom)
- **Encoding**: UTF-8 throughout
- **Target**: https://www.jumia.ma/electronique/

---

## 📄 Licence

Projet éducatif - Audit SEO Jumia

**Auteur**: AI Assistant  
**Date**: Décembre 2025
- `parse_log_file()`: Parse le fichier et retourne un DataFrame
- `get_stats()`: Retourne les statistiques générales

**Exemple d'usage:**
```python
from scraper import LogScraper

scraper = LogScraper('access.log')
df = scraper.parse_log_file()
stats = scraper.get_stats()
```

### ✔️ `validator.py`
**Validation et nettoyage des données**

**Classes:**
- `LogValidator`: Valide et filtre les données

**Méthodes principales:**
- `filter_googlebot()`: Filtre les requêtes Googlebot (User-Agent + IP)
- `filter_errors()`: Sépare les requêtes réussies des erreurs
- `identify_404_errors()`: Identifie les erreurs 404
- `identify_301_redirects()`: Identifie les redirections 301
- `identify_server_errors()`: Identifie les erreurs serveur (500+)

**Exemple d'usage:**
```python
from validator import LogValidator

validator = LogValidator(df)
googlebot_df = validator.filter_googlebot()
errors_404 = validator.identify_404_googlebot(googlebot_df)
report = validator.get_validation_report()
```

### 📊 `analyzer.py`
**Analyse des données et génération de rapports**

**Classes:**
- `LogAnalyzer`: Analyse les logs et génère des insights

**Méthodes principales:**
- `get_top_urls(n=20)`: Top N URLs crawlées
- `get_crawls_by_day()`: Crawls par jour
- `get_crawls_by_hour()`: Crawls par heure
- `get_http_distribution()`: Distribution des codes HTTP
- `analyze_url_types()`: Analyse les types d'URLs
- `detect_pagination_crawling()`: Détecte le crawling excessif
- `get_obsolete_urls()`: Identifie les URLs obsolètes
- `generate_all_reports()`: Génère tous les graphiques

**Exemple d'usage:**
```python
from analyzer import LogAnalyzer

analyzer = LogAnalyzer(googlebot_df)
top_urls = analyzer.get_top_urls(20)
url_types = analyzer.analyze_url_types()
analyzer.generate_all_reports()
```

### 🎯 `main.py`
**Point d'entrée principal orchestrant l'analyse complète**

Exécute les 4 étapes:
1. **Extraction** des données (Scraper)
2. **Validation** et filtrage (Validator)
3. **Analyse** des données (Analyzer)
4. **Génération** des visualisations (Graphiques)

## 📈 Analyses réalisées

### 1. Filtrage Googlebot
- Filtre par User-Agent "googlebot"
- Vérifie les IPs authentiques (66.249.x.x)
- Calcule le pourcentage de trafic Googlebot

### 2. Erreurs et Redirections
- Identifie les erreurs 404 (pages inexistantes)
- Mesure les redirections 301 et 302
- Détecte les erreurs serveur (500+)

### 3. Analyse des URLs
- Top 20 URLs les plus crawlées
- Répartition par type (articles, archives, pagination, etc.)
- Identification des URLs obsolètes

### 4. Tendances temporelles
- Crawls par jour (moyenne, min, max)
- Distribution par heure
- Évolution temporelle

### 5. Patterns de pagination
- Détecte le crawling excessif des pages de pagination
- Identifie les catégories problématiques

## 🎨 Visualisations générées

Tous les graphiques sont interactifs (Plotly HTML):

1. **top_urls.html** - Top 20 URLs crawlées (graphique en barres)
2. **crawls_by_day.html** - Tendance journalière (courbe)
3. **crawls_by_hour.html** - Distribution horaire (histogramme)
4. **http_distribution.html** - Codes HTTP (camembert)
5. **url_types.html** - Types d'URLs (camembert)

## 🎯 Problèmes identifiés et recommandations

### ⚠️ Taux d'erreur 404 élevé
**Problème:** ~10% des crawls Googlebot retournent 404  
**Impact:** Gaspillage du crawl budget  
**Solutions:**
- Identifier les URLs 404 et les rediriger (301)
- Ou mettre à jour les liens internes
- Ou supprimer/archiver le contenu

### ⚠️ Pagination excessive
**Problème:** Googlebot crawle trop de pages de pagination  
**Impact:** Consommation inutile du crawl budget  
**Solutions:**
- Ajouter `rel="nofollow"` sur liens pagination
- Utiliser `rel="next"` et `rel="prev"` sur pages paginées
- Bloquer pagination dans robots.txt

### ⚠️ Archives obsolètes
**Problème:** Contenu ancien toujours crawlé  
**Impact:** Perte d'autorité du site  
**Solutions:**
- Rediriger archives vers contenu actif (301)
- Ou bloquer dans robots.txt: `Disallow: /archive/`

### ⚠️ Redirections excessives
**Problème:** 301/302 consomment du crawl budget  
**Impact:** Ralentit l'exploration  
**Solutions:**
- Mettre à jour liens internes
- Mettre en cache des redirections

## 📊 Exemple de sortie

```
======================================================================
ANALYSE DES LOGS - NEWSHUB MEDIA
======================================================================

[1/4] ÉTAPE 1: EXTRACTION DES DONNÉES
----------------------------------------------------------------------
✓ 500000 lignes parsées avec succès

📊 Statistiques générales:
  - Total lignes: 500,000
  - IPs uniques: 1,234
  - URLs uniques: 5,678
  - Période: 01/Oct/2025:00:00:00 +0000 à 31/Oct/2025:23:59:59 +0000
  - Méthodes HTTP: {'GET': 490000, 'HEAD': 10000}

[2/4] ÉTAPE 2: VALIDATION ET FILTRAGE
----------------------------------------------------------------------
✓ 175000 requêtes Googlebot trouvées (35.00%)
✓ Erreurs 404 (Googlebot): 17500 (10.00%)
✓ Redirections 301: 17500 (10.00%)

[3/4] ÉTAPE 3: ANALYSE DES DONNÉES
----------------------------------------------------------------------
🔝 Top 20 URLs crawlées par Googlebot:
  1. /article/news-2025-10-0045: 1,234 crawls
  2. /article/news-2025-10-0044: 1,200 crawls
  ...

[4/4] ÉTAPE 4: GÉNÉRATION DES VISUALISATIONS
----------------------------------------------------------------------
✓ Graphique sauvegardé: analysis_output/top_urls.html
✓ Graphique sauvegardé: analysis_output/crawls_by_day.html
✓ Graphique sauvegardé: analysis_output/http_distribution.html
✓ Graphique sauvegardé: analysis_output/url_types.html
✓ Graphique sauvegardé: analysis_output/crawls_by_hour.html

✓ Tous les rapports ont été générés avec succès!

======================================================================

## 📊 Résultats Obtenus (Exemple: 5 pages = 40 produits)

### Statistiques Globales
```
✅ AUDIT COMPLÉTÉ:
  • Produits analysés: 40
  • Avec erreurs: 12 (30%)
  • Score moyen: 78.5%
  • Taux réussite: 70%
  
🎯 CONFORMITÉ PAR CRITÈRE:
  ✅ H1 Structure: 95% conforme
  ✅ H2 Structure: 92% conforme
  ⚠️  Meta Description: 80% conforme (8 erreurs)
  ⚠️  Images ALT: 87.5% conforme (5 erreurs)
  ⚠️  Contenu: 92.5% conforme (3 erreurs)
  ✅ Title: 95% conforme (2 erreurs)
```

### Fichiers Générés
```
📁 seo_analysis_output/
├── jumia_audit_seo.csv              # Données avec statuts
├── jumia_dashboard.png              # Dashboard visuel
├── error_distribution.html          # Histogramme
├── top_problematic_pages.html       # Top 15
├── error_types_pie.html             # Pie chart
├── score_distribution.html          # Distribution
└── simulation_improvements.html     # Avant/après

📄 seo_validation_report.json        # Validation JSON
📄 jumia_executive_summary.txt       # Résumé exécutif
```

---

## 🤖 Notes sur Respect des Robots.txt et Éthique

### Conformité et Bonnes Pratiques

**✅ Système respecte les standards:**

1. **Rate Limiting**
   - Délai: 2 secondes entre chaque requête
   - Évite la surcharge serveur
   - Respecte les ressources

2. **User-Agent Transparent**
   - Identifiant: `JumiaSEOAudit/1.0`
   - Permet au propriétaire de monitorer
   - Clairement identifiable

3. **Accès Public Uniquement**
   - Scrape pages publiques seulement
   - Catégorie: `/electronique/` (public)
   - Aucune donnée sensible/protégée

4. **Respect des Directives robots.txt**
   - ✅ Respecte les directives `robots.txt`
   - ✅ Respecte `Crawl-delay`
   - ✅ Respecte `User-agent` spécifiques

5. **Limitation de Portée**
   - Max 100 pages (sécurité intégrée)
   - Défaut: 5 pages (mode test)
   - Pas de scraping exhaustif sans accord

### ⚠️ Avant d'Utiliser en Production

**1. Vérifier robots.txt**
```bash
# Consulter: https://www.jumia.ma/robots.txt
# Respecter les directives Disallow/Crawl-delay
```

**2. Obtenir Autorisation si Nécessaire**
- Contactez Jumia pour scraping intensif
- Respectez les conditions d'utilisation
- Éviter concurrence déloyale

**3. Monitorer l'Impact**
- Vérifier server logs pour charge
- Augmenter délai si nécessaire (>2sec)
- Limiter pages scrapées selon besoins

**4. Usage Éthique Uniquement**
- ✅ Audit personnel/interne
- ✅ Recherche académique
- ❌ Concurrence déloyale
- ❌ Revente de données
- ❌ Scraping sans autorisation

### Configuration Responsable

```python
from scraper import JumiaScraper

# Configuration sécurisée:
scraper = JumiaScraper()
# - Rate limiting: 2 secondes ✓
# - User-Agent: JumiaSEOAudit/1.0 ✓
# - Pages max: 10 (pour test) ✓

products = scraper.scrape_products(max_pages=10)
```

---

## 📚 Documentation Supplémentaire

- **QUICK_START.md** - Démarrage rapide 5 min
- **COMPLETION_REPORT.md** - Rapport technique détaillé
- **jumia_executive_summary.txt** - Résumé exécutif audit

======================================================================

## 🛠️ Dépannage

| Problème | Solution |
|----------|----------|
| "No products found" | Vérifier disponibilité Jumia.ma |
| JSON parse error | Vérifier encoding UTF-8 |
| PNG not created | Vérifier permissions écriture |
| Timeout | Augmenter timeout requests |

## 📝 Notes Techniques

- **Target:** https://www.jumia.ma/electronique/
- **Rate limiting:** 2 secondes entre requêtes
- **User-Agent:** JumiaSEOAudit/1.0
- **Encoding:** UTF-8 throughout
- **Max pages:** 100 (configurable)
- **Extraction:** JSON depuis window.__STORE__

## 👤 Auteur

TP02 - Web Marketing & CRM - Audit SEO Jumia v1.0

## 📄 Licence

Projet éducatif - Audit SEO - Décembre 2025

======================================================================

## RECOMMANDATIONS

1. 🔴 ERREURS 404 ÉLEVÉES
   ⚠️  10.00% des crawls Googlebot retournent 404
   → Action: Vérifier les URLs cassées et rediriger ou supprimer
   → Impact SEO: Perte de crawl budget

2. 📄 PAGINATION EXCESSIVE
   ⚠️  Crawling excessif sur pages de pagination
   → Action: Ajouter nofollow sur liens de pagination
   → Action: Utiliser rel=next/prev sur pages de pagination

3. 🗑️  CONTENU OBSOLÈTE
   ⚠️  1,234 URLs obsolètes crawlées
   → Action: Rediriger vers contenu actif (HTTP 301)
   → Action: Ou bloquer avec robots.txt

4. 🔄 REDIRECTIONS
   ⚠️  10.00% redirections 301
   → Action: Mettre à jour les liens internes

======================================================================
```

## 🛠️ Dépannage

### Erreur: "Fichier non trouvé: access.log"
Assurez-vous que le fichier `access.log` est dans le même dossier que les scripts Python.

### Erreur: Module pandas introuvable
```bash
pip install pandas
```

### Erreur: Memory (fichier trop volumineux)
Pour les fichiers > 1GB, utiliser chunks:
```python
chunks = pd.read_csv('access.log', chunksize=10000)
```

## 📝 Notes

- Le fichier access.log contient 500k lignes (~105MB)
- Format: Apache Combined Log Format
- Période couverte: 30 derniers jours
- Encodage: UTF-8

## 👤 Auteur

TP02 - Web Marketing & CRM - Analyse des logs Googlebot

## 📄 Licence

Ce projet est fourni à titre éducatif.
