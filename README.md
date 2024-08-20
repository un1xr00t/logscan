# LogScan

![image](https://github.com/user-attachments/assets/bc6ad64b-0008-40f4-87be-74ab4c0de8d4)


LogScan is a powerful Python script designed to analyze log files for specific activities by detecting predefined keywords, assigning weighted importance to critical terms, and generating detailed reports. With the latest version, LogScan is even more customizable and efficient, making it an invaluable tool for system administrators and security professionals.

## Features

- **Keyword Matching:** Scans log files for predefined keywords, allowing for precise detection of potential issues or attacks.
- **Weighted Importance:** Assign different weights to keywords to prioritize more critical terms, ensuring that high-priority issues are highlighted.
- **Max Weight Cap:** Set a maximum weight cap for any single log entry, preventing excessive weight from overlapping keywords.
- **Importance Threshold:** Filters lines based on a user-defined threshold, ensuring that only significant entries are flagged for review.
- **Failed Login Detection:** Detects failed login attempts by matching specific patterns such as `Failed password for`, `Invalid user`, and `Authentication failure`.
- **Multi-Log File Support:** Analyzes multiple log files simultaneously, with options to specify custom log files for scanning.
- **HTML Report Generation:** Automatically generates an easy-to-read HTML report with a table of flagged activities, sorted by importance.
- **Exclusion of Keywords:** Exclude specific keywords from the scan, providing more focused results.
- **Case Sensitivity Option:** Choose whether the keyword matching should be case-sensitive or not.
- **Parallel Processing:** Utilizes multiprocessing for faster log analysis, making it scalable for large log files.
- **Verbose Mode:** Outputs detailed processing information, useful for debugging and understanding the scan process.

## New in Version 2.0

- **Versioning:** Added version information in the banner to keep track of updates.
- **Command-Line Customization:** Introduced multiple command-line flags to customize the scan behavior, including `--max-weight`, `--log-files`, `--exclude-keywords`, and more.
- **Improved HTML Reporting:** Enhanced the HTML report generation with better sorting and presentation.
- **Performance Improvements:** Implemented multiprocessing to significantly speed up the scanning process, especially for large log files.

![image](https://github.com/user-attachments/assets/f0fc329d-7527-474c-9798-5e2144218918)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/un1xr00t/logscan.git


2. Navigate to the project directory:

   ```bash
   cd logscan
   ```

3. Ensure Python 3.x is installed on your system.

## Usage

To run the script, use the following command:

```bash
python3 logscan.py
```

The script will scan the specified log files for suspicious activities and output any lines that match the keywords and patterns.

## Customization

You can customize the following variables within the script:

- **`log_file_paths`**: Specify the paths of log files to be analyzed.
- **`keywords`**: Define the list of keywords to search for.
- **`keyword_weights`**: Assign weights to keywords to prioritize critical terms.
- **`importance_threshold`**: Set the minimum total weight required to consider a line important.

## Contributing

Contributions are welcome! If you have any suggestions or improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Created by [un1xr00t](https://github.com/un1xr00t)

