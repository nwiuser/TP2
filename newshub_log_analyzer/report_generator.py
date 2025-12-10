"""
Report Generator for Newsroom Log Analyzer
Generates CSV reports and interactive Plotly dashboards
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from log_analyzer import LogAnalyzer


class ReportGenerator:
    """Generate CSV reports and interactive dashboards from log analysis"""

    def __init__(self, analyzer: LogAnalyzer):
        """
        Initialize report generator
        
        Args:
            analyzer: LogAnalyzer instance with parsed and analyzed data
        """
        self.analyzer = analyzer
        self.df = analyzer.df
        self.googlebot_df = analyzer.df[analyzer.df['is_googlebot']]
        self.output_dir = "reports"
        
        # Create reports directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def export_crawl_report_csv(self) -> str:
        """
        Export comprehensive crawl report to CSV
        
        Returns:
            str: Path to generated CSV file
        """
        # Aggregate data by URL
        url_stats = self.googlebot_df.groupby('url').agg({
            'ip': 'count',  # crawl_count
            'status_code': lambda x: x.value_counts().to_dict(),
            'size': 'mean',
            'url_depth': 'first',
            'timestamp': ['min', 'max'],
            'is_error': 'sum'  # Error count
        }).reset_index()

        # Flatten column names
        url_stats.columns = ['url', 'crawl_count', 'status_codes', 'avg_size', 
                            'depth', 'first_crawl', 'last_crawl', 'error_count']

        # Calculate error rate
        url_stats['error_rate'] = (url_stats['error_count'] / url_stats['crawl_count'] * 100).round(2)

        # Determine if page is obsolete
        url_stats['is_obsolete'] = url_stats['url'].str.contains(
            r'/archive/|/old-|/deprecated/|/backup/', 
            case=False, 
            regex=True
        ).astype(int)

        # Sort by crawl count descending
        url_stats = url_stats.sort_values('crawl_count', ascending=False)

        # Save to CSV
        csv_path = os.path.join(self.output_dir, 'crawl_report.csv')
        url_stats.to_csv(csv_path, index=False, encoding='utf-8')
        
        print(f"✅ CSV Report exported: {csv_path}")
        print(f"   Total URLs analyzed: {len(url_stats)}")
        
        return csv_path

    def _create_time_series_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Create time series data for crawls per day and hour
        
        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: Daily and hourly crawl counts
        """
        # Daily crawls
        daily_crawls = self.googlebot_df.groupby(self.googlebot_df['timestamp'].dt.date).size()
        daily_crawls = daily_crawls.reset_index()
        daily_crawls.columns = ['date', 'count']
        daily_crawls['date'] = pd.to_datetime(daily_crawls['date'])

        # Hourly crawls
        hourly_crawls = self.googlebot_df.groupby(self.googlebot_df['timestamp'].dt.floor('h')).size()
        hourly_crawls = hourly_crawls.reset_index()
        hourly_crawls.columns = ['datetime', 'count']

        return daily_crawls, hourly_crawls

    def _plot_crawls_timeline(self, daily_crawls: pd.DataFrame, hourly_crawls: pd.DataFrame) -> go.Figure:
        """
        Create line chart for crawls per day/hour
        
        Args:
            daily_crawls: Daily crawl counts
            hourly_crawls: Hourly crawl counts
            
        Returns:
            go.Figure: Plotly figure
        """
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=("Crawls par Jour", "Crawls par Heure (24h dernières)"),
            vertical_spacing=0.12
        )

        # Daily line chart
        fig.add_trace(
            go.Scatter(
                x=daily_crawls['date'],
                y=daily_crawls['count'],
                mode='lines+markers',
                name='Crawls/Jour',
                line=dict(color='#1f77b4', width=2),
                marker=dict(size=6),
                hovertemplate='<b>Date:</b> %{x|%d/%m/%Y}<br><b>Crawls:</b> %{y}<extra></extra>'
            ),
            row=1, col=1
        )

        # Hourly line chart (last 24 hours)
        hourly_recent = hourly_crawls.tail(24)
        fig.add_trace(
            go.Scatter(
                x=hourly_recent['datetime'],
                y=hourly_recent['count'],
                mode='lines+markers',
                name='Crawls/Heure',
                line=dict(color='#ff7f0e', width=2),
                marker=dict(size=5),
                hovertemplate='<b>Heure:</b> %{x|%d/%m %H:00}<br><b>Crawls:</b> %{y}<extra></extra>'
            ),
            row=2, col=1
        )

        # Update layout
        fig.update_xaxes(title_text="Date", row=1, col=1)
        fig.update_xaxes(title_text="Heure", row=2, col=1)
        fig.update_yaxes(title_text="Nombre de Crawls", row=1, col=1)
        fig.update_yaxes(title_text="Nombre de Crawls", row=2, col=1)

        return fig

    def _plot_top_urls(self, n: int = 20) -> go.Figure:
        """
        Create bar chart for top crawled URLs
        
        Args:
            n: Number of top URLs to display
            
        Returns:
            go.Figure: Plotly figure
        """
        top_urls = self.googlebot_df['url'].value_counts().head(n)
        
        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=top_urls.values,
                y=[url[:60] + '...' if len(url) > 60 else url for url in top_urls.index],
                orientation='h',
                marker=dict(color='#2ca02c', line=dict(color='#1f77b4', width=1)),
                hovertemplate='<b>URL:</b> %{fullData.customdata}<br><b>Crawls:</b> %{x}<extra></extra>',
                customdata=top_urls.index,
                text=top_urls.values,
                textposition='outside'
            )
        )

        fig.update_layout(
            title=f"Top {n} URLs les Plus Crawlées",
            xaxis_title="Nombre de Crawls",
            yaxis_title="URL",
            height=600,
            margin=dict(l=300, r=50, t=50, b=50),
            showlegend=False,
            hovermode='closest'
        )

        return fig

    def _plot_error_distribution(self) -> go.Figure:
        """
        Create pie chart for error codes distribution
        
        Returns:
            go.Figure: Plotly figure
        """
        # Categorize status codes
        status_categories = self.googlebot_df.copy()
        status_categories['status_category'] = status_categories['status_code'].apply(
            lambda x: '2xx (Success)' if 200 <= x < 300
            else '3xx (Redirect)' if 300 <= x < 400
            else '4xx (Client Error)' if 400 <= x < 500
            else '5xx (Server Error)' if x >= 500
            else 'Unknown'
        )

        status_dist = status_categories['status_category'].value_counts()
        colors = {
            '2xx (Success)': '#2ca02c',
            '3xx (Redirect)': '#1f77b4',
            '4xx (Client Error)': '#ff7f0e',
            '5xx (Server Error)': '#d62728'
        }

        fig = go.Figure()
        fig.add_trace(
            go.Pie(
                labels=status_dist.index,
                values=status_dist.values,
                marker=dict(colors=[colors.get(label, '#9467bd') for label in status_dist.index]),
                textposition='inside',
                textinfo='label+percent',
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
            )
        )

        fig.update_layout(
            title="Distribution des Codes HTTP",
            height=500
        )

        return fig

    def _plot_url_depth_histogram(self) -> go.Figure:
        """
        Create histogram for URL depth distribution
        
        Returns:
            go.Figure: Plotly figure
        """
        fig = go.Figure()
        fig.add_trace(
            go.Histogram(
                x=self.googlebot_df['url_depth'],
                nbinsx=20,
                marker=dict(color='#9467bd', line=dict(color='#1f77b4', width=1)),
                hovertemplate='<b>Profondeur:</b> %{x}<br><b>Nombre d\'URLs:</b> %{y}<extra></extra>'
            )
        )

        fig.update_layout(
            title="Distribution de la Profondeur d'URL",
            xaxis_title="Profondeur (Nombre de '/')",
            yaxis_title="Nombre d'URLs",
            height=500,
            showlegend=False
        )

        return fig

    def _plot_obsolete_pages_scatter(self) -> go.Figure:
        """
        Create scatter plot for obsolete pages vs crawls
        
        Returns:
            go.Figure: Plotly figure
        """
        # Identify obsolete pages
        df_plot = self.googlebot_df.copy()
        df_plot['is_obsolete'] = df_plot['url'].str.contains(
            r'/archive/|/old-|/deprecated/|/backup/',
            case=False,
            regex=True
        ).astype(int)

        # Aggregate by URL
        url_data = df_plot.groupby('url').agg({
            'ip': 'count',
            'url_depth': 'first',
            'is_obsolete': 'first',
            'is_error': lambda x: (x.sum() / len(x)) * 100
        }).reset_index()
        url_data.columns = ['url', 'crawl_count', 'depth', 'is_obsolete', 'error_rate']

        # Create color mapping
        color_map = {0: '#2ca02c', 1: '#d62728'}
        colors = [color_map[val] for val in url_data['is_obsolete']]

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=url_data['crawl_count'],
                y=url_data['error_rate'],
                mode='markers',
                marker=dict(
                    size=url_data['depth'] * 2,  # Size by depth
                    color=colors,
                    opacity=0.6,
                    line=dict(width=1, color='white'),
                    showscale=False
                ),
                text=[url[:50] + '...' if len(url) > 50 else url for url in url_data['url']],
                customdata=url_data[['url', 'depth', 'is_obsolete']],
                hovertemplate='<b>URL:</b> %{customdata[0]}<br>' +
                             '<b>Crawls:</b> %{x}<br>' +
                             '<b>Error Rate:</b> %{y:.1f}%<br>' +
                             '<b>Depth:</b> %{customdata[1]}<br>' +
                             '<b>Obsolete:</b> %{customdata[2]}<extra></extra>'
            )
        )

        fig.update_layout(
            title="Pages Obsolètes vs Crawls (Taille = Profondeur)",
            xaxis_title="Nombre de Crawls",
            yaxis_title="Taux d'Erreur (%)",
            height=600,
            hovermode='closest'
        )

        # Add legend manually for obsolete status
        fig.add_annotation(
            text="🟢 Active  🔴 Obsolete",
            xref="paper", yref="paper",
            x=0.02, y=0.98,
            showarrow=False,
            bgcolor="#f0f0f0",
            bordercolor="#333",
            borderwidth=1,
            font=dict(size=12)
        )

        return fig

    def create_interactive_dashboard(self) -> str:
        """
        Create comprehensive interactive dashboard with 5 visualizations
        
        Returns:
            str: Path to generated HTML dashboard
        """
        print("\n📊 Generating Interactive Dashboard...")

        # Prepare data
        daily_crawls, hourly_crawls = self._create_time_series_data()

        # Create individual figures
        fig_timeline = self._plot_crawls_timeline(daily_crawls, hourly_crawls)
        fig_top_urls = self._plot_top_urls(20)
        fig_errors = self._plot_error_distribution()
        fig_depth = self._plot_url_depth_histogram()
        fig_obsolete = self._plot_obsolete_pages_scatter()

        # Create HTML with multiple figures side by side
        html_parts = [
            """<!DOCTYPE html>
<html>
<head>
    <title>Newsroom Googlebot Crawl Analysis Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 20px;
            background: #f5f5f5;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            color: #333;
        }
        .dashboard-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }
        .chart-container {
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .chart-container.full-width {
            grid-column: 1 / -1;
        }
        .chart-title {
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 10px;
            color: #333;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Newsroom Googlebot Crawl Analysis Dashboard</h1>
        <p>Real-time monitoring of crawler activity and performance</p>
    </div>
    
    <div class="dashboard-grid">
        <div class="chart-container full-width">
            <div class="chart-title">📈 Crawls Timeline (Daily & Hourly)</div>
            <div id="timeline"></div>
        </div>
        
        <div class="chart-container">
            <div class="chart-title">🔝 Top URLs Crawled</div>
            <div id="top-urls"></div>
        </div>
        
        <div class="chart-container">
            <div class="chart-title">⚠️ HTTP Status Codes</div>
            <div id="errors"></div>
        </div>
        
        <div class="chart-container">
            <div class="chart-title">📊 URL Depth Distribution</div>
            <div id="depth"></div>
        </div>
        
        <div class="chart-container">
            <div class="chart-title">🗑️ Obsolete Pages Analysis</div>
            <div id="obsolete"></div>
        </div>
    </div>
    
    <script>"""
        ]
        
        # Extract data from each figure and add to HTML
        html_parts.append("Plotly.newPlot('timeline', ")
        html_parts.append(fig_timeline.to_json().split('"data":')[1].split(',"layout"')[0])
        html_parts.append(", ")
        html_parts.append(fig_timeline.to_json().split('"layout":')[1].rstrip('}'))
        html_parts.append("}, {responsive: true});\n")
        
        html_parts.append("Plotly.newPlot('top-urls', ")
        html_parts.append(fig_top_urls.to_json().split('"data":')[1].split(',"layout"')[0])
        html_parts.append(", ")
        html_parts.append(fig_top_urls.to_json().split('"layout":')[1].rstrip('}'))
        html_parts.append("}, {responsive: true});\n")
        
        html_parts.append("Plotly.newPlot('errors', ")
        html_parts.append(fig_errors.to_json().split('"data":')[1].split(',"layout"')[0])
        html_parts.append(", ")
        html_parts.append(fig_errors.to_json().split('"layout":')[1].rstrip('}'))
        html_parts.append("}, {responsive: true});\n")
        
        html_parts.append("Plotly.newPlot('depth', ")
        html_parts.append(fig_depth.to_json().split('"data":')[1].split(',"layout"')[0])
        html_parts.append(", ")
        html_parts.append(fig_depth.to_json().split('"layout":')[1].rstrip('}'))
        html_parts.append("}, {responsive: true});\n")
        
        html_parts.append("Plotly.newPlot('obsolete', ")
        html_parts.append(fig_obsolete.to_json().split('"data":')[1].split(',"layout"')[0])
        html_parts.append(", ")
        html_parts.append(fig_obsolete.to_json().split('"layout":')[1].rstrip('}'))
        html_parts.append("}, {responsive: true});\n")
        
        html_parts.append("""    </script>
</body>
</html>""")
        
        # Write to file
        html_path = os.path.join(self.output_dir, 'dashboard.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(''.join(html_parts))
        
        print(f"✅ Dashboard exported: {html_path}")
        
        return html_path

    def generate_full_report(self) -> Dict[str, str]:
        """
        Generate complete report with CSV and HTML dashboard
        
        Returns:
            Dict[str, str]: Paths to generated files
        """
        print("\n" + "="*60)
        print("🎯 GENERATING COMPREHENSIVE REPORT")
        print("="*60)

        # Export CSV
        csv_path = self.export_crawl_report_csv()

        # Create dashboard
        html_path = self.create_interactive_dashboard()

        # Print summary
        print("\n" + "="*60)
        print("✅ REPORT GENERATION COMPLETE")
        print("="*60)
        print(f"\n📁 Output Directory: {os.path.abspath(self.output_dir)}")
        print(f"📊 CSV Report: crawl_report.csv")
        print(f"📈 Dashboard: dashboard.html")
        print(f"\nTotal Googlebot Requests: {len(self.googlebot_df)}")
        print(f"Unique URLs: {self.googlebot_df['url'].nunique()}")
        print(f"Date Range: {self.googlebot_df['timestamp'].min()} to {self.googlebot_df['timestamp'].max()}")

        return {
            'csv': csv_path,
            'html': html_path
        }
