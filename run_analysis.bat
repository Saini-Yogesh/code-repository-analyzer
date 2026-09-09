@echo off
REM Step 1: Install required Python dependencies
echo Installing requirements...
python -m pip install -r requirements.txt

REM Step 2: Fetch all repository URLs owned by your account
echo Fetching repository URLs...
python fetch_all_repo.py

REM Step 3: Run full batch analysis on all repositories
echo Starting batch repository analysis...
python Repo_analysis_tool.py --batch clone_urls.txt

echo Analysis Complete! Check the ./outputs folder for results.
pause

