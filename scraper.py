import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from typing import List, Dict
import re
import json


class JumiaScraper:
    """Classe pour scraper les données produits Jumia avec audit SEO"""
    
    def __init__(self, base_url: str = "https://www.jumia.ma/electronique/"):
        """
        Initialise le scraper Jumia
        
        Args:
            base_url: URL de base de la catégorie à scraper
        """
        self.base_url = base_url
        self.products_data = []
        self.session = requests.Session()
        
        # User-Agent personnalisé
        self.headers = {
            'User-Agent': 'JumiaSEOAudit/1.0 (Mozilla/5.0)',
            'Accept-Language': 'fr-FR,fr;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }
    
    def get_product_urls(self, max_pages: int = 5) -> List[str]:
        """
        Collecte les URLs des produits depuis le JSON window.__STORE__
        
        Args:
            max_pages: Nombre de pages à scraper (30-100)
        
        Returns:
            Liste des URLs des produits
        """
        product_urls = []
        
        for page in range(1, max_pages + 1):
            try:
                page_url = f"{self.base_url}?page={page}"
                print(f"📄 Page {page}: {page_url}")
                
                response = self.session.get(page_url, headers=self.headers, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Chercher le script contenant window.__STORE__
                scripts = soup.find_all('script')
                page_products = 0
                
                for script in scripts:
                    content = script.string
                    if content and 'window.__STORE__' in content:
                        # Extraire le JSON
                        match = re.search(r'window\.__STORE__=(\{.*?\})\s*;', content, re.DOTALL)
                        
                        if match:
                            try:
                                json_str = match.group(1)
                                store_data = json.loads(json_str)
                                
                                # Récupérer les produits
                                if 'products' in store_data:
                                    products = store_data['products']
                                    
                                    for product in products:
                                        # Extraire l'URL du produit
                                        url = product.get('url') or product.get('link')
                                        
                                        if url:
                                            if not url.startswith('http'):
                                                url = 'https://www.jumia.ma' + url
                                            
                                            if url not in product_urls:
                                                product_urls.append(url)
                                                page_products += 1
                                
                                break  # On a trouvé les produits, sortir de la boucle
                            
                            except json.JSONDecodeError:
                                continue
                
                print(f"   ✓ {page_products} produits trouvés sur cette page")
                print(f"   Total: {len(product_urls)} produits collectés\n")
                
                # Délai pour respecter le serveur
                time.sleep(2)
                
            except requests.exceptions.RequestException as e:
                print(f"   ✗ Erreur: {str(e)}\n")
                continue
        
        return product_urls
    
    def extract_product_data(self, url: str) -> Dict:
        """
        Extrait les données SEO d'une page produit
        
        Args:
            url: URL du produit
        
        Returns:
            Dictionnaire contenant les données du produit
        """
        try:
            response = self.session.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # === EXTRACTION DES DONNÉES ===
            
            # URL
            product_url = url
            
            # Title (et longueur)
            title = soup.find('h1')
            title_text = title.get_text(strip=True) if title else "N/A"
            title_length = len(title_text) if title_text != "N/A" else 0
            
            # Meta Description (et longueur)
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            meta_description = meta_desc.get('content', "N/A") if meta_desc else "N/A"
            meta_length = len(meta_description) if meta_description != "N/A" else 0
            
            # H1 (nombre et contenu)
            h1_tags = soup.find_all('h1')
            h1_count = len(h1_tags)
            h1_contents = [h1.get_text(strip=True) for h1 in h1_tags]
            
            # H2 (nombre)
            h2_tags = soup.find_all('h2')
            h2_count = len(h2_tags)
            
            # Images (total et sans ALT)
            all_images = soup.find_all('img')
            total_images = len(all_images)
            images_without_alt = sum(1 for img in all_images if not img.get('alt'))
            
            # Contenu textuel (nombre de mots)
            text_content = soup.get_text()
            word_count = len(text_content.split())
            
            # Description du produit (extrait du contenu)
            description_section = soup.find('div', class_=re.compile('description|content|details', re.I))
            description_text = ""
            if description_section:
                description_text = description_section.get_text(strip=True)
                description_word_count = len(description_text.split())
            else:
                description_word_count = 0
            
            # Prix
            price = "N/A"
            price_elem = soup.find('span', class_=re.compile('price|amount|original', re.I))
            if price_elem:
                price = price_elem.get_text(strip=True)
            
            # Catégorie
            category = "N/A"
            breadcrumb = soup.find('nav', class_=re.compile('breadcrumb', re.I))
            if breadcrumb:
                breadcrumb_items = breadcrumb.find_all('a')
                if len(breadcrumb_items) > 1:
                    category = breadcrumb_items[-2].get_text(strip=True)
            
            # === CRÉATION DU DICTIONNAIRE ===
            product_data = {
                'url': product_url,
                'title': title_text,
                'title_length': title_length,
                'meta_description': meta_description,
                'meta_description_length': meta_length,
                'h1_count': h1_count,
                'h1_content': ' | '.join(h1_contents) if h1_contents else "N/A",
                'h2_count': h2_count,
                'total_images': total_images,
                'images_without_alt': images_without_alt,
                'word_count': word_count,
                'description_word_count': description_word_count,
                'price': price,
                'category': category
            }
            
            return product_data
        
        except requests.exceptions.RequestException as e:
            print(f"   ✗ Erreur lors de la récupération du produit: {str(e)}")
            return None
        except Exception as e:
            print(f"   ✗ Erreur lors du parsing: {str(e)}")
            return None
    
    def scrape_products(self, max_pages: int = 5) -> List[Dict]:
        """
        Scrape les données de tous les produits
        
        Args:
            max_pages: Nombre de pages à scraper
        
        Returns:
            Liste des données des produits
        """
        print("="*70)
        print("SCRAPING JUMIA - AUDIT SEO")
        print("="*70 + "\n")
        
        print("[1/2] COLLECTE DES URLs DE PRODUITS\n")
        product_urls = self.get_product_urls(max_pages)
        
        print(f"\n[2/2] EXTRACTION DES DONNÉES SEO ({len(product_urls)} produits)\n")
        
        for idx, url in enumerate(product_urls, 1):
            print(f"🔍 Produit {idx}/{len(product_urls)}: {url[:60]}...")
            
            product_data = self.extract_product_data(url)
            
            if product_data:
                self.products_data.append(product_data)
                
                # Afficher un résumé du produit
                print(f"   ✓ Title: {product_data['title'][:50]}...")
                print(f"   ✓ Meta: {product_data['meta_description_length']} caractères")
                print(f"   ✓ H1: {product_data['h1_count']} | H2: {product_data['h2_count']}")
                print(f"   ✓ Images: {product_data['total_images']} (sans ALT: {product_data['images_without_alt']})")
                print(f"   ✓ Mots: {product_data['word_count']}")
                print()
            
            # Délai entre les requêtes
            time.sleep(2)
        
        print(f"\n✓ {len(self.products_data)} produits scrappés avec succès\n")
        return self.products_data
    
    def get_dataframe(self) -> pd.DataFrame:
        """Retourne les données sous forme de DataFrame"""
        if not self.products_data:
            return pd.DataFrame()
        return pd.DataFrame(self.products_data)
    
    def save_to_csv(self, filename: str = 'jumia_products_seo_audit.csv') -> None:
        """
        Sauvegarde les données dans un fichier CSV
        
        Args:
            filename: Nom du fichier CSV
        """
        df = self.get_dataframe()
        if not df.empty:
            df.to_csv(filename, index=False, encoding='utf-8')
            print(f"✓ Données sauvegardées dans {filename}")
        else:
            print("✗ Aucune donnée à sauvegarder")
    
    def save_to_json(self, filename: str = 'jumia_products_seo_audit.json') -> None:
        """
        Sauvegarde les données dans un fichier JSON (dictionnaire)
        
        Args:
            filename: Nom du fichier JSON
        """
        if not self.products_data:
            print("✗ Aucune donnée à sauvegarder")
            return
        
        # Créer un dictionnaire avec statistiques globales
        df = pd.DataFrame(self.products_data)
        
        data = {
            'metadata': {
                'total_products': len(self.products_data),
                'timestamp': pd.Timestamp.now().isoformat(),
                'categories': list(set(p.get('category', 'N/A') for p in self.products_data if p.get('category') != 'N/A'))
            },
            'products': self.products_data,
            'statistics': {
                'title_length': {
                    'mean': float(df['title_length'].mean()),
                    'min': int(df['title_length'].min()),
                    'max': int(df['title_length'].max())
                },
                'meta_description_length': {
                    'mean': float(df['meta_description_length'].mean()),
                    'min': int(df['meta_description_length'].min()),
                    'max': int(df['meta_description_length'].max())
                },
                'h1_count': {
                    'mean': float(df['h1_count'].mean()),
                    'min': int(df['h1_count'].min()),
                    'max': int(df['h1_count'].max())
                },
                'h2_count': {
                    'mean': float(df['h2_count'].mean()),
                    'min': int(df['h2_count'].min()),
                    'max': int(df['h2_count'].max())
                },
                'images_without_alt': {
                    'mean': float(df['images_without_alt'].mean()),
                    'total': int(df['images_without_alt'].sum())
                },
                'word_count': {
                    'mean': float(df['word_count'].mean()),
                    'min': int(df['word_count'].min()),
                    'max': int(df['word_count'].max())
                }
            }
        }
        
        # Sauvegarder en JSON
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Données sauvegardées dans {filename}")
        print(f"  - {len(self.products_data)} produits")
        print(f"  - Statistiques incluses")
