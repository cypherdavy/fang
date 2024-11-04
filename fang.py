import requests
import argparse
import time
from termcolor import colored
from tqdm import tqdm
import sys
from colorama import init
import itertools
import threading

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
    print(colored("\tpython fang.py -f subdomains.txt -d example.com -e", "green", attrs=["underline"]))
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

# Main Function to Check Subdomains
def check_subdomains(subdomains_file, enumerate_dirs, rate_limit):
    # Read subdomains from the file
    with open(subdomains_file, "r") as file:
        subdomains = file.read().splitlines()

    # Directory list
    directories = ["/", "/admin", "/login", "/api", "/wp-admin", "/wp-login.php", "/cpanel", "/user", "/dashboard",
                   "/uploads", "/images", "/docs", "/includes", "/phpmyadmin", "/cgi-bin", "/backup", "/backups", 
                   "/dev", "/tmp", "/logs", "/config", "/.git", "/.svn", "/db", "/.env", "/.htaccess", "/.htpasswd", 
                   "/vendor", "/node_modules", "/api"]

    # Progress bar
    for subdomain in tqdm(subdomains, desc=colored("🦷 Scanning Subdomains", "cyan", attrs=["bold"])):
        if enumerate_dirs:
            for directory in directories:
                try:
                    url = f"http://{subdomain}.{args.domain}{directory}"
                    response = requests.get(url, timeout=5)
                    if response.status_code == 200:
                        print(colored(f"[+] {url} is accessible", "green"))
                    else:
                        print(colored(f"[-] {url} is down or forbidden", "red"))
                except requests.exceptions.RequestException as e:
                    print(colored(f"[!] Error checking {url}: {e}", "yellow"))
                time.sleep(rate_limit)  # Respect rate limit
        else:
            try:
                url = f"http://{subdomain}.{args.domain}"
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    print(colored(f"[+] {url} is accessible", "green"))
                else:
                    print(colored(f"[-] {url} is down or forbidden", "red"))
            except requests.exceptions.RequestException as e:
                print(colored(f"[!] Error checking {url}: {e}", "yellow"))
            time.sleep(rate_limit)  # Respect rate limit

# Command-line argument parsing
parser = argparse.ArgumentParser(description="Subdomain and Directory Enumerator - Aggressive Mode")
parser.add_argument("-f", "--file", help="File containing subdomains", required=True)
parser.add_argument("-d", "--domain", help="Target domain", required=True)
parser.add_argument("-e", "--enumerate", help="Enumerate directories", action="store_true")
parser.add_argument("-r", "--rate", help="Rate limit requests (seconds)", type=float, default=0.5)
args = parser.parse_args()

# Run the fancy intro
run_intro()

# Call the main function with provided arguments
check_subdomains(args.file, args.enumerate, args.rate)
