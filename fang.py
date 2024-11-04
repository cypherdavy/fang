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

# Function to get the default subdomain file
def get_subdomain_file():
    subdomain_file = "subdomain.txt"

    if not os.path.isfile(subdomain_file):
        print(colored(f"Subdomain file '{subdomain_file}' not found!", "red"))
        sys.exit(1)

    return subdomain_file

# Function to perform subdomain enumeration and save results
def enumerate_subdomains(domain):
    subdomain_file = get_subdomain_file()
    results = []

    # Simulate the enumeration process
    with open(subdomain_file, "r") as file:
        subdomains = file.readlines()
        valid_domains = []  # Store valid domains for printing
        for subdomain in tqdm(subdomains, desc="Enumerating subdomains"):
            subdomain = subdomain.strip()
            # Simulated request (replace with actual request logic)
            try:
                response = requests.get(f"http://{subdomain}.{domain}", timeout=1)
                if response.status_code == 200:
                    valid_domain = f"{subdomain}.{domain}"
                    results.append(f"{valid_domain}\n")
                    valid_domains.append(valid_domain)  # Collect valid domains
            except requests.RequestException:
                continue  # Ignore any request exceptions

    # Write results to a file
    output_file = f"{domain}_subdomains.txt"
    with open(output_file, "w") as outfile:
        outfile.writelines(results)

    # Print valid domains in terminal
    if valid_domains:
        print(colored("\nValid Subdomains Found:", "green", attrs=["bold"]))
        for valid in valid_domains:
            print(colored(valid, "green"))

    # Announce start of directory enumeration
    print(colored("\nNow we will start directory enumeration...", "cyan", attrs=["bold"]))
    # Placeholder for directory enumeration function call
    # enumerate_directories(domain)  # Uncomment this line once you implement the directory enumeration logic

# Main function to parse arguments and run the program
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Subdomain & Directory Enumerator")
    parser.add_argument("-d", "--domain", required=True, help="Domain to enumerate")
    args = parser.parse_args()

    run_intro()  # Display intro and loading animation
    enumerate_subdomains(args.domain)  # Start enumeration
_subdomains(subdomains_file, args.enumerate, args.rate)
