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

USERNAME = os.getenv("GITHUB_USERNAME", "Saini-Yogesh")
TOKEN = os.getenv("GITHUB_TOKEN")

headers = {"Accept": "application/vnd.github+json"}

if TOKEN:
    print("[+] GITHUB_TOKEN found. Fetching all public & private repositories owned by user...")
    headers["Authorization"] = f"Bearer {TOKEN}"
    url = "https://api.github.com/user/repos"
    params = {"per_page": 100, "affiliation": "owner"}
else:
    print(f"[-] No GITHUB_TOKEN found. Fetching public repositories for user '{USERNAME}'...")
    url = f"https://api.github.com/users/{USERNAME}/repos"
    params = {"per_page": 100, "type": "owner"}

page = 1
all_repos = []

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

clone_urls = []
for repo in all_repos:
    clone_urls.append(repo["html_url"])

print(len(clone_urls))

# save clone_urls to a file
with open("clone_urls.txt", "w") as f:
    for url in clone_urls:
        f.write(url + "\n")

print("Saved clone URLs to clone_urls.txt")