import argparse
from file_analyzer import FileAnalyzer

def main():
    parser = argparse.ArgumentParser(description="File Analyzer CLI")
    parser.add_argument('--path', required=True, help="Root folder to analyze")
    parser.add_argument('--report', choices=['size', 'all'], help="Show size report")
    parser.add_argument('--find-duplicates', action='store_true', help="Find duplicate files")
    args = parser.parse_args()

    analyzer = FileAnalyzer(args.path)
    analyzer.scan()

    if args.report:
        analyzer.print_summary()
        if args.report == "size":
            sizes = analyzer.get_size_report()
            print(sizes)

    if args.find_duplicates:
        duplicates = analyzer.find_duplicates()
        if duplicates:
            print("🔁 Duplicates found:")
            for dup in duplicates:
                print(f"{dup[0]} == {dup[1]}")
        else:
            print("No duplicates found.")

if __name__ == '__main__':
    main()
