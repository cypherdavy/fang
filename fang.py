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

# Function to create a default subdomain file if it doesn't exist
def create_default_subdomain_file():
    default_subdomains = [
        "www", "api", "mail", "blog", "support", "dev", "test", "secure", "shop", "m", "forum"
    ]
    with open("subdomain.txt", "w") as file:
        for subdomain in default_subdomains:
            file.write(f"{subdomain}\n")
    print(colored("Created 'subdomain.txt' with default subdomains.", "yellow"))

# Function to get the default subdomain file
def get_subdomain_file():
    if not os.path.isfile("subdomain.txt"):
        print(colored("Subdomain file 'subdomain.txt' not found!", "red"))
        create_default_subdomain_file()  # Create the file if it doesn't exist
    return "subdomain.txt"

# Function to check if a subdomain is valid
def is_valid_subdomain(subdomain, domain):
    try:
        # Check both HTTP and HTTPS
        for scheme in ["http", "https"]:
            response = requests.get(f"{scheme}://{subdomain}.{domain}", timeout=2)
            if response.status_code == 200:
                return True
    except requests.RequestException:
        return False
    return False

# Function to perform subdomain enumeration and save results
def enumerate_subdomains(domain):
    subdomain_file = get_subdomain_file()
    results = []

    print(colored("🦷 Scanning Subdomains...", "cyan", attrs=["bold"]))
    with open(subdomain_file, "r") as file:
        subdomains = file.readlines()
        valid_domains = []  # Store valid domains for printing
        for subdomain in tqdm(subdomains, desc="Scanning Subdomains"):
            subdomain = subdomain.strip()
            if is_valid_subdomain(subdomain, domain):
                valid_domain = f"{subdomain}.{domain}"
                results.append(f"{valid_domain}\n")
                valid_domains.append(valid_domain)  # Collect valid domains

    # Write results to a file
    output_file = f"{domain}_subdomains.txt"
    with open(output_file, "w") as outfile:
        outfile.writelines(results)

    # Print valid domains in terminal
    if valid_domains:
        print(colored("\nValid Subdomains Found:", "green", attrs=["bold"]))
        for valid in valid_domains:
            print(colored(valid, "green"))
    else:
        print(colored("\nNo valid subdomains found.", "yellow"))

    # Announce start of directory enumeration
    print(colored("\nNow we will start directory enumeration...", "cyan", attrs=["bold"]))
    enumerate_directories(domain)  # Call the directory enumeration function

# Function to perform directory enumeration
def enumerate_directories(domain):
    # List of common directories for testing
    common_directories = [
        "admin", "login", "uploads", "api", "dashboard", "images", 
        "css", "js", "static", "files", "scripts", "data"
    ]
    results = []

    print(colored("\nScanning Directories...", "cyan", attrs=["bold"]))
    for directory in tqdm(common_directories, desc="Scanning Directories"):
        try:
            # Check both HTTP and HTTPS
            for scheme in ["http", "https"]:
                response = requests.get(f"{scheme}://{domain}/{directory}", timeout=2)
                if response.status_code == 200:
                    result = f"Valid directory found: {directory} at {domain}/{directory}\n"
                    results.append(result)
                    print(colored(result.strip(), "green"))
        except requests.RequestException:
            continue  # Ignore any request exceptions

    # Save directory results to a file
    directory_output_file = f"{domain}_directories.txt"
    with open(directory_output_file, "w") as dir_outfile:
        dir_outfile.writelines(results)

# Main function to parse arguments and run the program
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Subdomain & Directory Enumerator")
    parser.add_argument("-d", "--domain", required=True, help="Domain to enumerate")
    args = parser.parse_args()

    run_intro()  # Display intro and loading animation
    enumerate_subdomains(args.domain)  # Start enumeration
