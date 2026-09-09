# Repository Intelligence Batch Analyzer

A lightweight tool that scans all repositories owned by a GitHub user, collects various metrics (LOC, language breakdown, CI status, etc.) and writes detailed reports to an `outputs` directory. The workflow can be run locally or automatically via GitHub Actions.

---

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Setup &amp; Running Locally](#setup--running-locally)
- [Running on GitHub Actions](#running-on-github-actions)
- [Configuration Details](#configuration-details)
- [Customizing the Analysis](#customizing-the-analysis)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The repository contains two main components:

1. **`fetch_all_repo.py`** – Retrieves every repository URL for the specified GitHub account (public repos by default; private repos when a token is supplied).
2. **`Repo_analysis_tool.py`** – Performs the heavy‑lifting analysis (cloc, commit history, CI detection, etc.) on the cloned repositories and writes JSON/CSV reports under `outputs/`.

A GitHub Actions workflow (`.github/workflows/analyze_repos.yml`) ties everything together, allowing you to trigger a full batch run with a single button click.

---

## Prerequisites

| Requirement                                       | Version                                                                                                                                                                   |
| ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Python**                                  | `3.10` (or later) – the workflow uses `actions/setup-python@v5`                                                                                                      |
| **Git**                                     | Any recent version (required for cloning)                                                                                                                                 |
| **cloc**                                    | Installed by the workflow (`sudo apt-get install -y cloc`). If running locally, install it via your package manager (`brew install cloc`, `apt install cloc`, etc.) |
| **GitHub Personal Access Token** (optional) | Needs`repo` scope for private repositories. Store it as a secret named `GH_TOKEN`.                                                                                    |
| **GitHub Username**                         | Store as a secret named`GH_USERNAME`.                                                                                                                                   |

## Setup & Running Locally

1. **Clone the repository**

   ```bash
   git clone https://github.com/Saini-Yogesh/code-repository-analyzer.git
   cd code-repository-analyzer
   ```
2. **Create a `.env` file** (or export environment variables). Example based on `env.example`:

   ```text
   GH_TOKEN=your-github-personal-access-token   # optional – required for private repos
   GH_USERNAME=your-github-username
   ```

   > **Tip:** Omit `GH_TOKEN` if you only need to analyse public repositories.
   >
3. **Install Python dependencies**

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. **Fetch all repository URLs**

   ```bash
   python fetch_all_repo.py
   ```

   This creates a `clone_urls.txt` file containing one URL per line.
5. **Run the analysis**

   ```bash
   python Repo_analysis_tool.py --batch clone_urls.txt --github-token "$GH_TOKEN" --output-dir ./outputs
   ```

   All reports are placed in the `outputs/` directory.
6. **(Optional) Windows helper**

   ```powershell
   ./run_analysis.bat
   ```

   The batch file runs the three steps above sequentially.

---

## Running on GitHub Actions

The repo ships with a ready‑to‑use workflow that performs the same steps on an `ubuntu-latest` runner.

### 1️⃣ Add the required secrets

1. Go to **Settings → Secrets and variables → Actions → New repository secret**.
2. Create the following secrets (replace the example values with your own):

   - `GH_TOKEN` – your personal access token (optional for public repos only).
   - `GH_USERNAME` – your GitHub user name.

   > **Important:** Secret names **must not** start with `GITHUB_`.
   >

### 2️⃣ Trigger the workflow

- Navigate to the **Actions** tab → select **Repository Intelligence Batch Analysis** → click **Run workflow**.
- The workflow will:
  1. Checkout the repository.
  2. Install `cloc` and Python dependencies.
  3. Run `fetch_all_repo.py`.
  4. Execute `Repo_analysis_tool.py` on every repo.
  5. Push the generated `outputs/` files to a new branch named `output-of-<username>` (or `output-of-<username>-N` if the branch already exists).

### 3️⃣ View the results

- After the run finishes, check the new branch in the **Code** view. The `outputs/` folder contains all CSV/JSON reports.
- You can also download the artifacts directly from the workflow run page.

---

## Configuration Details

| File                                    | Purpose               | Customisation points                                                           |
| --------------------------------------- | --------------------- | ------------------------------------------------------------------------------ |
| `fetch_all_repo.py`                   | Retrieves repo URLs.  | Change pagination or add filters.                                              |
| `Repo_analysis_tool.py`               | Core analysis engine. | Adjust rating thresholds, enable/disable stages, or add new metric collectors. |
| `.github/workflows/analyze_repos.yml` | CI pipeline.          | Edit Python version, environment variables, or output‑branch naming.          |

---

## Customizing the Analysis

- **Adjust Rating Criteria** – Edit the `RATING_CRITERIA` dictionary in `Repo_analysis_tool.py`.
- **Skip Files/Directories** – Modify `SKIP_DIRS` and `SKIP_EXTENSIONS` in the same file.
- **Add New Metrics** – Implement additional functions and call them from the analysis pipeline.

---

## Troubleshooting

- **`actions/checkout` token error** – Ensure the `GH_TOKEN` secret exists. If you only need public repos, the workflow will fall back to the built‑in `github.token`.
- **Rate‑limit errors** – Use a token with a higher quota or add a short `sleep` between API calls in `fetch_all_repo.py`.
- **Missing `cloc`** – Install it locally (`brew install cloc`, `apt install cloc`, etc.). The workflow installs it automatically.
- **Empty `outputs/`** – Verify `clone_urls.txt` contains URLs and that the token (if used) has cloning permission.

---

## Contributing

Contributions are welcome! Feel free to:

- Open an issue for bugs or feature requests.
- Fork the repo and submit a pull request.
- Add support for other VCS providers (GitLab, Bitbucket) – placeholders already exist.

---

*Happy analysing!*
