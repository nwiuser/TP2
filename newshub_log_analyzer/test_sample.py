"""
Test script for Report Generator with sample logs
Tests CSV export and dashboard generation
"""

from log_analyzer import LogAnalyzer
from report_generator import ReportGenerator
import os


def main():
    """Test complete report generation workflow"""
    
    print("\n" + "="*70)
    print("🧪 TESTING REPORT GENERATOR - SAMPLE LOGS")
    print("="*70)

    # Use sample log file
    log_file = 'sample_access.log'
    
    if not os.path.exists(log_file):
        print(f"❌ Error: Log file not found at {log_file}")
        print(f"   Current directory: {os.getcwd()}")
        print(f"   Files: {os.listdir('.')}")
        return

    # Initialize analyzer
    print(f"\n📂 Loading logs from: {log_file}")
    analyzer = LogAnalyzer(log_file)
    
    # Parse and analyze
    print("📊 Parsing logs...")
    df = analyzer.parse_log_file()
    
    if df is None:
        print("❌ Failed to parse logs")
        return
    
    print("🔍 Analyzing data...")

    # Print analysis summary
    print(f"\n✅ Analysis Complete:")
    print(f"   • Total requests: {len(analyzer.df)}")
    print(f"   • Googlebot requests: {len(analyzer.df[analyzer.df['is_googlebot']])}")
    print(f"   • Unique IPs: {analyzer.df['ip'].nunique()}")
    print(f"   • Unique URLs: {analyzer.df['url'].nunique()}")
    print(f"   • Date range: {analyzer.df['timestamp'].min()} to {analyzer.df['timestamp'].max()}")

    # Generate reports
    print(f"\n🚀 Generating Reports...")
    generator = ReportGenerator(analyzer)
    results = generator.generate_full_report()

    print(f"\n✅ Reports generated successfully!")
    print(f"\n📁 Output Files:")
    print(f"   • CSV: {results['csv']}")
    print(f"   • HTML Dashboard: {results['html']}")
    
    # Verify files exist
    if os.path.exists(results['csv']):
        print(f"   ✓ CSV file created ({os.path.getsize(results['csv'])} bytes)")
    if os.path.exists(results['html']):
        print(f"   ✓ HTML file created ({os.path.getsize(results['html'])} bytes)")

    # Show top URLs
    print(f"\n🔝 Top 5 Crawled URLs (Googlebot):")
    googlebot_df = analyzer.df[analyzer.df['is_googlebot']]
    top_urls = googlebot_df['url'].value_counts().head(5)
    for idx, (url, count) in enumerate(top_urls.items(), 1):
        print(f"   {idx}. {url}: {count} crawls")

    # Show error stats
    print(f"\n⚠️  Error Analysis:")
    total_requests = len(googlebot_df)
    error_4xx = len(googlebot_df[googlebot_df['status_code'] >= 400])
    error_5xx = len(googlebot_df[googlebot_df['status_code'] >= 500])
    error_rate = (error_4xx / total_requests * 100) if total_requests > 0 else 0
    
    print(f"   • Total Googlebot requests: {total_requests}")
    print(f"   • 4xx errors: {error_4xx} ({error_4xx/total_requests*100:.1f}%)")
    print(f"   • 5xx errors: {error_5xx} ({error_5xx/total_requests*100:.1f}%)")
    print(f"   • Error rate: {error_rate:.1f}%")

    # Show URL depth analysis
    print(f"\n📊 URL Depth Analysis:")
    print(f"   • Average depth: {analyzer.df['url_depth'].mean():.2f}")
    print(f"   • Min depth: {analyzer.df['url_depth'].min()}")
    print(f"   • Max depth: {analyzer.df['url_depth'].max()}")
    
    # Check for obsolete URLs
    obsolete = analyzer.df[analyzer.df['is_obsolete']]
    if len(obsolete) > 0:
        print(f"\n🗑️  Obsolete URLs Found: {len(obsolete)}")
        obsolete_urls = obsolete['url'].value_counts().head(3)
        for url, count in obsolete_urls.items():
            print(f"   • {url}: {count} requests")

    print("\n" + "="*70)
    print("✅ Test Completed Successfully!")
    print("="*70 + "\n")


if __name__ == '__main__':
    main()
