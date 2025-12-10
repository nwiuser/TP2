"""
main.py - Point d'entrée du système d'audit SEO Jumia
Orchestre le workflow complet: Scrape -> Validate -> Analyze
"""

import sys
import json
import os
from scraper import JumiaScraper
from validator import SEOValidator
from analyzer import SEOAnalyzer


def print_header():
    """Affiche l'en-tête du programme"""
    print("\n" + "="*80)
    print(" " * 15 + "🎯 JUMIA SEO AUDIT - SYSTÈME COMPLET")
    print("="*80)
    print("  Scraping 🕷️  | Validation ✅ | Analyse 📊 | Rapports 📈")
    print("="*80 + "\n")


def step_scraper(max_pages=5):
    """
    Scrape les données depuis Jumia.ma
    
    Args:
        max_pages: Nombre de pages à scraper (max 100)
    
    Returns:
        Liste des produits scrappés ou None si erreur
    """
    print("[1/3] SCRAPING - Extraction des données Jumia")
    print("-" * 80)
    
    # Limiter à 100 pages max
    max_pages = min(int(max_pages), 100)
    print(f"\n🕷️  Scraping {max_pages} pages depuis jumia.ma/electronique/\n")
    
    try:
        scraper = JumiaScraper()
        products = scraper.scrape_products(max_pages=max_pages)
        
        if not products:
            print("❌ Aucun produit trouvé")
            return None
        
        # Sauvegarder en JSON et CSV
        scraper.save_to_json('jumia_audit.json')
        scraper.save_to_csv('jumia_audit.csv')
        
        print(f"\n✅ Scraping complété")
        print(f"  • {len(products)} produits extraits")
        print(f"  • Fichiers: jumia_audit.json, jumia_audit.csv")
        
        return products
    
    except Exception as e:
        print(f"❌ Erreur scraping: {str(e)}")
        return None


def step_validator(products):
    """
    Valide les critères SEO de tous les produits
    
    Args:
        products: Liste des produits à valider
    
    Returns:
        Résultats de validation ou None si erreur
    """
    print("\n[2/3] VALIDATION - Vérification des critères SEO")
    print("-" * 80)
    print(f"\n✅ Validation {len(products)} produits\n")
    
    try:
        validator = SEOValidator(products)
        results = validator.validate_all_products()
        validator.save_validation_report('seo_validation_report.json')
        
        # Afficher résumé rapide
        failed = len([r for r in results if r['statut_global'] == 'ERREUR'])
        success_rate = ((len(results) - failed) / len(results) * 100)
        
        print(f"\n✅ Validation complétée")
        print(f"  • {len(results)} produits validés")
        print(f"  • Taux réussite: {success_rate:.1f}%")
        print(f"  • Produits avec erreurs: {failed}")
        
        return results
    
    except Exception as e:
        print(f"❌ Erreur validation: {str(e)}")
        return None


def step_analyzer(validation_results):
    """
    Analyse les résultats et génère tous les rapports
    
    Args:
        validation_results: Résultats de validation
    
    Returns:
        True si succès, False sinon
    """
    print("\n[3/3] ANALYSE - Génération des rapports et visualisations")
    print("-" * 80)
    print(f"\n📊 Analyse {len(validation_results)} produits\n")
    
    try:
        analyzer = SEOAnalyzer(validation_results, output_dir='seo_analysis_output')
        analyzer.generate_all_analysis()
        
        return True
    
    except Exception as e:
        print(f"❌ Erreur analyse: {str(e)}")
        return False


def display_summary(validation_results):
    """Affiche un résumé final des résultats"""
    print("\n" + "="*80)
    print("📋 RÉSUMÉ FINAL - AUDIT SEO JUMIA")
    print("="*80)
    
    try:
        analyzer = SEOAnalyzer(validation_results)
        stats = analyzer.get_statistics()
        
        print(f"\n📊 STATISTIQUES GLOBALES:")
        print(f"  • Produits analysés: {stats['total_products']}")
        print(f"  • Avec erreurs: {stats['products_with_errors']}")
        print(f"  • Taux réussite: {stats['success_rate']}%")
        print(f"  • Score moyen: {stats['average_score']}%")
        
        print(f"\n⚠️  TOP ERREURS:")
        for element, data in sorted(
            analyzer.error_by_type.items(),
            key=lambda x: -x[1]['count']
        )[:3]:
            print(f"  • {element}: {data['count']} ({data['percentage']:.1f}%)")
        
        print(f"\n📁 FICHIERS GÉNÉRÉS:")
        print(f"  • CSV: seo_analysis_output/jumia_audit_seo.csv")
        print(f"  • PNG: seo_analysis_output/jumia_dashboard.png")
        print(f"  • JSON: seo_validation_report.json")
        print(f"  • Graphiques: seo_analysis_output/*.html")
        
        print("\n" + "="*80 + "\n")
    
    except Exception as e:
        print(f"Erreur affichage résumé: {str(e)}")


def main():
    """Fonction principale - orchestre le workflow complet"""
    print_header()
    
    try:
        # Demander le nombre de pages
        while True:
            try:
                pages_input = input("Nombre de pages à scraper (1-100, défaut: 5): ").strip()
                max_pages = int(pages_input) if pages_input else 5
                
                if 1 <= max_pages <= 100:
                    break
                print("❌ Veuillez entrer un nombre entre 1 et 100")
            except ValueError:
                print("❌ Veuillez entrer un nombre valide")
        
        # ÉTAPE 1: SCRAPER
        products = step_scraper(max_pages)
        if not products:
            sys.exit(1)
        
        # ÉTAPE 2: VALIDATOR
        validation_results = step_validator(products)
        if not validation_results:
            sys.exit(1)
        
        # ÉTAPE 3: ANALYZER
        if not step_analyzer(validation_results):
            sys.exit(1)
        
        # RÉSUMÉ
        display_summary(validation_results)
        
        print("✅ WORKFLOW COMPLET TERMINÉ AVEC SUCCÈS!\n")
    
    except KeyboardInterrupt:
        print("\n\n⏸ Programme interrompu par l'utilisateur\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur: {str(e)}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
