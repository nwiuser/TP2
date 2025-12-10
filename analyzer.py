import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Tuple
from collections import defaultdict, Counter
import os
import json


class SEOAnalyzer:
    """Classe pour analyser les données SEO et générer des rapports et visualisations"""
    
    def __init__(self, validation_results: List[Dict], output_dir: str = 'seo_analysis_output'):
        """
        Initialise l'analyseur SEO
        
        Args:
            validation_results: Liste des résultats de validation
            output_dir: Répertoire pour sauvegarder les résultats
        """
        self.validation_results = validation_results
        self.output_dir = output_dir
        
        # Créer le répertoire de sortie
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        print(f"✓ Répertoire de sortie créé: {output_dir}\n")
        
        # Créer le DataFrame principal
        self.df = self._create_dataframe()
        
        # Calculer les statistiques
        self.error_summary = self._calculate_error_summary()
        self.error_by_type = self._calculate_error_by_type()
    
    def _create_dataframe(self) -> pd.DataFrame:
        """Crée un DataFrame à partir des résultats de validation"""
        data = []
        
        for result in self.validation_results:
            row = {
                'URL': result['url'],
                'Title': result['title'],
                'Score Global': result['score_global'],
                'Nombre Erreurs': result['nombre_erreurs'],
                'Statut Global': result['statut_global']
            }
            
            # Ajouter les statuts de chaque validation
            for v in result['validations']:
                row[f"{v['element']} - Status"] = v['status']
                row[f"{v['element']} - Valeur"] = v['value']
                row[f"{v['element']} - Métrique"] = v['metric']
            
            data.append(row)
        
        df = pd.DataFrame(data)
        return df
    
    def _calculate_error_summary(self) -> Dict:
        """Calcule le résumé des erreurs"""
        errors = {}
        
        for result in self.validation_results:
            for v in result['validations']:
                element = v['element']
                if element not in errors:
                    errors[element] = 0
                if v['status'] == 'ERREUR':
                    errors[element] += 1
        
        return errors
    
    def _calculate_error_by_type(self) -> Dict:
        """Calcule le nombre d'erreurs par type avec pourcentages"""
        total_products = len(self.validation_results)
        error_by_type = {}
        
        for element, count in self.error_summary.items():
            percentage = (count / total_products * 100) if total_products > 0 else 0
            error_by_type[element] = {
                'count': count,
                'percentage': percentage
            }
        
        return error_by_type
    
    def save_to_csv(self, filename: str = 'jumia_audit_seo.csv') -> None:
        """
        Sauvegarde les données d'analyse en CSV
        
        Args:
            filename: Nom du fichier CSV
        """
        # Créer une version simplifiée du DataFrame pour le CSV
        csv_data = []
        
        for result in self.validation_results:
            row = {
                'URL': result['url'],
                'Title': result['title'],
                'Score Global (%)': round(result['score_global'], 1),
                'Nombre Erreurs': result['nombre_erreurs'],
                'Statut': result['statut_global'],
                'Title Status': self._get_validation_status(result, 'Title'),
                'Meta Description Status': self._get_validation_status(result, 'Meta Description'),
                'H1 Status': self._get_validation_status(result, 'H1'),
                'H2 Status': self._get_validation_status(result, 'H2'),
                'Images ALT Status': self._get_validation_status(result, 'Images ALT'),
                'Contenu Status': self._get_validation_status(result, 'Contenu')
            }
            csv_data.append(row)
        
        df_csv = pd.DataFrame(csv_data)
        filepath = os.path.join(self.output_dir, filename)
        df_csv.to_csv(filepath, index=False, encoding='utf-8')
        
        print(f"✓ Données sauvegardées dans {filepath}")
    
    def _get_validation_status(self, result: Dict, element: str) -> str:
        """Récupère le statut d'une validation spécifique"""
        for v in result['validations']:
            if v['element'] == element:
                return v['status']
        return 'N/A'
    
    def get_top_problematic_pages(self, n: int = 10) -> pd.DataFrame:
        """
        Retourne les Top N pages avec le plus d'erreurs
        
        Args:
            n: Nombre de pages à retourner
        
        Returns:
            DataFrame avec les pages problématiques
        """
        top_pages = sorted(
            self.validation_results,
            key=lambda x: -x['nombre_erreurs']
        )[:n]
        
        data = []
        for page in top_pages:
            errors_list = [v['element'] for v in page['validations'] if v['status'] == 'ERREUR']
            data.append({
                'URL': page['url'][:60],
                'Title': page['title'][:50],
                'Erreurs': page['nombre_erreurs'],
                'Score': round(page['score_global'], 1),
                'Types d\'erreurs': ', '.join(errors_list)
            })
        
        return pd.DataFrame(data)
    
    def get_statistics(self) -> Dict:
        """Retourne les statistiques globales"""
        scores = [r['score_global'] for r in self.validation_results]
        errors = [r['nombre_erreurs'] for r in self.validation_results]
        
        stats = {
            'total_products': len(self.validation_results),
            'products_with_errors': sum(1 for r in self.validation_results if r['statut_global'] == 'ERREUR'),
            'average_score': round(sum(scores) / len(scores) if scores else 0, 1),
            'min_score': round(min(scores) if scores else 0, 1),
            'max_score': round(max(scores) if scores else 0, 1),
            'average_errors': round(sum(errors) / len(errors) if errors else 0, 1),
            'total_errors': sum(errors),
            'success_rate': round(
                ((len(self.validation_results) - sum(1 for r in self.validation_results if r['statut_global'] == 'ERREUR')) 
                 / len(self.validation_results) * 100) if self.validation_results else 0,
                1
            )
        }
        
        return stats
    
    def plot_error_distribution(self) -> None:
        """Crée un histogramme de distribution des erreurs"""
        errors = [r['nombre_erreurs'] for r in self.validation_results]
        
        fig = px.histogram(
            x=errors,
            nbins=7,
            title='Distribution du nombre d\'erreurs par produit',
            labels={'x': 'Nombre d\'erreurs', 'count': 'Nombre de produits'},
            color_discrete_sequence=['#EF553B']
        )
        
        fig.update_xaxes(title_text='Nombre d\'erreurs')
        fig.update_yaxes(title_text='Nombre de produits')
        
        filepath = os.path.join(self.output_dir, 'error_distribution.html')
        fig.write_html(filepath)
        print(f"✓ Graphique créé: {filepath}")
    
    def plot_top_problematic_pages(self, n: int = 15) -> None:
        """Crée un bar chart des pages problématiques"""
        top_pages = sorted(
            self.validation_results,
            key=lambda x: -x['nombre_erreurs']
        )[:n]
        
        data = {
            'Page': [p['title'][:30] + '...' for p in top_pages],
            'Erreurs': [p['nombre_erreurs'] for p in top_pages],
            'Score': [p['score_global'] for p in top_pages]
        }
        
        df = pd.DataFrame(data)
        
        fig = px.bar(
            df,
            x='Erreurs',
            y='Page',
            orientation='h',
            title=f'Top {n} pages avec le plus d\'erreurs',
            color='Score',
            color_continuous_scale='RdYlGn',
            labels={'Erreurs': 'Nombre d\'erreurs', 'Page': 'Page produit'}
        )
        
        filepath = os.path.join(self.output_dir, 'top_problematic_pages.html')
        fig.write_html(filepath)
        print(f"✓ Graphique créé: {filepath}")
    
    def plot_error_types_pie(self) -> None:
        """Crée un pie chart de répartition par type d'erreur"""
        error_types = list(self.error_summary.keys())
        error_counts = list(self.error_summary.values())
        
        fig = px.pie(
            values=error_counts,
            names=error_types,
            title='Répartition des erreurs par type',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        filepath = os.path.join(self.output_dir, 'error_types_pie.html')
        fig.write_html(filepath)
        print(f"✓ Graphique créé: {filepath}")
    
    def plot_score_distribution(self) -> None:
        """Crée un graphique de distribution des scores"""
        scores = [r['score_global'] for r in self.validation_results]
        
        fig = px.histogram(
            x=scores,
            nbins=20,
            title='Distribution des scores SEO',
            labels={'x': 'Score (%)', 'count': 'Nombre de produits'},
            color_discrete_sequence=['#00CC96']
        )
        
        fig.update_xaxes(title_text='Score SEO (%)')
        fig.update_yaxes(title_text='Nombre de produits')
        
        filepath = os.path.join(self.output_dir, 'score_distribution.html')
        fig.write_html(filepath)
        print(f"✓ Graphique créé: {filepath}")
    
    def simulate_improvements(self) -> None:
        """
        Simule l'amélioration des scores après correction des erreurs
        """
        # Calculer les scores actuels et simulés
        current_scores = []
        improved_scores = []
        scenarios = []
        
        for result in self.validation_results:
            current = result['score_global']
            # Simuler: chaque erreur corrigée = +16.67% (6 critères)
            improved = min(100, current + (result['nombre_erreurs'] * 16.67))
            
            current_scores.append(current)
            improved_scores.append(improved)
            scenarios.append({
                'Scenario': 'Actuel',
                'Score': current,
                'Type': result['title'][:20]
            })
            scenarios.append({
                'Scenario': 'Après corrections',
                'Score': improved,
                'Type': result['title'][:20]
            })
        
        df_scenarios = pd.DataFrame(scenarios)
        
        # Créer le graphique de comparaison
        fig = go.Figure()
        
        # Ajouter les distributions
        fig.add_trace(go.Histogram(
            x=current_scores,
            name='Score actuel',
            opacity=0.7,
            nbinsx=20,
            marker_color='#EF553B'
        ))
        
        fig.add_trace(go.Histogram(
            x=improved_scores,
            name='Score après corrections',
            opacity=0.7,
            nbinsx=20,
            marker_color='#00CC96'
        ))
        
        fig.update_layout(
            title='Impact potentiel des corrections SEO',
            xaxis_title='Score (%)',
            yaxis_title='Nombre de produits',
            barmode='overlay',
            hovermode='x unified'
        )
        
        filepath = os.path.join(self.output_dir, 'simulation_improvements.html')
        fig.write_html(filepath)
        print(f"✓ Graphique de simulation créé: {filepath}")
        
        # Afficher les statistiques d'amélioration
        avg_current = sum(current_scores) / len(current_scores)
        avg_improved = sum(improved_scores) / len(improved_scores)
        
        print(f"\n  Score moyen actuel: {avg_current:.1f}%")
        print(f"  Score moyen après corrections: {avg_improved:.1f}%")
        print(f"  Amélioration attendue: +{avg_improved - avg_current:.1f}%")
    
    def create_dashboard_png(self, filename: str = 'jumia_dashboard.png') -> None:
        """
        Crée un dashboard en PNG avec les visualisations principales
        
        Args:
            filename: Nom du fichier PNG
        """
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Dashboard SEO Jumia - Vue d\'ensemble', fontsize=20, fontweight='bold')
        
        # 1. Distribution des scores
        scores = [r['score_global'] for r in self.validation_results]
        axes[0, 0].hist(scores, bins=15, color='#00CC96', edgecolor='black', alpha=0.7)
        axes[0, 0].set_title('Distribution des scores SEO', fontsize=14, fontweight='bold')
        axes[0, 0].set_xlabel('Score (%)')
        axes[0, 0].set_ylabel('Nombre de produits')
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Top erreurs par type
        error_types = list(self.error_summary.keys())
        error_counts = list(self.error_summary.values())
        
        colors = ['#EF553B' if count > 5 else '#FFA15A' for count in error_counts]
        axes[0, 1].barh(error_types, error_counts, color=colors, edgecolor='black')
        axes[0, 1].set_title('Nombre d\'erreurs par type', fontsize=14, fontweight='bold')
        axes[0, 1].set_xlabel('Nombre d\'erreurs')
        axes[0, 1].grid(True, alpha=0.3, axis='x')
        
        # 3. Top pages problématiques
        top_pages = sorted(
            self.validation_results,
            key=lambda x: -x['nombre_erreurs']
        )[:10]
        
        top_titles = [p['title'][:25] + '...' for p in top_pages]
        top_errors = [p['nombre_erreurs'] for p in top_pages]
        top_colors = ['#EF553B' if e > 3 else '#FFA15A' for e in top_errors]
        
        axes[1, 0].bar(range(len(top_titles)), top_errors, color=top_colors, edgecolor='black')
        axes[1, 0].set_xticks(range(len(top_titles)))
        axes[1, 0].set_xticklabels(top_titles, rotation=45, ha='right')
        axes[1, 0].set_title('Top 10 pages avec le plus d\'erreurs', fontsize=14, fontweight='bold')
        axes[1, 0].set_ylabel('Nombre d\'erreurs')
        axes[1, 0].grid(True, alpha=0.3, axis='y')
        
        # 4. Répartition statut global
        statut_counts = Counter([r['statut_global'] for r in self.validation_results])
        labels = list(statut_counts.keys())
        sizes = list(statut_counts.values())
        colors_pie = ['#00CC96' if l == 'OK' else '#EF553B' for l in labels]
        
        axes[1, 1].pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors_pie,
                       startangle=90, textprops={'fontsize': 12, 'weight': 'bold'})
        axes[1, 1].set_title('Répartition des statuts globaux', fontsize=14, fontweight='bold')
        
        # Ajouter des statistiques en bas
        stats = self.get_statistics()
        stats_text = (
            f"Total produits: {stats['total_products']} | "
            f"Avec erreurs: {stats['products_with_errors']} | "
            f"Score moyen: {stats['average_score']}% | "
            f"Taux réussite: {stats['success_rate']}%"
        )
        fig.text(0.5, 0.02, stats_text, ha='center', fontsize=11, 
                style='italic', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout(rect=[0, 0.05, 1, 0.96])
        
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        print(f"✓ Dashboard PNG créé: {filepath}")
        plt.close()
    
    def print_summary(self) -> None:
        """Affiche un résumé des analyses"""
        stats = self.get_statistics()
        
        print("\n" + "="*70)
        print("RÉSUMÉ DE L'ANALYSE SEO")
        print("="*70)
        print(f"\n📊 STATISTIQUES GLOBALES:")
        print(f"  • Total de produits analysés: {stats['total_products']}")
        print(f"  • Produits avec erreurs: {stats['products_with_errors']}")
        print(f"  • Taux de réussite: {stats['success_rate']}%")
        print(f"  • Score moyen: {stats['average_score']}%")
        print(f"  • Meilleur score: {stats['max_score']}%")
        print(f"  • Pire score: {stats['min_score']}%")
        print(f"  • Nombre moyen d'erreurs par produit: {stats['average_errors']:.1f}")
        
        print(f"\n⚠️  ERREURS PAR TYPE:")
        for element, data in sorted(self.error_by_type.items(), key=lambda x: -x[1]['count']):
            print(f"  • {element}: {data['count']} ({data['percentage']:.1f}%)")
        
        print(f"\n🔝 TOP 5 PAGES PROBLÉMATIQUES:")
        top_pages = self.get_top_problematic_pages(5)
        for idx, (_, row) in enumerate(top_pages.iterrows(), 1):
            print(f"  {idx}. {row['Title'][:40]}")
            print(f"     Score: {row['Score']}% | Erreurs: {row['Erreurs']}")
            error_types = row['Types d\'erreurs']
            print(f"     Types: {error_types}\n")
        
        print("="*70 + "\n")
    
    def generate_all_analysis(self) -> None:
        """Génère tous les rapports et visualisations"""
        print("\n" + "="*70)
        print("GÉNÉRATION DES ANALYSES ET VISUALISATIONS")
        print("="*70 + "\n")
        
        # Sauvegarder en CSV
        self.save_to_csv()
        
        print("\n📊 Création des visualisations...\n")
        
        # Créer les graphiques
        self.plot_error_distribution()
        self.plot_top_problematic_pages()
        self.plot_error_types_pie()
        self.plot_score_distribution()
        self.simulate_improvements()
        
        print("\n🎨 Création du dashboard PNG...\n")
        self.create_dashboard_png()
        
        # Afficher le résumé
        self.print_summary()
        
        print("✓ Toutes les analyses ont été générées avec succès!\n")


