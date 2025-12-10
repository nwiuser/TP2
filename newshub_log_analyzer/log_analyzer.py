"""
log_analyzer.py - Parser et analyseur des logs Apache
Extrait et analyse les données de crawl de Googlebot
"""

import pandas as pd
import re
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from collections import defaultdict, Counter


class LogAnalyzer:
    """Classe pour parser et analyser les logs Apache"""
    
    # Pattern regex Apache Combined Log Format
    LOG_PATTERN = re.compile(
        r'(\d+\.\d+\.\d+\.\d+)\s+'  # IP
        r'(?:\S+)\s+'  # Identité (-)
        r'(?:\S+)\s+'  # User (-)
        r'\[([^\]]+)\]\s+'  # Date/Time
        r'"(\S+)\s+(\S+)\s+(\S+)"\s+'  # Méthode URL Protocole
        r'(\d+)\s+'  # Code HTTP
        r'(\d+|-)\s+'  # Taille
        r'"([^"]*)" '  # Referrer
        r'"([^"]*)"'  # User-Agent
    )
    
    def __init__(self, log_file: str):
        """
        Initialise l'analyseur
        
        Args:
            log_file: Chemin vers le fichier access.log
        """
        self.log_file = log_file
        self.raw_logs = []
        self.df = None
        self.googlebot_df = None
    
    def parse_log_file(self) -> Optional[pd.DataFrame]:
        """
        Parse le fichier access.log et retourne DataFrame
        
        Returns:
            DataFrame avec les logs parsés ou None si erreur
        """
        print(f"\n📖 Lecture du fichier: {self.log_file}")
        
        try:
            with open(self.log_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            print(f"✅ {len(lines):,} lignes lues\n")
            
            # Parser les lignes
            parsed_data = []
            errors = 0
            
            for idx, line in enumerate(lines, 1):
                if idx % 50000 == 0:
                    print(f"  Traitement: {idx:,}/{len(lines):,} lignes...")
                
                match = self.LOG_PATTERN.match(line)
                if match:
                    try:
                        ip = match.group(1)
                        datetime_str = match.group(2)
                        method = match.group(3)
                        url = match.group(4)
                        protocol = match.group(5)
                        status = int(match.group(6))
                        size = match.group(7)
                        referrer = match.group(8)
                        user_agent = match.group(9)
                        
                        # Parser la date
                        parsed_date = self._parse_date(datetime_str)
                        
                        parsed_data.append({
                            'ip': ip,
                            'timestamp': parsed_date,
                            'date': parsed_date.date(),
                            'hour': parsed_date.hour,
                            'method': method,
                            'url': url,
                            'protocol': protocol,
                            'status': status,
                            'status_code': status,  # Alias for status
                            'size': int(size) if size != '-' else 0,
                            'referrer': referrer,
                            'user_agent': user_agent,
                            'is_googlebot': 'googlebot' in user_agent.lower(),
                            'is_error': 1 if status >= 400 else 0,
                            'url_depth': url.count('/') - 1,  # Count slashes minus protocol //
                            'is_obsolete': '/archive/' in url or 'old' in url.lower() or 'deprecated' in url.lower()
                        })
                    except Exception as e:
                        errors += 1
                else:
                    errors += 1
            
            print(f"✅ Parsing complété")
            print(f"  • Lignes parsées: {len(parsed_data):,}")
            print(f"  • Erreurs: {errors:,}\n")
            
            # Créer DataFrame
            self.df = pd.DataFrame(parsed_data)
            
            # Filtrer Googlebot
            self.googlebot_df = self.df[self.df['is_googlebot']].copy()
            
            return self.df
        
        except FileNotFoundError:
            print(f"❌ Fichier non trouvé: {self.log_file}")
            return None
        except Exception as e:
            print(f"❌ Erreur parsing: {str(e)}")
            return None
    
    def _parse_date(self, date_str: str) -> datetime:
        """
        Parse la date Apache format: 01/Jan/2025:12:34:56 +0000
        
        Args:
            date_str: Chaîne de date
        
        Returns:
            Objet datetime
        """
        try:
            return datetime.strptime(date_str[:20], '%d/%b/%Y:%H:%M:%S')
        except:
            return datetime.now()
    
    def get_statistics(self) -> Dict:
        """Retourne les statistiques globales"""
        if self.df is None or self.df.empty:
            return {}
        
        return {
            'total_lines': len(self.df),
            'unique_ips': self.df['ip'].nunique(),
            'unique_urls': self.df['url'].nunique(),
            'date_range': f"{self.df['date'].min()} à {self.df['date'].max()}",
            'methods': dict(self.df['method'].value_counts()),
            'total_googlebot': len(self.googlebot_df),
            'googlebot_percentage': round(
                len(self.googlebot_df) / len(self.df) * 100, 2
            ) if len(self.df) > 0 else 0
        }
    
    def analyze_temporal_distribution(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Analyse la distribution temporelle des crawls
        
        Returns:
            Tuple (crawls_par_jour, crawls_par_heure)
        """
        if self.googlebot_df is None or self.googlebot_df.empty:
            return pd.DataFrame(), pd.DataFrame()
        
        # Crawls par jour
        by_day = self.googlebot_df.groupby('date').size().reset_index(name='crawl_count')
        by_day.columns = ['date', 'crawls']
        
        # Crawls par heure
        by_hour = self.googlebot_df.groupby('hour').size().reset_index(name='crawl_count')
        by_hour.columns = ['hour', 'crawls']
        
        print("✅ Distribution temporelle analysée")
        print(f"  • Crawls/jour: min={by_day['crawls'].min()}, "
              f"max={by_day['crawls'].max()}, "
              f"avg={by_day['crawls'].mean():.0f}")
        
        return by_day, by_hour
    
    def get_top_urls(self, n: int = 20) -> pd.DataFrame:
        """
        Retourne les Top N URLs les plus crawlées
        
        Args:
            n: Nombre d'URLs à retourner
        
        Returns:
            DataFrame avec les top URLs
        """
        if self.googlebot_df is None or self.googlebot_df.empty:
            return pd.DataFrame()
        
        top_urls = self.googlebot_df['url'].value_counts().head(n).reset_index()
        top_urls.columns = ['url', 'crawl_count']
        
        print(f"✅ Top {n} URLs analysées")
        
        return top_urls
    
    def analyze_status_codes(self) -> Dict:
        """
        Analyse la distribution des codes HTTP
        
        Returns:
            Dictionnaire avec statistiques codes HTTP
        """
        if self.googlebot_df is None or self.googlebot_df.empty:
            return {}
        
        total = len(self.googlebot_df)
        
        # Compter par code
        status_counts = self.googlebot_df['status'].value_counts().to_dict()
        
        # Calculer pourcentages erreurs
        errors_4xx = sum(
            v for k, v in status_counts.items() 
            if 400 <= k < 500
        )
        errors_5xx = sum(
            v for k, v in status_counts.items() 
            if 500 <= k < 600
        )
        
        stats = {
            'total_requests': total,
            'status_distribution': status_counts,
            'errors_4xx': errors_4xx,
            'errors_4xx_percentage': round(errors_4xx / total * 100, 2),
            'errors_5xx': errors_5xx,
            'errors_5xx_percentage': round(errors_5xx / total * 100, 2),
            'total_errors': errors_4xx + errors_5xx,
            'error_rate': round((errors_4xx + errors_5xx) / total * 100, 2)
        }
        
        print("✅ Codes HTTP analysés")
        print(f"  • Erreurs 4xx: {errors_4xx} ({stats['errors_4xx_percentage']:.2f}%)")
        print(f"  • Erreurs 5xx: {errors_5xx} ({stats['errors_5xx_percentage']:.2f}%)")
        print(f"  • Taux erreur global: {stats['error_rate']:.2f}%")
        
        return stats
    
    def analyze_url_depth(self) -> Dict:
        """
        Analyse la profondeur des URLs (nombre de niveaux)
        
        Returns:
            Dictionnaire avec distribution de profondeur
        """
        if self.googlebot_df is None or self.googlebot_df.empty:
            return {}
        
        def get_depth(url):
            """Compte les niveaux d'URL"""
            return url.count('/')
        
        depths = self.googlebot_df['url'].apply(get_depth)
        depth_dist = depths.value_counts().sort_index().to_dict()
        
        stats = {
            'depth_distribution': depth_dist,
            'average_depth': round(depths.mean(), 2),
            'min_depth': int(depths.min()),
            'max_depth': int(depths.max()),
            'most_common_depth': int(depths.mode()[0]) if len(depths.mode()) > 0 else 0
        }
        
        print("✅ Profondeur d'URL analysée")
        print(f"  • Profondeur moyenne: {stats['average_depth']}")
        print(f"  • Profondeur la plus courante: {stats['most_common_depth']}")
        
        return stats
    
    def find_obsolete_urls(self) -> List[Tuple[str, int]]:
        """
        Identifie les URLs obsolètes (patterns: /archive/, /old-, etc.)
        
        Returns:
            Liste des URLs obsolètes avec count
        """
        if self.googlebot_df is None or self.googlebot_df.empty:
            return []
        
        obsolete_patterns = ['/archive/', '/old-', '/deleted', '/deprecated']
        
        obsolete_urls = []
        for pattern in obsolete_patterns:
            matches = self.googlebot_df[
                self.googlebot_df['url'].str.contains(pattern, case=False, na=False)
            ]
            
            if not matches.empty:
                url_counts = matches['url'].value_counts().to_list()
                for idx, (url, count) in enumerate(matches['url'].value_counts().items()):
                    obsolete_urls.append((url, count))
        
        # Dédupliquer et trier
        obsolete_urls = sorted(list(set(obsolete_urls)), key=lambda x: -x[1])
        
        print(f"✅ URLs obsolètes trouvées: {len(obsolete_urls)}")
        
        return obsolete_urls[:20]  # Top 20
    
    def calculate_kpis(self) -> Dict:
        """
        Calcule les KPIs principaux
        
        Returns:
            Dictionnaire avec tous les KPIs
        """
        if self.googlebot_df is None or self.googlebot_df.empty:
            return {}
        
        status_stats = self.analyze_status_codes()
        depth_stats = self.analyze_url_depth()
        
        kpis = {
            'crawl_count': len(self.googlebot_df),
            'crawl_count_per_day': round(
                len(self.googlebot_df) / len(self.googlebot_df['date'].unique()), 2
            ),
            'unique_urls_crawled': self.googlebot_df['url'].nunique(),
            'avg_crawls_per_url': round(
                len(self.googlebot_df) / self.googlebot_df['url'].nunique(), 2
            ),
            'status_distribution': status_stats.get('status_distribution', {}),
            'error_rate': status_stats.get('error_rate', 0),
            'avg_response_time': round(
                self.googlebot_df['size'].mean(), 2
            ) if 'size' in self.googlebot_df.columns else 0,
            'avg_url_depth': depth_stats.get('average_depth', 0),
            'crawl_efficiency': round(
                (self.googlebot_df['url'].nunique() / len(self.googlebot_df)) * 100, 2
            )
        }
        
        return kpis
    
    def generate_report(self) -> str:
        """
        Génère un rapport texte complet
        
        Returns:
            Rapport formaté
        """
        stats = self.get_statistics()
        kpis = self.calculate_kpis()
        status_stats = self.analyze_status_codes()
        depth_stats = self.analyze_url_depth()
        top_urls = self.get_top_urls(10)
        obsolete_urls = self.find_obsolete_urls()
        
        report = f"""
{'='*70}
RAPPORT D'ANALYSE - GOOGLEBOT CRAWL AUDIT
{'='*70}

📊 STATISTIQUES GLOBALES:
  • Lignes totales: {stats.get('total_lines', 0):,}
  • IPs uniques: {stats.get('unique_ips', 0):,}
  • URLs uniques: {stats.get('unique_urls', 0):,}
  • Période: {stats.get('date_range', 'N/A')}
  • Méthodes HTTP: {stats.get('methods', {})}

🤖 GOOGLEBOT:
  • Requêtes Googlebot: {stats.get('total_googlebot', 0):,}
  • Pourcentage: {stats.get('googlebot_percentage', 0)}%
  • Crawls/jour: {kpis.get('crawl_count_per_day', 0)}
  • URLs crawlées: {kpis.get('unique_urls_crawled', 0):,}
  • Efficacité: {kpis.get('crawl_efficiency', 0)}%

⚠️  CODES HTTP:
  • Erreurs 4xx: {status_stats.get('errors_4xx', 0)} "
    "({status_stats.get('errors_4xx_percentage', 0)}%)
  • Erreurs 5xx: {status_stats.get('errors_5xx', 0)} "
    "({status_stats.get('errors_5xx_percentage', 0)}%)
  • Taux erreur: {status_stats.get('error_rate', 0)}%

📏 PROFONDEUR:
  • Profondeur moyenne: {depth_stats.get('average_depth', 0)}
  • Profondeur max: {depth_stats.get('max_depth', 0)}
  • Plus courante: {depth_stats.get('most_common_depth', 0)}

🔝 TOP 10 URLs:
{self._format_top_urls(top_urls)}

🗑️  URLs OBSOLÈTES ({len(obsolete_urls)}):
{self._format_obsolete_urls(obsolete_urls)}

{'='*70}
"""
        return report
    
    def _format_top_urls(self, df: pd.DataFrame) -> str:
        """Formate le top URLs pour le rapport"""
        if df.empty:
            return "  Aucune URL trouvée"
        
        lines = []
        for idx, (_, row) in enumerate(df.head(10).iterrows(), 1):
            lines.append(f"  {idx:2d}. {row['url'][:50]:50s} ({row['crawl_count']:,})")
        
        return "\n".join(lines)
    
    def _format_obsolete_urls(self, urls: List[Tuple[str, int]]) -> str:
        """Formate les URLs obsolètes pour le rapport"""
        if not urls:
            return "  Aucune URL obsolète trouvée"
        
        lines = []
        for url, count in urls[:5]:
            lines.append(f"  • {url[:60]:60s} ({count:,})")
        
        return "\n".join(lines)
