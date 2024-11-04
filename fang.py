import requests
import argparse
import time
from termcolor import colored
from tqdm import tqdm
import sys
from colorama import init
import itertools
import threading
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin

# Initialize Colorama
init()

# ASCII Art and Fancy Introduction
def print_intro():
    fang_art = """
      █████▒█      ██  ▄████▄   ▄▄▄        ██████
    ▓██   ▒██   ██ ▒██▀ ▀█  ▒████▄    ▒██ ▒   ██▒
    ▒████ ░██   ██ ▒▓█    ▄ ▒██  ▀█▄  ▒██ ░████ ░
    ░▓█▒  ▒██  ██ ▒▒▓▓▄ ▄██ ░██▄▄▄▄██ ░██ ░▓█▒  ░
    ░▒█░   ▒▀██▀▒▒ ▒ ▓███▀   ▓█   ▓██▒▒██ ░▒█░   ░
     ▒ ░    ▒██▒   ░ ░▒ ▒  ░ ▒▒   ▓▒█░▒▒ ▒ ░    ░
     ░     ▒▒▒▒▒▒▒▒ ░  ░       ░ ▒  ░ ░▒ ░ ░  ░
      ░░░░░░░▒▒▒▒▒░   ░ ░ ░    ░ ░░░▒░ ░ ░ ░ ░ ░
            ░░░░░     ░    ░   ░ ░ ░     ░░
   """
    print(colored(fang_art, "red", attrs=["bold"]))
    print(colored("\n\tSUBDOMAIN & DIRECTORY ENUMERATOR\n", "cyan", attrs=["bold"]))
    print(colored("\t         ~ Made by cipherdavy ~\n", "green", attrs=["bold"]))
    print(colored("\t  ⚡ Hunt the Web Like a Predator ⚡\n", "yellow", attrs=["bold"]))
    print(colored("Usage:", "blue", attrs=["bold"]))
    print(colored("\tpython fang.py -d example.com", "green", attrs=["underline"]))
    print("\n" + "=" * 70 + "\n")

# Event for stopping the loading animation
stop_event = threading.Event()

# Loading Animation
def loading_animation():
    for frame in itertools.cycle(["|", "/", "-", "\\"]):
        if stop_event.is_set():  # Check if we should stop
            break
        sys.stdout.write(colored(f"\rLoading FANG... {frame}", "yellow", attrs=["bold"]))
        sys.stdout.flush()
        time.sleep(0.1)

# Run Intro with Loading Animation
def run_intro():
    global stop_event
    stop_event.clear()  # Clear the event at the start
    intro_thread = threading.Thread(target=loading_animation)
    intro_thread.start()
    time.sleep(3)  # Simulate loading time
    stop_event.set()  # Signal the thread to stop
    intro_thread.join()  # Wait for the thread to finish
    sys.stdout.write("\r" + " " * 20 + "\r")  # Clear line after loading
    print_intro()

# Directory patterns to search for in enumeration
common_directories = [
    "admin", "login", "uploads", "api", "dashboard", "images",
    "css", "js", "static", "files", "scripts", "data", "backup",
    ".git", ".env", "config", "archive"
]

file_extensions = [".php", ".html", ".js", ".bak", ".old", ".zip"]

# Recursive directory scanner function
def recursive_scan(url, depth=1, max_depth=2, found_directories=set()):
    if depth > max_depth:
        return found_directories

    print(colored(f"\nScanning directories at depth {depth}: {url}", "yellow"))

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(scan_directory, urljoin(url, dir_)): dir_ for dir_ in common_directories}
        for future in as_completed(future_to_url):
            try:
                subdir_url = future_to_url[future]
                is_valid = future.result()
                if is_valid:
                    print(colored(f"Valid directory found: {urljoin(url, subdir_url)}", "green"))
                    found_directories.add(urljoin(url, subdir_url))
                    recursive_scan(urljoin(url, subdir_url), depth + 1, max_depth, found_directories)
            except Exception as e:
                continue
    return found_directories

# Helper function for scanning directories
def scan_directory(directory_url):
    try:
        response = requests.get(directory_url, timeout=3)
        if response.status_code == 200:
            return True
    except requests.RequestException:
        return False
    return False

# Advanced directory enumeration
def enumerate_directories(domain, max_depth=2):
    print(colored("\nStarting Advanced Directory Enumeration...", "cyan", attrs=["bold"]))
    url = f"http://{domain}"
    found_directories = recursive_scan(url, max_depth=max_depth)

    # Search for files in the found directories
    print(colored("\nChecking for specific files in directories...", "cyan", attrs=["bold"]))
    for directory in found_directories:
        for ext in file_extensions:
            file_url = f"{directory}{ext}"
            try:
                response = requests.get(file_url, timeout=2)
                if response.status_code == 200:
                    print(colored(f"File found: {file_url}", "green"))
            except requests.RequestException:
                continue

    # Save found directories to file
    output_file = f"{domain}_advanced_directories.txt"
    with open(output_file, "w") as f:
        f.write("\n".join(found_directories))
    print(colored(f"\nResults saved to {output_file}", "yellow"))

# Main function to parse arguments and run the program
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advanced Subdomain & Directory Enumerator")
    parser.add_argument("-d", "--domain", required=True, help="Domain to enumerate")
    parser.add_argument("--depth", type=int, default=2, help="Max depth for recursive directory search")
    args = parser.parse_args()

    run_intro()  # Display intro and loading animation
    enumerate_directories(args.domain, args.depth)  # Start advanced directory enumeration
