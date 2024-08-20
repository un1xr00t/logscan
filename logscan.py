import argparse
import re
import os
from datetime import datetime
from multiprocessing import Pool

# ANSI escape code for blue color
BLUE = "\033[94m"
RESET = "\033[0m"

# Banner with blue color
banner = f"""
{BLUE}██╗      ██████╗  ██████╗ ███████╗ ██████╗ █████╗ ███╗   ██╗
██║     ██╔═══██╗██╔════╝ ██╔════╝██╔════╝██╔══██╗████╗  ██║
██║     ██║   ██║██║  ███╗███████╗██║     ███████║██╔██╗ ██║
██║     ██║   ██║██║   ██║╚════██║██║     ██╔══██║██║╚██╗██║
███████╗╚██████╔╝╚██████╔╝███████║╚██████╗██║  ██║██║ ╚████║
╚══════╝ ╚═════╝  ╚═════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝

Version 2.0     

{RESET}
"""

def parse_line(line_info, max_weight):
    line_num, line, keywords, keyword_weights, ignore_case, exclude_keywords = line_info
    total_weight = 0
    for keyword in keywords:
        flags = re.IGNORECASE if ignore_case else 0
        if keyword in exclude_keywords:
            continue
        if re.search(r'\b' + re.escape(keyword) + r'\b', line, flags):
            # If 'fatal' is found with 'not fatal', skip adding weight for 'fatal'
            if keyword == 'fatal' and 'not fatal' in line.lower():
                continue
            total_weight += keyword_weights.get(keyword, 1)
            if total_weight >= max_weight:
                total_weight = max_weight
                break
    return (line_num, line.strip(), total_weight) if total_weight > 0 else None

def parse_log_file(log_file_path, keywords, keyword_weights, ignore_case=False, max_weight=10, exclude_keywords=[]):
    flagged_lines = []

    if not os.path.exists(log_file_path):
        print(f"Warning: Log file not found at {log_file_path}")
        return flagged_lines

    try:
        with open(log_file_path, 'r') as log_file:
            lines = [(i + 1, line, keywords, keyword_weights, ignore_case, exclude_keywords) for i, line in enumerate(log_file)]
            
            # Use multiprocessing for parallel processing
            with Pool() as pool:
                results = pool.starmap(parse_line, [(line_info, max_weight) for line_info in lines])
                flagged_lines = [result for result in results if result is not None]

    except PermissionError:
        print(f"Error: Permission denied to access {log_file_path}")
    except Exception as e:
        print(f"Error processing {log_file_path}: {e}")

    return flagged_lines

def load_keywords(keywords_input):
    keywords = []
    keyword_weights = {}

    if isinstance(keywords_input, list):
        return keywords_input, keyword_weights
    elif os.path.isfile(keywords_input):
        try:
            with open(keywords_input, 'r') as file:
                for line in file:
                    stripped_line = line.strip()
                    if stripped_line and not stripped_line.startswith(('#', '//', ';')):
                        parts = stripped_line.split('=')
                        keyword = parts[0].strip()
                        weight = int(parts[1].strip()) if len(parts) > 1 else 1
                        keywords.append(keyword)
                        keyword_weights[keyword] = weight
        except Exception as e:
            print(f"Error loading keywords from {keywords_input}: {e}")

    return keywords, keyword_weights

def generate_html_report(flagged_lines, output_file):
    flagged_lines.sort(key=lambda x: x[2], reverse=True)

    html_content = f"""
    <html>
    <head>
        <title>LogScan Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #dddddd; text-align: left; padding: 8px; }}
            th {{ background-color: #f2f2f2; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
            tr:hover {{ background-color: #f1f1f1; }}
        </style>
    </head>
    <body>
        <h1>LogScan Report</h1>
        <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <table>
            <tr>
                <th>Line Number</th>
                <th>Content</th>
                <th>Importance</th>
            </tr>
    """

    for line_num, line, weight in flagged_lines:
        html_content += f"""
            <tr>
                <td>{line_num}</td>
                <td>{line}</td>
                <td>{weight}</td>
            </tr>
        """

    html_content += """
        </table>
    </body>
    </html>
    """

    with open(output_file, 'w') as f:
        f.write(html_content)

def main():
    parser = argparse.ArgumentParser(description="LogScan: A tool for scanning log files for specific activities.")

    parser.add_argument('-k', '--keywords', help="List of keywords to search for in log files or a file containing keywords", default="keywords.txt")
    parser.add_argument('-i', '--ignore-case', action='store_true', help="Ignore case when searching for keywords")
    parser.add_argument('-o', '--output-file', help="Save the output to a file", default="output.html")
    parser.add_argument('-q', '--quiet', action='store_true', help="Suppress all output except for errors")
    parser.add_argument('-s', '--summary', action='store_true', help="Display a summary of the results")
    parser.add_argument('--max-weight', type=int, default=10, help="Set the maximum weight for any single log entry, 1-10")
    parser.add_argument('--log-files', nargs='+', help="Specify custom log files to scan")
    parser.add_argument('--exclude-keywords', nargs='+', help="List of keywords to exclude from the scan")
    parser.add_argument('--verbose', action='store_true', help="Show detailed processing information")
    
    args = parser.parse_args()

    keywords, keyword_weights = load_keywords(args.keywords)

    if not args.quiet:
        print(banner)

    log_file_paths = args.log_files if args.log_files else [
        "/var/log/syslog",
        "/var/log/auth.log",
        "/var/log/kern.log",
    ]

    flagged_lines = []

    for log_file_path in log_file_paths:
        flagged_lines += parse_log_file(log_file_path, keywords, keyword_weights, args.ignore_case, args.max_weight, args.exclude_keywords or [])

    if flagged_lines:
        generate_html_report(flagged_lines, args.output_file)
        if not args.quiet:
            print(f"\nFlagged activity found and saved to {args.output_file}.")
    else:
        if not args.quiet:
            print("\nEverything looks good! No flagged activity detected.")
    
    if args.summary:
        print(f"\nSummary: {len(flagged_lines)} lines flagged.")

if __name__ == "__main__":
    main()

