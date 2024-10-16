# CSP Validator

This is a Python project that validates if the `Content-Security-Policy` (CSP) of a website contains the required domains specified in a JSON file. The script fetches the CSP header from the provided URL, compares it against the required domains, and outputs a detailed report of the validation process.

## Features
- Fetches `Content-Security-Policy` from a specified URL.
- Converts the `Content-Security-Policy` to a JSON-like dictionary.
- Compares extracted CSP directives with required domains.
- Provides detailed reports on which domains are present or missing.
- Supports flexible comparison by normalizing domains (removing `http://` or `https://` for comparison).

## Requirements

- Python 3.x
- [Requests](https://pypi.org/project/requests/) library

## Setting up a Virtual Environment

1. Check if Python is installed: Open your terminal and run the following command to check if Python is installed:

   ```bash
   python --version
   ```

    Note: if python is not installed, download and install [here](https://www.python.org/downloads/).

2. Run the following command to create a virtual environment named `venv`:

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment using the command:

   ```bash
   .\venv\Scripts\activate
   ```
    The command to exit a virtual environment (venv) in Python is: `deactivate`

## Installing Dependencies

- Install the dependencies listed in the `requirements.txt` file using the following command:

   ```bash
   pip install -r requirements.txt
   ```

## Running

To run, open a terminal and navigate to your project's root directory. Then, execute the following command:
   ```bash
   python csp_validator.py <URL> <path_to_json>
   ```
