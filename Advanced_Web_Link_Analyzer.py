import os
import re
import sys
import time
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore, Style

# Initialize colorama for Windows/Linux
init(autoreset=True)

# ============ BANNER & ANIMATION ============
def print_banner():
    banner = f"""
{Fore.GREEN}{'='*50}
{Fore.CYAN}███╗   ██╗ ██████╗ ████████╗ █████╗ ██████╗ ██╗     ███████╗
{Fore.CYAN}████╗  ██║██╔═══██╗╚══██╔══╝██╔══██╗██╔══██╗██║     ██╔════╝
{Fore.CYAN}██╔██╗ ██║██║   ██║   ██║   ███████║██████╔╝██║     █████╗  
{Fore.CYAN}██║╚██╗██║██║   ██║   ██║   ██╔══██║██╔══██╗██║     ██╔══╝  
{Fore.CYAN}██║ ╚████║╚██████╔╝   ██║   ██║  ██║██║  ██║███████╗███████╗
{Fore.CYAN}╚═╝  ╚═══╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝
{Fore.GREEN}{'='*50}
{Fore.YELLOW}         [⚡] Advanced Web Link Analyzer [⚡]
{Fore.MAGENTA}         [👤] Coded by: darkboss1bd
{Fore.GREEN}{'='*50}
"""
    animate_text(banner)
    print(f"\n{Fore.WHITE}[🔍] Initializing darkboss1bd's Link Analyzer...\n")
    time.sleep(1)

def animate_text(text, delay=0.005):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def hacker_animation():
    animation = "|/-\\"
    for i in range(20):
        sys.stdout.write(f"\r{Fore.GREEN}[{animation[i % 4]}] Scanning for hidden links... {darkboss_progress(i, 20)}")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write(f"\r{Fore.GREEN}[✓] Scan complete!\n\n")

def darkboss_progress(current, total):
    percent = (current / total) * 100
    return f"{Fore.CYAN}[{'█' * (current // 2)}{'░' * (50 - current // 2)}] {int(percent)}%"

# ============ MAIN FUNCTION ============
def find_hidden_links(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[❌] Error fetching the URL: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    hidden_links = []

    # 1. Find all <a> tags with display:none or visibility:hidden
    for tag in soup.find_all('a', href=True):
        style = tag.get('style', '')
        if 'display:none' in style or 'visibility:hidden' in style:
            hidden_links.append({
                'type': 'Hidden via CSS',
                'url': tag['href'],
                'text': tag.get_text(strip=True)
            })

    # 2. Find links in comments
    comments = soup.find_all(string=lambda text: isinstance(text, str) and '<a ' in text and 'href' in text)
    for comment in comments:
        links = re.findall(r'href=["\'](https?://[^"\']+)["\']', comment)
        for link in links:
            hidden_links.append({
                'type': 'Link in HTML Comment',
                'url': link,
                'text': 'Found in comment'
            })

    # 3. Find links in JavaScript (simple regex-based)
    scripts = soup.find_all('script')
    js_patterns = [
        r'(https?://[^\s"\']+)',
        r"window\.location\.href\s*=\s*['\"](https?://[^\s'\"]+)['\"]",
        r"window\.open\(['\"](https?://[^\s'\"]+)['\"]"
    ]
    for script in scripts:
        if script.string:
            for pattern in js_patterns:
                matches = re.findall(pattern, script.string)
                for match in matches:
                    hidden_links.append({
                        'type': 'JavaScript Redirect or Link',
                        'url': match,
                        'text': 'Found in JS'
                    })

    # 4. Find iframes (often used to hide content)
    for iframe in soup.find_all('iframe', src=True):
        hidden_links.append({
            'type': 'Embedded iframe',
            'url': iframe['src'],
            'text': 'Iframe source'
        })

    # 5. Off-screen positioning (e.g., left: -9999px)
    for tag in soup.find_all(['a', 'div'], href=True):
        style = tag.get('style', '')
        if 'position:absolute' in style and ('left:-' in style or 'top:-' in style):
            hidden_links.append({
                'type': 'Off-screen positioned link',
                'url': tag['href'],
                'text': tag.get_text(strip=True)
            })

    return hidden_links

# ============ DISPLAY RESULTS ============
def show_results(url, links):
    print(f"{Fore.WHITE}[🌐] Target URL: {Fore.YELLOW}{url}")
    print(f"{Fore.WHITE}[🔎] Total Hidden Links Found: {Fore.RED}{len(links)}\n")

    if not links:
        print(f"{Fore.GREEN}[✅] No hidden links detected. Site looks clean!")
    else:
        for idx, link in enumerate(links, 1):
            print(f"{Fore.CYAN}[🔗 {idx}] Type: {Fore.MAGENTA}{link['type']}")
            print(f"      URL: {Fore.BLUE}{link['url']}")
            print(f"      Text/Info: {Fore.WHITE}{link['text']}\n")

# ============ MAIN ============
def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_banner()

    while True:
        url = input(f"{Fore.GREEN}[📥] Enter website URL (or 'quit' to exit): {Style.BRIGHT}").strip()
        if url.lower() in ['quit', 'exit', 'q']:
            print(f"\n{Fore.MAGENTA}[👋] Goodbye from darkboss1bd! Stay ethical. 🖤")
            break

        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        print(f"\n{Fore.YELLOW}[🚀] Analyzing {url} for hidden links...\n")
        hacker_animation()

        results = find_hidden_links(url)
        show_results(url, results)

        print(f"\n{Fore.CYAN}{'-'*60}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}[!] Process interrupted by user. Exiting gracefully...")
        print(f"{Fore.MAGENTA}[👤] darkboss1bd says: Stay curious, stay safe.")
    except Exception as e:
        print(f"{Fore.RED}[💥] An unexpected error occurred: {e}")