import re
import os

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
╚══════╝ ╚═════╝  ╚═════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝{RESET}
"""

def parse_log_file(log_file_path, suspicious_keywords, importance_threshold=3, keyword_weights=None):
    """
    Parses a log file and extracts lines containing suspicious keywords,
    filtering based on an importance threshold and optional keyword weights.

    Args:
        log_file_path (str): The path to the log file.
        suspicious_keywords (list): A list of keywords to search for.
        importance_threshold (int, optional): Minimum total weight of keyword matches
                                              required to consider a line important.
                                              Defaults to 3.
        keyword_weights (dict, optional): A dictionary mapping keywords to their weights.
                                          If not provided, all keywords have a weight of 1.

    Returns:
        list: A list of tuples, each containing the line number and the matching line.
    """
    suspicious_lines = []
    if keyword_weights is None:
        keyword_weights = {keyword: 1 for keyword in suspicious_keywords}

    if not os.path.exists(log_file_path):
        print(f"Warning: Log file not found at {log_file_path}")
        return suspicious_lines

    try:
        with open(log_file_path, 'r') as log_file:
            for line_num, line in enumerate(log_file, 1):
                total_weight = 0
                for keyword in suspicious_keywords:
                    if re.search(keyword, line, re.IGNORECASE):
                        total_weight += keyword_weights.get(keyword, 1)
                        if total_weight >= importance_threshold:
                            suspicious_lines.append((line_num, line.strip()))
                            break

    except PermissionError:
        print(f"Error: Permission denied to access {log_file_path}")
    except Exception as e:
        print(f"Error processing {log_file_path}: {e}")

    return suspicious_lines

if __name__ == "__main__":
    print(banner)

    log_file_paths = [
        "/var/log/syslog",
        "/var/log/auth.log",
        "/var/log/kern.log",
        # "/var/log/apache2/error.log",
        # "/var/log/nginx/error.log"
    ]

    keywords = ["error", "fail", "unauthorized", "attack", "malware"]
    failed_login_patterns = [r"Failed password for", r"Invalid user", r"Authentication failure"]

    keyword_weights = {
        "attack": 3,
        "malware": 3
    }

    importance_threshold = 3

    any_suspicious_activity = False

    for log_file_path in log_file_paths:
        suspicious_lines = parse_log_file(log_file_path, keywords, importance_threshold, keyword_weights)

        with open(log_file_path, 'r') as log_file:
            for line_num, line in enumerate(log_file, 1):
                for pattern in failed_login_patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        suspicious_lines.append((line_num, line.strip()))
                        break

        if suspicious_lines:
            any_suspicious_activity = True
            print(f"\nSuspicious activity found in {log_file_path}:")
            for line_num, line in suspicious_lines:
                print(f"Line {line_num}: {line}")

    if not any_suspicious_activity:
        print("\nEverything looks good! No suspicious activity detected.")
