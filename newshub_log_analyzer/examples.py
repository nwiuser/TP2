"""
Advanced usage examples for Newsroom Googlebot Log Analyzer
Exemples d'utilisation avancée
"""

from log_analyzer import LogAnalyzer
from report_generator import ReportGenerator
import pandas as pd

# ============================================================
# EXEMPLE 1: Analyse Complète Simplifiée
# ============================================================

def example_1_basic_analysis():
    """Analyse simple avec rapport complet"""
    print("\n" + "="*60)
    print("EXEMPLE 1: Analyse Basique")
    print("="*60)
    
    # Parser et analyser
    analyzer = LogAnalyzer('access.log')
    analyzer.parse_log_file()
    
    # Générer rapports
    generator = ReportGenerator(analyzer)
    results = generator.generate_full_report()
    
    print(f"✅ CSV exported: {results['csv']}")
    print(f"✅ Dashboard exported: {results['html']}")


# ============================================================
# EXEMPLE 2: Filtrer Googlebot uniquement
# ============================================================

def example_2_googlebot_only():
    """Analyser seulement les crawls Googlebot"""
    print("\n" + "="*60)
    print("EXEMPLE 2: Analyse Googlebot Uniquement")
    print("="*60)
    
    analyzer = LogAnalyzer('access.log')
    df = analyzer.parse_log_file()
    
    # Filtrer Googlebot
    googlebot_df = df[df['is_googlebot']]
    
    print(f"\nTotal requests: {len(df)}")
    print(f"Googlebot requests: {len(googlebot_df)}")
    print(f"Percentage: {len(googlebot_df)/len(df)*100:.1f}%")
    
    # Top URLs crawled by Googlebot
    top_urls = googlebot_df['url'].value_counts().head(10)
    print(f"\nTop 10 URLs crawled by Googlebot:")
    for url, count in top_urls.items():
        print(f"  {count:3d}x {url}")


# ============================================================
# EXEMPLE 3: Détecter les Pages Problématiques
# ============================================================

def example_3_problem_pages():
    """Identifier les URLs avec taux d'erreur élevé"""
    print("\n" + "="*60)
    print("EXEMPLE 3: Pages Problématiques (Taux d'Erreur > 30%)")
    print("="*60)
    
    analyzer = LogAnalyzer('access.log')
    df = analyzer.parse_log_file()
    
    # Analyser les erreurs
    error_analysis = analyzer.analyze_status_codes()
    
    print(f"\nErrorr Analysis:")
    print(f"  Total 4xx errors: {error_analysis['4xx']}")
    print(f"  Total 5xx errors: {error_analysis['5xx']}")
    print(f"  Global error rate: {error_analysis['error_rate']*100:.1f}%")
    
    # URLs avec beaucoup d'erreurs
    googlebot_df = df[df['is_googlebot']].copy()
    
    if len(googlebot_df) > 0:
        # Calculer taux d'erreur par URL
        url_errors = googlebot_df.groupby('url').agg({
            'status_code': ['count', lambda x: (x >= 400).sum()]
        }).reset_index()
        url_errors.columns = ['url', 'total', 'errors']
        url_errors['error_rate'] = url_errors['errors'] / url_errors['total']
        
        # Filtrer URLs problématiques
        problem_urls = url_errors[url_errors['error_rate'] > 0.3]
        
        print(f"\n⚠️  URLs avec > 30% d'erreurs:")
        if len(problem_urls) > 0:
            for _, row in problem_urls.iterrows():
                print(f"  {row['url']}: {row['errors']}/{row['total']} ({row['error_rate']*100:.0f}%)")
        else:
            print("  ✅ Aucune URL problématique détectée")


# ============================================================
# EXEMPLE 4: Analyser la Profondeur des URLs
# ============================================================

def example_4_url_depth():
    """Vérifier la distribution de profondeur des URLs"""
    print("\n" + "="*60)
    print("EXEMPLE 4: Analyse Profondeur URLs")
    print("="*60)
    
    analyzer = LogAnalyzer('access.log')
    df = analyzer.parse_log_file()
    
    depth_analysis = analyzer.analyze_url_depth()
    
    print(f"\nProfondeur des URLs:")
    print(f"  Moyenne: {depth_analysis['avg']:.2f}")
    print(f"  Min: {depth_analysis['min']}")
    print(f"  Max: {depth_analysis['max']}")
    print(f"  Median: {depth_analysis['median']:.2f}")
    
    # Distribution
    print(f"\n  Distribution:")
    for depth, count in sorted(depth_analysis['distribution'].items()):
        bar = "█" * int(count / 10)
        print(f"    Depth {depth}: {bar} ({count})")


# ============================================================
# EXEMPLE 5: Détecter Pages Obsolètes
# ============================================================

def example_5_obsolete_pages():
    """Identifier les pages obsolètes toujours crawlées"""
    print("\n" + "="*60)
    print("EXEMPLE 5: Pages Obsolètes Détectées")
    print("="*60)
    
    analyzer = LogAnalyzer('access.log')
    df = analyzer.parse_log_file()
    
    # Pages obsolètes
    obsolete_urls = analyzer.find_obsolete_urls()
    
    print(f"\n🗑️  Pages obsolètes trouvées: {len(obsolete_urls)}")
    for url, count in obsolete_urls[:10]:
        print(f"  {count:3d}x {url}")
    
    # Pourcentage du budget de crawl
    googlebot_df = df[df['is_googlebot']]
    obsolete_count = googlebot_df[googlebot_df['is_obsolete']].shape[0]
    total_googlebot = len(googlebot_df)
    
    if total_googlebot > 0:
        pct = obsolete_count / total_googlebot * 100
        print(f"\n📊 Budget de crawl utilisé par pages obsolètes: {pct:.1f}% ({obsolete_count}/{total_googlebot})")


# ============================================================
# EXEMPLE 6: Analyse Temporelle
# ============================================================

def example_6_temporal_analysis():
    """Analyser les patterns de crawl dans le temps"""
    print("\n" + "="*60)
    print("EXEMPLE 6: Analyse Temporelle des Crawls")
    print("="*60)
    
    analyzer = LogAnalyzer('access.log')
    df = analyzer.parse_log_file()
    
    daily_crawls, hourly_crawls = analyzer.analyze_temporal_distribution()
    
    print(f"\nCrawls par jour:")
    for _, row in daily_crawls.head().iterrows():
        bar = "█" * int(row['count'] / 5)
        print(f"  {row['date'].date()}: {bar} ({int(row['count'])})")
    
    print(f"\nCrawls par heure:")
    for _, row in hourly_crawls.head().iterrows():
        bar = "█" * int(row['count'] / 2)
        print(f"  {row['datetime']}: {bar} ({int(row['count'])})")


# ============================================================
# EXEMPLE 7: Export CSV Personnalisé
# ============================================================

def example_7_custom_csv_export():
    """Exporter des données personnalisées en CSV"""
    print("\n" + "="*60)
    print("EXEMPLE 7: Export CSV Personnalisé")
    print("="*60)
    
    analyzer = LogAnalyzer('access.log')
    df = analyzer.parse_log_file()
    
    # Créer un DataFrame personnalisé
    custom_df = df[df['is_googlebot']].copy()
    custom_df = custom_df[['timestamp', 'url', 'status_code', 'url_depth', 'is_obsolete']]
    
    # Exporter
    output_file = 'reports/googlebot_custom.csv'
    custom_df.to_csv(output_file, index=False)
    print(f"✅ Custom CSV exported: {output_file}")
    print(f"   Rows: {len(custom_df)}")
    print(f"   Columns: {', '.join(custom_df.columns)}")


# ============================================================
# EXEMPLE 8: Génération KPIs
# ============================================================

def example_8_kpis():
    """Calculer les KPIs importants"""
    print("\n" + "="*60)
    print("EXEMPLE 8: Calcul des KPIs")
    print("="*60)
    
    analyzer = LogAnalyzer('access.log')
    df = analyzer.parse_log_file()
    
    kpis = analyzer.calculate_kpis()
    
    print(f"\n📊 KPIs Principaux:")
    print(f"  Total Crawls: {kpis['crawl_count']}")
    print(f"  Success Rate: {(1-kpis['error_rate'])*100:.1f}%")
    print(f"  Average URL Depth: {kpis['avg_url_depth']:.2f}")
    print(f"  Crawl Efficiency: {kpis['crawl_efficiency']:.1f}%")


# ============================================================
# EXEMPLE 9: Comparaison Jour/Jour
# ============================================================

def example_9_day_comparison():
    """Comparer l'activité entre deux jours"""
    print("\n" + "="*60)
    print("EXEMPLE 9: Comparaison Entre Jours")
    print("="*60)
    
    analyzer = LogAnalyzer('access.log')
    df = analyzer.parse_log_file()
    
    if len(df) > 0:
        googlebot_df = df[df['is_googlebot']]
        
        # Grouper par date
        daily = googlebot_df.groupby(googlebot_df['date']).size()
        
        print(f"\nCrawls par jour:")
        for date, count in daily.items():
            print(f"  {date}: {count} crawls")
            
        if len(daily) > 1:
            avg = daily.mean()
            print(f"\nMoyenne: {avg:.0f} crawls/jour")


# ============================================================
# EXEMPLE 10: Rapport Complet en Texte
# ============================================================

def example_10_text_report():
    """Générer un rapport texte complet"""
    print("\n" + "="*60)
    print("EXEMPLE 10: Rapport Textuel Complet")
    print("="*60)
    
    analyzer = LogAnalyzer('access.log')
    analyzer.parse_log_file()
    
    report = analyzer.generate_report()
    print(report)


# ============================================================
# MAIN - Exécuter les exemples
# ============================================================

if __name__ == '__main__':
    # Décommenter les exemples à exécuter:
    
    example_1_basic_analysis()
    example_2_googlebot_only()
    example_3_problem_pages()
    example_4_url_depth()
    example_5_obsolete_pages()
    example_6_temporal_analysis()
    example_7_custom_csv_export()
    example_8_kpis()
    example_9_day_comparison()
    example_10_text_report()
    
    print("\n" + "="*60)
    print("✅ Tous les exemples exécutés!")
    print("="*60)
