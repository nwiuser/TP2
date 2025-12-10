"""
test_log_analyzer.py - Test du parseur et analyseur de logs
"""

from log_analyzer import LogAnalyzer
import pandas as pd


def main():
    """Lance l'analyse complète"""
    
    print("\n" + "="*70)
    print("🔍 TEST LOG ANALYZER - GOOGLEBOT AUDIT")
    print("="*70)
    
    # Initialiser l'analyseur
    analyzer = LogAnalyzer('access_log.txt')
    
    # Parser le fichier
    df = analyzer.parse_log_file()
    if df is None or df.empty:
        print("❌ Erreur: Impossible de parser le fichier")
        return
    
    # Afficher statistiques globales
    print("\n" + "="*70)
    print("📊 STATISTIQUES GLOBALES")
    print("="*70)
    stats = analyzer.get_statistics()
    for key, value in stats.items():
        print(f"  • {key:25s}: {value}")
    
    # Analyse temporelle
    print("\n" + "="*70)
    print("📅 DISTRIBUTION TEMPORELLE")
    print("="*70)
    by_day, by_hour = analyzer.analyze_temporal_distribution()
    
    if not by_day.empty:
        print("\n📆 Crawls par jour (top 10):")
        print(by_day.head(10).to_string(index=False))
    
    if not by_hour.empty:
        print("\n⏰ Crawls par heure:")
        print(by_hour.to_string(index=False))
    
    # Top URLs
    print("\n" + "="*70)
    print("🔝 TOP 20 URLS CRAWLEES")
    print("="*70)
    top_urls = analyzer.get_top_urls(20)
    if not top_urls.empty:
        for idx, (_, row) in enumerate(top_urls.iterrows(), 1):
            print(f"  {idx:2d}. {row['url'][:60]:60s} -> {row['crawl_count']:5,} crawls")
    
    # Codes HTTP
    print("\n" + "="*70)
    print("⚠️  ANALYSE DES CODES HTTP")
    print("="*70)
    status_stats = analyzer.analyze_status_codes()
    print(f"\n  Distribution:")
    for code in sorted(status_stats['status_distribution'].keys()):
        count = status_stats['status_distribution'][code]
        pct = round(count / status_stats['total_requests'] * 100, 2)
        print(f"    {code} -> {count:6,} ({pct:5.2f}%)")
    
    # Profondeur
    print("\n" + "="*70)
    print("📏 ANALYSE DE PROFONDEUR")
    print("="*70)
    depth_stats = analyzer.analyze_url_depth()
    print(f"  • Profondeur moyenne: {depth_stats['average_depth']}")
    print(f"  • Min/Max: {depth_stats['min_depth']}/{depth_stats['max_depth']}")
    print(f"  • Plus courante: {depth_stats['most_common_depth']}")
    print(f"\n  Distribution:")
    for depth in sorted(depth_stats['depth_distribution'].keys()):
        count = depth_stats['depth_distribution'][depth]
        print(f"    Niveau {depth}: {count:6,} URLs")
    
    # URLs obsolètes
    print("\n" + "="*70)
    print("🗑️  URLS OBSOLETES")
    print("="*70)
    obsolete = analyzer.find_obsolete_urls()
    if obsolete:
        for url, count in obsolete[:10]:
            print(f"  • {url[:60]:60s} -> {count:,} crawls")
    else:
        print("  ✅ Aucune URL obsolète trouvée")
    
    # KPIs
    print("\n" + "="*70)
    print("📈 KPIs PRINCIPAUX")
    print("="*70)
    kpis = analyzer.calculate_kpis()
    for key, value in kpis.items():
        if isinstance(value, dict):
            print(f"  • {key:30s}: {len(value)} éléments")
        else:
            print(f"  • {key:30s}: {value}")
    
    # Rapport complet
    print("\n" + analyzer.generate_report())
    
    # Exporter les données
    print("\n" + "="*70)
    print("💾 EXPORT DES DONNEES")
    print("="*70)
    
    try:
        # CSV des logs Googlebot
        analyzer.googlebot_df.to_csv('googlebot_logs.csv', index=False)
        print("  ✅ googlebot_logs.csv créé")
        
        # CSV des top URLs
        top_urls.to_csv('top_urls.csv', index=False)
        print("  ✅ top_urls.csv créé")
        
        # CSV de la distribution temporelle
        by_day.to_csv('crawls_per_day.csv', index=False)
        print("  ✅ crawls_per_day.csv créé")
    except Exception as e:
        print(f"  ❌ Erreur export: {e}")


if __name__ == "__main__":
    main()
