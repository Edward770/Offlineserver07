import requests
from colorama import Fore, Style, init
import time
import os
import hashlib
from urllib.parse import quote

# Initialize colorama for colored output
init(autoreset=True)

# Function to fetch IP and location details
def fetch_ip_info():
    try:
        response = requests.get("http://ip-api.com/json/")
        if response.status_code == 200:
            data = response.json()
            return {
                "ip": data.get("query", "N/A"),
                "country": data.get("country", "N/A"),
                "region": data.get("regionName", "N/A"),
                "city": data.get("city", "N/A")
            }
        else:
            print(f"{Fore.RED}Failed to fetch IP information.")
            return None
    except requests.RequestException as e:
        print(f"{Fore.RED}Error fetching IP info: {e}")
        return None

# Function to display IP and user information
def display_info():
    ip_info = fetch_ip_info()
    if ip_info:
        info = f"""
{Fore.YELLOW}< YOUR INFO >-----------------------------------------
[ IP ADDRESS ]: {ip_info['ip']}
[ TIME       ]: {time.strftime("%I:%M %p")}
[ DATE       ]: {time.strftime("%d/%B/%Y")}
------------------------------------------------------------
[ COUNTRY    ]: {ip_info['country']}
[ REGION     ]: {ip_info['region']}
[ CITY       ]: {ip_info['city']}
------------------------------------------------------------
"""
        print(info)
    else:
        print(f"{Fore.RED}Could not retrieve IP and location information.")

# Function to load data from a file
def load_from_file(file_path):
    if not os.path.exists(file_path):
        print(f"{Fore.RED}File not found: {file_path}")
        return []
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

# Function to send POST requests with retry logic
def send_post_request(url, json_data, retries=3):
    for attempt in range(retries):
        try:
            response = requests.post(url, json=json_data)
            if response.status_code == 200:
                return response
            else:
                print(f"{Fore.RED}Failed (Attempt {attempt + 1}/{retries}): {response.text}")
        except requests.RequestException as e:
            print(f"{Fore.RED}Error (Attempt {attempt + 1}/{retries}): {e}")
        time.sleep(1)  # Retry delay
    return None

# Function to start a new loader task
def start_loader(server_url):
    print(f"\n{Fore.YELLOW}--- Start a New Loader ---")
    convo_id = input(f"{Fore.CYAN}Enter Conversation ID: {Style.RESET_ALL}")
    hater_name = input(f"{Fore.CYAN}Enter Hater Name: {Style.RESET_ALL}")
    tokens_file = input(f"{Fore.CYAN}Enter Access Tokens File Path: {Style.RESET_ALL}")
    access_tokens = load_from_file(tokens_file)

    if not access_tokens:
        print(f"{Fore.RED}No tokens found!")
        return

    message_choice = input(f"{Fore.CYAN}Enter Messages (1: Manually, 2: File): {Style.RESET_ALL}")
    if message_choice == "1":
        messages = []
        print(f"{Fore.CYAN}Enter messages one per line (type 'END' to finish):{Style.RESET_ALL}")
        while True:
            message = input()
            if message.upper() == "END":
                break
            messages.append(message.strip())
    else:
        messages_file = input(f"{Fore.CYAN}Enter Message File Path: {Style.RESET_ALL}")
        messages = load_from_file(messages_file)

    timer = int(input(f"{Fore.CYAN}Enter Timer Interval (seconds): {Style.RESET_ALL}"))
    data = {
        "convo_id": convo_id,
        "tokens": access_tokens,
        "messages": messages,
        "hater_name": hater_name,
        "timer": timer
    }

    response = send_post_request(f"{server_url}/start_task", data)
    if response and response.status_code == 200:
        print(f"{Fore.GREEN}Loader started successfully!")
    else:
        print(f"{Fore.RED}Failed to start loader.")

# Main menu function
def menu(server_url):
    display_info()

    while True:
        print(f"""
{Fore.CYAN}< MENU >-------------------------------------------
[1] Start Loader
[2] Exit
------------------------------------------------------------
""")
        choice = input(f"{Fore.CYAN}Choose an option: {Style.RESET_ALL}")
        if choice == "1":
            start_loader(server_url)
        elif choice == "2":
            print(f"{Fore.GREEN}Exiting... Goodbye!")
            break
        else:
            print(f"{Fore.RED}Invalid choice! Try again.")

# Run the application
if __name__ == "__main__":
    SERVER_URL = "https://single-elbertine-hardikbisht-08ae26.koyeb.app/"
    menu(SERVER_URL)
    
