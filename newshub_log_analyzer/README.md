# Newsroom Googlebot Crawl Analysis System

Analyse des logs Apache pour optimiser le crawl Googlebot et identifier les opportunités d'amélioration SEO.

## 🎯 Objectifs

- **Analyser les patterns de crawl** de Googlebot sur votre site
- **Identifier les pages problématiques** (404, 500, pages obsolètes)
- **Optimiser le budget de crawl** pour maximiser l'indexation
- **Générer des rapports CSV et dashboards interactifs**

## 📋 Features

✅ **Parsing Apache Combined Log Format**
- Extraction de: IP, date/heure, méthode, URL, protocole, code HTTP, User-Agent
- Détection Googlebot automatique
- Gestion des erreurs de parsing

✅ **Analyse Approfondie**
- Distribution temporelle (par jour/heure)
- Top URLs crawlées par Googlebot
- Taux d'erreurs (4xx/5xx) par URL
- Distribution de la profondeur des URLs
- Détection des pages obsolètes

✅ **Rapports & Visualisations**
- Export CSV détaillé (crawl_report.csv)
- Dashboard Plotly interactif (HTML)
- 5 visualisations principales

## 🚀 Installation

### Prérequis
- Python 3.8+
- pip (gestionnaire de paquets Python)

### Setup

```bash
# 1. Cloner/naviguer vers le dossier
cd newshub_log_analyzer

# 2. (Optionnel) Créer un environnement virtuel
python -m venv env
env\Scripts\activate  # Windows
source env/bin/activate  # Linux/Mac

# 3. Installer les dépendances
pip install pandas plotly

# Alternative (si plotly existe déjà):
pip install plotly  # Pour l'HTML interactif
pip install kaleido  # Pour export PNG (optionnel)
```

## 📊 Usage

### 1. Analyse Simple avec Sample Logs

```bash
python test_sample.py
```

Génère:
- `reports/crawl_report.csv` - Rapport détaillé par URL
- `reports/dashboard.html` - Dashboard interactif

### 2. Analyse Personnalisée

```python
from log_analyzer import LogAnalyzer
from report_generator import ReportGenerator

# Parser les logs
analyzer = LogAnalyzer('access.log')
df = analyzer.parse_log_file()

# Générer les rapports
generator = ReportGenerator(analyzer)
results = generator.generate_full_report()

print(f"CSV: {results['csv']}")
print(f"HTML: {results['html']}")
```

### 3. Statistiques KPI

```python
from log_analyzer import LogAnalyzer

analyzer = LogAnalyzer('access.log')
analyzer.parse_log_file()

# Statistiques générales
stats = analyzer.get_statistics()
print(f"Total requests: {stats['total_requests']}")
print(f"Googlebot requests: {stats['googlebot_requests']}")
print(f"Error rate: {stats['error_rate']:.1f}%")

# Top URLs
top_urls = analyzer.get_top_urls(20)
print(top_urls)

# Analyse d'erreurs
errors = analyzer.analyze_status_codes()
print(f"4xx errors: {errors['4xx']}")
print(f"5xx errors: {errors['5xx']}")

# Profondeur des URLs
depth = analyzer.analyze_url_depth()
print(f"Average depth: {depth['avg']:.2f}")
```

## 📈 Output Examples

### CSV Report (crawl_report.csv)

| url | crawl_count | status_codes | avg_size | depth | first_crawl | last_crawl | error_count | error_rate | is_obsolete |
|-----|-------------|--------------|----------|-------|------------|------------|------------|-----------|-----------|
| /article/news-001 | 2 | {200: 2} | 5432.0 | 1 | 2025-10-01 10:02:00 | 2025-10-01 10:04:45 | 0 | 0.0 | 0 |
| /archive/old-article | 1 | {200: 1} | 3456.0 | 1 | 2025-10-01 10:01:00 | 2025-10-01 10:01:00 | 0 | 0.0 | 1 |

### Dashboard HTML (dashboard.html)

Le dashboard contient 5 visualisations Plotly interactives:

1. **📈 Timeline** - Crawls par jour et par heure
2. **🔝 Top URLs** - Classement des 20 URLs les plus crawlées
3. **⚠️ Status Codes** - Distribution des codes HTTP (200, 404, 500, etc.)
4. **📊 URL Depth** - Histogramme de la profondeur des URLs
5. **🗑️ Obsolete Pages** - Scatter plot des pages obsolètes vs crawls

Toutes les visualisations sont **interactives** (zoom, hover, legend toggle).

## 🔍 Log Format Support

Format accepté: **Apache Combined Log Format**

```
192.168.1.1 - - [01/Jan/2025:12:34:56 +0000] "GET /article/news HTTP/1.1" 200 5432 "-" "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
```

**Colonnes extraites:**
- `ip` - Adresse IP du client
- `timestamp` - Date et heure au format datetime
- `date` - Date seule
- `hour` - Heure (0-23)
- `method` - GET, POST, etc.
- `url` - URL demandée
- `protocol` - HTTP/1.1, HTTP/2, etc.
- `status_code` - 200, 404, 500, etc.
- `size` - Taille réponse (bytes)
- `referrer` - Referrer header
- `user_agent` - User-Agent string
- `is_googlebot` - Booléen (True si Googlebot)
- `is_error` - Booléen (True si 4xx ou 5xx)
- `url_depth` - Profondeur URL (nombre de /)
- `is_obsolete` - Booléen (True si /archive/, old, deprecated)

## 📊 Analyses Disponibles

### LogAnalyzer Methods

```python
analyzer.parse_log_file()                    # Parse Apache logs
analyzer.get_statistics()                    # Stats générales
analyzer.analyze_temporal_distribution()     # Daily/hourly crawls
analyzer.get_top_urls(n=20)                  # Top N URLs
analyzer.analyze_status_codes()              # Error analysis
analyzer.analyze_url_depth()                 # URL depth stats
analyzer.find_obsolete_urls()                # Detect old pages
analyzer.calculate_kpis()                    # Compute KPIs
analyzer.generate_report()                   # Text report
```

### ReportGenerator Methods

```python
generator.export_crawl_report_csv()          # CSV export
generator.create_interactive_dashboard()     # HTML dashboard
generator.generate_full_report()             # All reports
```

## 🎯 Use Cases

### 1. Audit SEO Googlebot
```bash
python -c "
from log_analyzer import LogAnalyzer
a = LogAnalyzer('access.log')
a.parse_log_file()
print(a.generate_report())
"
```

### 2. Monitoring Continu
Exécuter quotidiennement:
```bash
#!/bin/bash
python generate_reports.py \
  --log-file /var/log/apache2/access.log \
  --output reports/daily_$(date +%Y%m%d).html
```

### 3. Détection de Problèmes
```python
# Trouver les URLs avec + de 50% d'erreurs
high_error_urls = df[df['error_rate'] > 0.5]
print(high_error_urls[['url', 'crawl_count', 'error_rate']])
```

## 🛠️ Troubleshooting

### "No module named 'plotly'"
```bash
pip install plotly
# ou utiliser l'environment virtuel:
.\env\Scripts\pip install plotly
```

### "Can't read access.log"
```
Vérifiez:
- Le chemin du fichier est correct
- Les permissions de lecture (chmod 644 access.log)
- L'encodage est UTF-8
```

### "Columns do not exist" Error
Assurez-vous que le log format est Apache Combined:
```
IP - USER [DATE] "METHOD URL PROTOCOL" STATUS SIZE "REFERRER" "USER-AGENT"
```

## 📅 Log Retention

Pour optimiser les performances:
- **Petits logs** (< 100MB): Parse complet en secondes
- **Logs moyens** (100MB-1GB): ~30-60 secondes
- **Gros logs** (> 1GB): Utilisez `tail` ou `grep` pour filtrer d'abord

```bash
# Parser seulement Googlebot requests
grep -i googlebot access.log > googlebot.log
python analyze.py googlebot.log
```

## 📝 Output Files

Les rapports sont générés dans le dossier `reports/`:

```
reports/
├── crawl_report.csv       # Rapport détaillé (CSV)
└── dashboard.html         # Dashboard interactif (HTML)
```

## 🔐 Robots.txt & Ethical Scraping

⚠️ **Important**: Ces scripts analysent vos **propres logs**, pas du web scraping.

Bonnes pratiques:
- ✅ Analyser vos propres logs Apache/Nginx
- ✅ Respecter `robots.txt` pour vos règles de crawl
- ✅ Ne pas bloquer les crawlers légitimes
- ✅ Implémenter Crawl-delay si nécessaire

## 📖 Ressources

- [Apache Log Format Documentation](https://httpd.apache.org/docs/2.4/logs.html)
- [Googlebot User-Agent String](https://support.google.com/webmasters/answer/1061943)
- [Google Search Console - Crawl Stats](https://support.google.com/webmasters/answer/7645953)
- [Plotly Documentation](https://plotly.com/python/)

## 📜 License

Ce projet est développé à des fins éducatives et de référence.

## 👨‍💻 Auteur

Développé pour l'analyse des logs Newsroom Googlebot.

---

**Questions?** Consultez les fichiers d'exemple:
- `sample_access.log` - Exemple de données de test
- `test_sample.py` - Script de test complet
