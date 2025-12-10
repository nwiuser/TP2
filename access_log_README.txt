═══════════════════════════════════════════════════════════════════════
        FICHIER ACCESS.LOG - EXERCICE NEWSHUB MEDIA
═══════════════════════════════════════════════════════════════════════
---------------------------------
CARACTÉRISTIQUES DU FICHIER
---------------------------------
Nom du fichier    : access.log
Nombre de lignes  : 500 000
Taille            : ~105 MB
Format            : Apache Combined Log Format
Période couverte  : 30 derniers jours
Encodage          : UTF-8


---------------------------------
 FORMAT DES LOGS APACHE
---------------------------------

Chaque ligne suit le format :
IP - - [Date] "Méthode URL Protocole" Code_HTTP Taille Referrer User-Agent

Exemple :
66.249.66.1 - - [16/Oct/2025:15:15:55 +0000] "GET /article/news-2025-10-0045 HTTP/1.1" 200 23146 "-" "Mozilla/5.0 (compatible; Googlebot/2.1)"

---------------------------------
COMPOSITION DU TRAFIC
---------------------------------

• Googlebot     : ~35% (175 000 requêtes)
• Visiteurs     : ~60% (300 000 requêtes)
• Bingbot       : ~5%  (25 000 requêtes)

---------------------------------
TYPES DE PAGES CRAWLÉES
---------------------------------

1. Articles récents       : /article/news-YYYY-MM-NNNN
   - Années : 2024, 2025
   - ~30% du trafic

2. Articles archivés      : /archive/YYYY/article-NNNN
   - Années : 2020-2022
   - ~15% du trafic
   - ATTENTION : Certaines pages retournent 404

3. Pages de pagination    : /category/{tech|sport|politique}?page=N
   - Jusqu'à 50 pages par catégorie
   - ~20% du trafic
   - PROBLÈME : Consomme beaucoup de crawl budget

4. Page d'accueil         : /, /index.html, /home
   - ~10% du trafic

5. URLs obsolètes (404)   : /old-article-N, /deleted-page-N
   - ~8% du trafic
   - PROBLÈME : Gaspillage de crawl budget

6. Redirections (301)     : /old-url-N
   - ~7% du trafic

7. Fichiers statiques     : /css/*, /js/*, /robots.txt, /sitemap.xml
   - ~10% du trafic

---------------------------------
CODES HTTP
---------------------------------

200 (OK)                : ~70% des requêtes
301 (Redirect permanent): ~10%
302 (Redirect temporaire): ~3%
304 (Not Modified)      : ~5%
404 (Not Found)         : ~10% ⚠️ PROBLÈME
500 (Server Error)      : ~2%

---------------------------------
ADRESSES IP GOOGLEBOT (authentiques)
---------------------------------

66.249.66.x
66.249.79.x
66.249.64.x

Identification : User-Agent contient "Googlebot"


🚨 PROBLÈMES À IDENTIFIER DANS L'EXERCICE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. ❌ Taux d'erreur 404 élevé (~10%)
   → Impact : Googlebot perd du temps sur des pages inexistantes

2. ❌ Crawl excessif sur pagination
   → Impact : Budget crawl gaspillé sur pages de faible valeur

3. ❌ Archives anciennes crawlées inutilement
   → Impact : Ressources serveur consommées pour contenu obsolète

4. ❌ Redirections 301 multiples
   → Impact : Ralentit le crawl, mauvaise UX

5. ❌ Pages obsolètes toujours accessibles
   → Impact : Dilue l'autorité du site

---------------------------------
ANALYSES ATTENDUES
---------------------------------

1. Filtrer uniquement les requêtes Googlebot
2. Calculer le nombre de crawls par jour/heure
3. Identifier les Top 20 URLs les plus crawlées
4. Mesurer le taux d'erreur 404 pour Googlebot
5. Analyser la distribution par profondeur d'URL
6. Détecter les patterns de pagination excessive
7. Quantifier le temps perdu sur pages obsolètes

---------------------------------
MÉTRIQUES CLÉS À EXTRAIRE
---------------------------------

• Total crawls Googlebot
• Crawls/jour (moyenne, min, max)
• Top 50 URLs crawlées
• % erreurs 404
• % redirections 301/302
• Répartition par type de page
• Pages obsolètes crawlées

---------------------------------
COMMANDES UTILES POUR EXPLORATION
---------------------------------

# Compter les lignes
wc -l access.log

# Filtrer Googlebot uniquement
grep -i "googlebot" access.log > googlebot_only.log

# Compter les erreurs 404
grep " 404 " access.log | wc -l

# Top 10 URLs les plus fréquentes
awk '{print $7}' access.log | sort | uniq -c | sort -rn | head -10

# Répartition par code HTTP
awk '{print $9}' access.log | sort | uniq -c | sort -rn

# Extraire les IPs uniques
awk '{print $1}' access.log | sort -u | wc -l


---------------------------------
Etape à suivre 
---------------------------------
1. Charger le fichier avec Pandas
2. Parser chaque ligne avec regex
3. Filtrer sur User-Agent contenant "googlebot"
4. Créer des visualisations (Matplotlib/Plotly)
5. Générer des recommandations basées sur les données



