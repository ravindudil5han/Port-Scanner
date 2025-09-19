# Port-Scanner

This repository contains a simple, multithreaded TCP port scanner written in Python.

---

## Files included

* `port_scanner.py` — the main scanner script (the code you provided).
* `requirements.txt` — Python dependencies required to run the script.
* `README.md` — this file (usage, install, examples, and contribution notes).

---

## requirements.txt

```
# Minimal dependencies required to run the scanner
termcolor
pyfiglet
```

> You can pin version numbers if you prefer, e.g. `termcolor==1.1.0` and `pyfiglet==0.8.post1`, but unpinned packages are fine for a small utility.

---

## README.md

# Port-Scanner

A minimal, multithreaded TCP port scanner written in Python. It uses threads and a queue to scan a range or a list of ports, prints open ports, attempts a simple banner grab, and prints common service names when available.

**Repository:** `https://github.com/ravindudil5han/Port-Scanner.git`

### Features

* Multithreaded scanning using `threading` and `queue`
* Accepts port ranges (`1-1024`), comma-separated lists (`80,443,8080`), or single ports
* Attempts a basic banner grab for open ports
* Prints common service names using `socket.getservbyport`
* Nice ASCII banner using `pyfiglet` and colored output via `termcolor`

### Requirements

* Python 3.7+ (recommended Python 3.8 or newer)
* Packages listed in `requirements.txt` (install with pip)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/ravindudil5han/Port-Scanner.git
cd Port-Scanner
```

2. (optional) Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate     # Windows (PowerShell)
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

### Usage

Basic usage follows the CLI arguments implemented in the script.

```bash
python port_scanner.py <target> [-p PORTS] [-t THREADS] [-T TIMEOUT]
```

Examples:

* Scan the first 1024 ports (default):

```bash
python port_scanner.py example.com
```

* Scan ports 1–5000 with 100 threads and 0.3s timeout:

```bash
python port_scanner.py skymansion.site -p 1-5000 -t 100 -T 0.3
```

* Scan specific ports:

```bash
python port_scanner.py 192.0.2.1 -p 22,80,443
```

### CLI Options (implemented)

* `target` (positional): Hostname or IP to scan
* `-p`, `--ports`: Ports to scan (default `1-1024`). Can be a range `start-end`, a comma-separated list `80,443`, or a single port `22`.
* `-t`, `--threads`: Number of worker threads (default `50`).
* `-T`, `--timeout`: Socket timeout in seconds (default `0.5`).

### Notes and Recommendations

* Scanning networks or hosts you do not own or do not have explicit permission to test may be illegal. Always have authorization before scanning.
* For faster and stealthier scanning, consider tuning `threads` and `timeout` for your environment.
* Banner grabbing with a single `HEAD` request is best-effort and will vary by service.

### Suggested Improvements (ideas)

* Add logging to a file (CSV/JSON) with timestamps
* Add rate limiting and backoff for noisy scans
* Add UDP scanning (requires different approach)
* Add service fingerprinting and more robust banner parsing
* Add output formats (JSON, CSV)

### Contributing

Contributions are welcome. Open an issue to discuss changes before submitting a pull request. Please follow the repository's coding style and include tests for new functionality where applicable.

### License

Choose a license for your project. If you do not yet have a license, you can add one such as the MIT License. Example:

```
MIT License

Copyright (c) 2025 <Your Name>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## Quick checklist for repository

* Add `port_scanner.py` (rename the script file to `port_scanner.py` if you want clarity)
* Add this `README.md` to the repo
* Add `requirements.txt` (contents shown above)
* Optionally create a LICENSE file

---

If you want, I can:

* Produce a fully pinned `requirements.txt` with exact versions and hashes.
* Generate a short `LICENSE` file (MIT/Apache2/GPL).
* Produce a GitHub Actions workflow for automated linting or tests.

Tell me which one you want and I'll add it.
