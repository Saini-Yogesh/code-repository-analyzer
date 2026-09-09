import os
import requests

# Try to load environment variables from .env file if present
if os.path.exists(".env"):
    try:
        with open(".env", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    key, val = key.strip(), val.strip().strip('"').strip("'")
                    if key and key not in os.environ:
                        os.environ[key] = val
    except Exception as e:
        print(f"[!] Warning: Failed to load .env file: {e}")

USERNAME = os.getenv("GH_USERNAME")
TOKEN = os.getenv("GH_TOKEN")

all_repos = []

if TOKEN:
    print(f"[+] GITHUB_TOKEN found. Attempting to fetch public and private repositories for '{USERNAME}'...")
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {TOKEN}"
    }
    url = "https://api.github.com/user/repos"
    params = {"per_page": 100, "affiliation": "owner"}
    page = 1
    success_with_token = False
    
    try:
        while True:
            current_params = params.copy()
            current_params["page"] = page
            response = requests.get(url, headers=headers, params=current_params)
            response.raise_for_status()
            repos = response.json()
            if not repos:
                break
            
            # Filter to ensure we only get repos belonging to USERNAME
            for r in repos:
                if r.get("owner", {}).get("login", "").lower() == USERNAME.lower():
                    all_repos.append(r)
                    
            page += 1
            
        success_with_token = True
        print(f"[+] Successfully fetched {len(all_repos)} repository/repositories using token.")
    except Exception as e:
        print(f"[!] Token authentication failed or is invalid: {e}")
        success_with_token = False

    if not success_with_token:
        print(f"[-] Falling back to fetching public repositories for '{USERNAME}' without token...")
        TOKEN = None  # Clear token to trigger the fallback

if not TOKEN:
    headers = {"Accept": "application/vnd.github+json"}
    print(f"[-] Fetching public repositories for user '{USERNAME}'...")
    url = f"https://api.github.com/users/{USERNAME}/repos"
    params = {"per_page": 100, "type": "owner"}
    page = 1
    try:
        while True:
            current_params = params.copy()
            current_params["page"] = page
            response = requests.get(url, headers=headers, params=current_params)
            response.raise_for_status()
            repos = response.json()
            if not repos:
                break
            all_repos.extend(repos)
            page += 1
        print(f"[+] Successfully fetched {len(all_repos)} public repository/repositories.")
    except Exception as e:
        print(f"[!] Failed to fetch public repositories for '{USERNAME}': {e}")

clone_urls = []
for repo in all_repos:
    if isinstance(repo, dict) and "html_url" in repo:
        clone_urls.append(repo["html_url"])

# Deduplicate clone URLs preserving order
clone_urls = list(dict.fromkeys(clone_urls))

print(f"[+] Total repository URLs discovered: {len(clone_urls)}")

# Save clone_urls to a file
with open("clone_urls.txt", "w", encoding="utf-8") as f:
    for url in clone_urls:
        f.write(url + "\n")

print("Saved clone URLs to clone_urls.txt")
