# 🦷 Fang - The Aggressive Subdomain & Directory Enumerator

![Fang Logo](https://ibb.co/qypYmfH)

Welcome to **Fang**! This powerful tool is designed for cybersecurity enthusiasts and ethical hackers looking to hunt for vulnerabilities through subdomain and directory enumeration. Whether you're performing a security assessment or simply exploring the depths of the web, **Fang** has your back!

---

## Features

- **Aggressive Scanning**: Quickly and efficiently enumerate subdomains and directories.
- **Custom User-Agent**: Bypass restrictions with customizable headers.
- **Multi-threaded Requests**: Speed up your scans with multi-threading.
- **Detailed Logging**: Keep track of your scans with comprehensive log files.
- **Interactive Feedback**: Enjoy colorful terminal output and a dynamic progress bar.

---

## Installation

### Prerequisites

- Python 3.6 or higher
- `pip` for managing Python packages

### Steps

1. **Clone the repository**:
   ```bash
  git clone https://github.com/cypherdavy/fang.git
   cd fang ```

## Usage

### Command-Line Options

Run **Fang** using the following command structure:

```bash
python fang.py -f <subdomains_file> -d <target_domain> [-e] [-r <rate>] [-u <user_agent>]
```

### Arguments

- `-f`, `--file`: **(Required)** Path to the file containing subdomains (one per line).
- `-d`, `--domain`: **(Required)** Target domain to enumerate.
- `-e`, `--enumerate`: **(Optional)** Flag to enable directory enumeration.
- `-r`, `--rate`: **(Optional)** Set a rate limit for requests (in seconds). Default is `0.5`.
- `-u`, `--user-agent`: **(Optional)** Custom User-Agent string. Default is `Mozilla/5.0`.

### Example Commands

**Subdomain Scan**:
```bash
python fang.py -f subdomains.txt -d example.com
```

**Directory Enumeration**:
```bash
python fang.py -f subdomains.txt -d example.com -e
```
## Contributing

We welcome contributions to **Fang**! If you have ideas, improvements, or fixes, please submit a pull request or open an issue.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a pull request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Author

**Fang** is made with ❤️ by [cipherdavy](https://github.com/yourusername).

**Stay sharp, and happy hunting! 🦷**
