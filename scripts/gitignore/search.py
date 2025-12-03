#!/usr/bin/env python3

# This script will use the `gh` CLI to search for .gitignore files based on user input.

import sys
import subprocess
import json
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

import threading
from concurrent.futures import ThreadPoolExecutor

thread_local = threading.local()

REPO = 'github/gitignore'
REF = 'heads/main'
DOWNLOAD_BASE_URL = f'https://raw.githubusercontent.com/{REPO}/refs/{REF}'
MAX_WORKERS = 5

shorthands = {
  "vscode": "VisualStudioCode",
  "mac": "macOS",
}

if len(sys.argv) < 2:
  print("No arguments provided")
  sys.exit(1)

input_text = sys.argv[1]
kws = []

# Split input
if " " in input_text:
  parts = input_text.split(" ")

  for i, part in enumerate(parts):
    if part in shorthands:
      part = shorthands[part]

    kws.append(part)

def search_gitignore(kw):
  '''
  Search for a .gitignore file in the specified repository.
  
  :param kw: Description
  '''

  fn = f"{kw}.gitignore"

  try:
    cmd_result = subprocess.run([
      'gh', 'search', 'code', '--repo', REPO,
      fn, 'in:path',
      '--json=path',
    ], capture_output=True, text=True, check=True)

    paths = json.loads(cmd_result.stdout)

    if len(paths) > 0:
      return paths[0]['path']

    return ''

  except subprocess.CalledProcessError as e:
    print(f"Error running gh command: {e}")
    print(f"stderr: {e.stderr}")
    sys.exit(1)
  except json.JSONDecodeError as e:
    print(f"Error parsing JSON output: {e}")
    sys.exit(1)
  except FileNotFoundError:
    print("Error: 'gh' command not found. Please install GitHub CLI.")
    sys.exit(1)

def download_file(path):
  '''
  Download the specified file from the repository.
  
  :param path: Path to the file in the repository.
  '''

  if not path:
    return ''

  url = f"{DOWNLOAD_BASE_URL}/{path}"

  try:
    with urlopen(url) as response:
      return response.read().decode('utf-8')

  except HTTPError as e:
    print(f"HTTP Error {e.code}: {e.reason} for {url}")
    return ''
  except URLError as e:
    print(f"URL Error: {e.reason} for {url}")
    return ''

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
  files = executor.map(search_gitignore, kws)
  for f in files:
    content = download_file(f)
    if content:
      print(f"# {DOWNLOAD_BASE_URL}/{f}\n")
      print(content)
