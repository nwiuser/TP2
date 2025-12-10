import pandas as pd
from typing import Tuple, List, Dict
import json

class SEOValidator:
    """Classe pour valider les critères SEO des pages produit"""
    
    # Règles SEO
    RULES = {
        'title': {
            'min': 40,
            'max': 70,
            'description': 'Title doit être entre 40 et 70 caractères'
        },
        'meta_description': {
            'min': 120,
            'description': 'Meta description doit avoir au minimum 120 caractères'
        },
        'h1': {
            'required': 1,
            'description': 'Doit avoir exactement 1 H1'
        },
        'h2': {
            'min': 2,
            'description': 'Doit avoir au minimum 2 H2'
        },
        'images_alt': {
            'max_percentage_without_alt': 30,
            'description': 'Maximum 30% des images peuvent être sans ALT'
        },
        'content': {
            'min_words': 150,
            'description': 'Contenu doit avoir au minimum 150 mots'
        }
    }
    
    def __init__(self, products_data: List[Dict]):
        """
        Initialise le validateur SEO
        
        Args:
            products_data: Liste des dictionnaires contenant les données des produits
        """
        self.products_data = products_data
        self.validation_results = []
        self.error_summary = {}
    
    def validate_title(self, product: Dict) -> Dict:
        """
        Valide le title
        
        Args:
            product: Dictionnaire du produit
        
        Returns:
            Dict avec statut et détails
        """
        title_length = product.get('title_length', 0)
        rules = self.RULES['title']
        
        status = 'OK'
        error = None
        
        if title_length < rules['min']:
            status = 'ERREUR'
            error = f"Trop court ({title_length}), minimum {rules['min']}"
        elif title_length > rules['max']:
            status = 'ERREUR'
            error = f"Trop long ({title_length}), maximum {rules['max']}"
        
        return {
            'element': 'Title',
            'status': status,
            'value': product.get('title', 'N/A')[:50],
            'metric': f"{title_length} chars",
            'error': error,
            'rule': rules['description']
        }
    
    def validate_meta_description(self, product: Dict) -> Dict:
        """
        Valide la meta description
        
        Args:
            product: Dictionnaire du produit
        
        Returns:
            Dict avec statut et détails
        """
        meta_length = product.get('meta_description_length', 0)
        rules = self.RULES['meta_description']
        
        status = 'OK'
        error = None
        
        if meta_length == 0:
            status = 'ERREUR'
            error = "Meta description absente"
        elif meta_length < rules['min']:
            status = 'ERREUR'
            error = f"Trop courte ({meta_length}), minimum {rules['min']}"
        
        return {
            'element': 'Meta Description',
            'status': status,
            'value': product.get('meta_description', 'N/A')[:50],
            'metric': f"{meta_length} chars",
            'error': error,
            'rule': rules['description']
        }
    
    def validate_h1(self, product: Dict) -> Dict:
        """
        Valide les H1
        
        Args:
            product: Dictionnaire du produit
        
        Returns:
            Dict avec statut et détails
        """
        h1_count = product.get('h1_count', 0)
        rules = self.RULES['h1']
        
        status = 'OK'
        error = None
        
        if h1_count != rules['required']:
            status = 'ERREUR'
            error = f"Nombre incorrect ({h1_count}), doit être exactement {rules['required']}"
        
        return {
            'element': 'H1',
            'status': status,
            'value': product.get('h1_content', 'N/A')[:50],
            'metric': f"{h1_count} H1",
            'error': error,
            'rule': rules['description']
        }
    
    def validate_h2(self, product: Dict) -> Dict:
        """
        Valide les H2
        
        Args:
            product: Dictionnaire du produit
        
        Returns:
            Dict avec statut et détails
        """
        h2_count = product.get('h2_count', 0)
        rules = self.RULES['h2']
        
        status = 'OK'
        error = None
        
        if h2_count < rules['min']:
            status = 'ERREUR'
            error = f"Insuffisant ({h2_count}), minimum {rules['min']}"
        
        return {
            'element': 'H2',
            'status': status,
            'value': f"{h2_count} H2 trouvés",
            'metric': f"{h2_count} H2",
            'error': error,
            'rule': rules['description']
        }
    
    def validate_images_alt(self, product: Dict) -> Dict:
        """
        Valide les attributs ALT des images
        
        Args:
            product: Dictionnaire du produit
        
        Returns:
            Dict avec statut et détails
        """
        total_images = product.get('total_images', 0)
        images_without_alt = product.get('images_without_alt', 0)
        rules = self.RULES['images_alt']
        
        status = 'OK'
        error = None
        
        if total_images > 0:
            percentage_without_alt = (images_without_alt / total_images) * 100
        else:
            percentage_without_alt = 0
        
        if percentage_without_alt > rules['max_percentage_without_alt']:
            status = 'ERREUR'
            error = f"{percentage_without_alt:.1f}% sans ALT, maximum {rules['max_percentage_without_alt']}%"
        
        return {
            'element': 'Images ALT',
            'status': status,
            'value': f"{total_images} images",
            'metric': f"{images_without_alt}/{total_images} sans ALT ({percentage_without_alt:.1f}%)",
            'error': error,
            'rule': rules['description']
        }
    
    def validate_content(self, product: Dict) -> Dict:
        """
        Valide le contenu textuel
        
        Args:
            product: Dictionnaire du produit
        
        Returns:
            Dict avec statut et détails
        """
        word_count = product.get('word_count', 0)
        rules = self.RULES['content']
        
        status = 'OK'
        error = None
        
        if word_count < rules['min_words']:
            status = 'ERREUR'
            error = f"Trop peu de mots ({word_count}), minimum {rules['min_words']}"
        
        return {
            'element': 'Contenu',
            'status': status,
            'value': f"{word_count} mots",
            'metric': f"{word_count} mots",
            'error': error,
            'rule': rules['description']
        }
    
    def validate_product(self, product: Dict) -> Dict:
        """
        Valide tous les critères SEO pour un produit
        
        Args:
            product: Dictionnaire du produit
        
        Returns:
            Dict contenant toutes les validations et un score global
        """
        validations = {
            'url': product.get('url', 'N/A'),
            'title': product.get('title', 'N/A')[:50],
            'validations': []
        }
        
        # Valider chaque critère
        validations['validations'].append(self.validate_title(product))
        validations['validations'].append(self.validate_meta_description(product))
        validations['validations'].append(self.validate_h1(product))
        validations['validations'].append(self.validate_h2(product))
        validations['validations'].append(self.validate_images_alt(product))
        validations['validations'].append(self.validate_content(product))
        
        # Calculer le score global
        errors = sum(1 for v in validations['validations'] if v['status'] == 'ERREUR')
        total = len(validations['validations'])
        score = ((total - errors) / total * 100) if total > 0 else 0
        
        validations['score_global'] = score
        validations['nombre_erreurs'] = errors
        validations['statut_global'] = 'OK' if errors == 0 else 'ERREUR'
        
        return validations
    
    def validate_all_products(self) -> List[Dict]:
        """
        Valide tous les produits
        
        Returns:
            Liste des validations pour tous les produits
        """
        print("\n" + "="*70)
        print("VALIDATION SEO DE TOUS LES PRODUITS")
        print("="*70 + "\n")
        
        self.validation_results = []
        
        for idx, product in enumerate(self.products_data, 1):
            result = self.validate_product(product)
            self.validation_results.append(result)
            
            print(f"Produit {idx}/{len(self.products_data)}: {result['statut_global']} | "
                  f"Score: {result['score_global']:.1f}% | "
                  f"Erreurs: {result['nombre_erreurs']}")
        
        self._generate_error_summary()
        return self.validation_results
    
    def _generate_error_summary(self) -> None:
        """Génère un résumé des erreurs"""
        error_summary = {}
        
        for validation in self.validation_results:
            for v in validation['validations']:
                element = v['element']
                if element not in error_summary:
                    error_summary[element] = 0
                if v['status'] == 'ERREUR':
                    error_summary[element] += 1
        
        self.error_summary = error_summary
        
        print("\n" + "="*70)
        print("RÉSUMÉ DES ERREURS")
        print("="*70)
        for element, count in sorted(error_summary.items(), key=lambda x: -x[1]):
            percentage = (count / len(self.validation_results)) * 100
            print(f"  {element}: {count} erreurs ({percentage:.1f}%)")
        
        total_errors = sum(error_summary.values())
        total_checks = len(self.validation_results) * 6  # 6 critères par produit
        success_rate = ((total_checks - total_errors) / total_checks * 100) if total_checks > 0 else 0
        
        print(f"\n  Taux de réussite global: {success_rate:.1f}%")
        print("="*70 + "\n")
    
    def get_failed_products(self) -> List[Dict]:
        """Retourne les produits avec erreurs"""
        return [v for v in self.validation_results if v['statut_global'] == 'ERREUR']
    
    def get_error_summary(self) -> Dict:
        """Retourne le résumé des erreurs"""
        return self.error_summary
    
    def save_validation_report(self, filename: str = 'seo_validation_report.json') -> None:
        """
        Sauvegarde le rapport de validation en JSON
        
        Args:
            filename: Nom du fichier de sortie
        """
        report = {
            'total_products': len(self.products_data),
            'products_with_errors': len(self.get_failed_products()),
            'error_summary': self.error_summary,
            'validations': self.validation_results
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Rapport de validation sauvegardé dans {filename}")


# class SEOValidator:
#     """Classe pour valider et nettoyer les données des logs"""
    
#     # IPs authentiques de Googlebot
#     GOOGLEBOT_IPS = [
#         '66.249.66',
#         '66.249.79',
#         '66.249.64'
#     ]
    
#     def __init__(self, df: pd.DataFrame):
#         """
#         Initialise le validateur
        
#         Args:
#             df: DataFrame contenant les logs
#         """
#         self.df = df.copy()
#         self.original_df = df.copy()
#         self.validation_report = {}
    
#     def filter_googlebot(self) -> pd.DataFrame:
#         """
#         Filtre uniquement les requêtes Googlebot (User-Agent + IP)
        
#         Returns:
#             DataFrame filtré avec les requêtes Googlebot
#         """
#         # Filtre par User-Agent
#         googlebot_ua = self.df[self.df['user_agent'].str.contains('googlebot', case=False, na=False)].copy()
        
#         # Filtre par IP
#         googlebot_ips = googlebot_ua[googlebot_ua['ip'].str.startswith(tuple(self.GOOGLEBOT_IPS))]
        
#         self.validation_report['googlebot_count'] = len(googlebot_ips)
#         self.validation_report['googlebot_percentage'] = (len(googlebot_ips) / len(self.df) * 100) if len(self.df) > 0 else 0
        
#         print(f"✓ {len(googlebot_ips)} requêtes Googlebot trouvées ({self.validation_report['googlebot_percentage']:.2f}%)")
#         return googlebot_ips
    
#     def filter_errors(self, df: pd.DataFrame = None) -> Tuple[pd.DataFrame, pd.DataFrame]:
#         """
#         Sépare les requêtes réussies (200, 301, 302, 304) des erreurs
        
#         Args:
#             df: DataFrame à filtrer (self.df par défaut)
        
#         Returns:
#             Tuple (requêtes_réussies, erreurs)
#         """
#         if df is None:
#             df = self.df
        
#         success_codes = [200, 301, 302, 304]
#         success = df[df['status'].isin(success_codes)]
#         errors = df[~df['status'].isin(success_codes)]
        
#         self.validation_report['success_count'] = len(success)
#         self.validation_report['error_count'] = len(errors)
#         self.validation_report['error_rate'] = (len(errors) / len(df) * 100) if len(df) > 0 else 0
        
#         print(f"✓ Requêtes réussies: {len(success)} | Erreurs: {len(errors)} ({self.validation_report['error_rate']:.2f}%)")
#         return success, errors
    
#     def identify_404_errors(self, df: pd.DataFrame = None) -> pd.DataFrame:
#         """
#         Identifie les erreurs 404
        
#         Args:
#             df: DataFrame à analyser (self.df par défaut)
        
#         Returns:
#             DataFrame avec les erreurs 404
#         """
#         if df is None:
#             df = self.df
        
#         errors_404 = df[df['status'] == 404]
#         self.validation_report['errors_404'] = len(errors_404)
#         self.validation_report['errors_404_percentage'] = (len(errors_404) / len(df) * 100) if len(df) > 0 else 0
        
#         print(f"✓ Erreurs 404: {len(errors_404)} ({self.validation_report['errors_404_percentage']:.2f}%)")
#         return errors_404
    
#     def identify_404_googlebot(self, googlebot_df: pd.DataFrame) -> pd.DataFrame:
#         """
#         Identifie les erreurs 404 pour Googlebot uniquement
        
#         Args:
#             googlebot_df: DataFrame contenant uniquement les logs Googlebot
        
#         Returns:
#             DataFrame avec les erreurs 404 de Googlebot
#         """
#         errors_404 = googlebot_df[googlebot_df['status'] == 404]
#         self.validation_report['googlebot_404'] = len(errors_404)
#         self.validation_report['googlebot_404_percentage'] = (len(errors_404) / len(googlebot_df) * 100) if len(googlebot_df) > 0 else 0
        
#         print(f"✓ Erreurs 404 (Googlebot): {len(errors_404)} ({self.validation_report['googlebot_404_percentage']:.2f}%)")
#         return errors_404
    
#     def identify_301_redirects(self, df: pd.DataFrame = None) -> pd.DataFrame:
#         """
#         Identifie les redirections 301
        
#         Args:
#             df: DataFrame à analyser (self.df par défaut)
        
#         Returns:
#             DataFrame avec les redirections 301
#         """
#         if df is None:
#             df = self.df
        
#         redirects_301 = df[df['status'] == 301]
#         self.validation_report['redirects_301'] = len(redirects_301)
#         self.validation_report['redirects_301_percentage'] = (len(redirects_301) / len(df) * 100) if len(df) > 0 else 0
        
#         print(f"✓ Redirections 301: {len(redirects_301)} ({self.validation_report['redirects_301_percentage']:.2f}%)")
#         return redirects_301
    
#     def identify_server_errors(self, df: pd.DataFrame = None) -> pd.DataFrame:
#         """
#         Identifie les erreurs serveur (500+)
        
#         Args:
#             df: DataFrame à analyser (self.df par défaut)
        
#         Returns:
#             DataFrame avec les erreurs serveur
#         """
#         if df is None:
#             df = self.df
        
#         server_errors = df[df['status'] >= 500]
#         self.validation_report['server_errors'] = len(server_errors)
#         self.validation_report['server_errors_percentage'] = (len(server_errors) / len(df) * 100) if len(df) > 0 else 0
        
#         print(f"✓ Erreurs serveur (500+): {len(server_errors)} ({self.validation_report['server_errors_percentage']:.2f}%)")
#         return server_errors
    
#     def get_validation_report(self) -> dict:
#         """Retourne le rapport de validation"""
#         return self.validation_report

