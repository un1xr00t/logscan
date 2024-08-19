# LogScan

LogScan is a Python script designed to analyze log files for suspicious activities by detecting specific keywords, assigning weighted importance to critical terms, and identifying failed login attempts. It is a valuable tool for system administrators and security professionals looking to quickly identify potential security incidents.

## Features

- **Keyword Matching:** Scans log files for predefined keywords such as `error`, `fail`, `unauthorized`, `attack`, and `malware`.
- **Weighted Importance:** Allows assigning different weights to keywords to prioritize more critical terms like `attack` and `malware`.
- **Importance Threshold:** Filters lines based on a user-defined threshold, ensuring that only significant entries are flagged.
- **Failed Login Detection:** Detects failed login attempts by matching specific patterns (e.g., `Failed password for`, `Invalid user`, `Authentication failure`).
- **Multi-Log File Support:** Analyzes multiple log files simultaneously, including `/var/log/syslog`, `/var/log/auth.log`, and `/var/log/kern.log`.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/un1xr00t/logscan.git
   ```

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

