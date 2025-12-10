"""
Test script for Report Generator
Demonstrates CSV export and interactive dashboard generation
"""

from log_analyzer import LogAnalyzer
from report_generator import ReportGenerator
import os


def main():
    """Test complete report generation workflow"""
    
    print("\n" + "="*60)
    print("🧪 TESTING REPORT GENERATOR")
    print("="*60)

    # Check if log file exists
    log_file = '../access.log'
    
    if not os.path.exists(log_file):
        print(f"❌ Error: Log file not found at {log_file}")
        print(f"   Current directory: {os.getcwd()}")
        print(f"   Files in current directory: {os.listdir('.')}")
        return

    # Initialize analyzer
    print(f"\n📂 Loading logs from: {log_file}")
    analyzer = LogAnalyzer(log_file)
    analyzer.parse_log_file()
    analyzer.analyze()

    # Print analysis summary
    print(f"\n📊 Analysis Summary:")
    print(f"   Total requests: {len(analyzer.df)}")
    print(f"   Googlebot requests: {len(analyzer.df[analyzer.df['is_googlebot']])}")
    print(f"   Unique IPs: {analyzer.df['ip'].nunique()}")
    print(f"   Unique URLs: {analyzer.df['url'].nunique()}")

    # Generate reports
    print(f"\n🚀 Generating Reports...")
    generator = ReportGenerator(analyzer)
    results = generator.generate_full_report()

    print(f"\n✅ Reports generated successfully!")
    print(f"   CSV: {results['csv']}")
    print(f"   HTML Dashboard: {results['html']}")

    # Show top URLs
    print(f"\n🔝 Top 10 Crawled URLs (Googlebot only):")
    top_urls = analyzer.df[analyzer.df['is_googlebot']]['url'].value_counts().head(10)
    for idx, (url, count) in enumerate(top_urls.items(), 1):
        print(f"   {idx}. {url[:60]}... ({count} crawls)")

    # Show error statistics
    print(f"\n⚠️ Error Statistics:")
    kpis = analyzer.get_kpis()
    status_codes = kpis['status_codes']
    total = sum(status_codes.values())
    
    print(f"   Total requests: {total}")
    for code, count in sorted(status_codes.items()):
        percentage = (count / total * 100)
        if code >= 400:
            print(f"   {code}: {count} ({percentage:.1f}%) ❌")
        elif code >= 300:
            print(f"   {code}: {count} ({percentage:.1f}%) 🔀")
        else:
            print(f"   {code}: {count} ({percentage:.1f}%) ✅")

    print(f"\n💡 Next Steps:")
    print(f"   1. Open reports/dashboard.html in your browser")
    print(f"   2. Review crawl_report.csv for detailed URL statistics")
    print(f"   3. Analyze crawl patterns and optimize site structure")

    print("\n" + "="*60)


if __name__ == "__main__":
    main()
