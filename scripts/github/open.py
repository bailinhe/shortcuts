#!/usr/bin/env python3

# This script will use the `gh` CLI to go to a GitHub repository based on user input.

import sys
import subprocess
import json

orgs = {
  "default": "equinixmetal",
  "em": "equinixmetal",
  "emh": "equinixmetal-helm",
  "mtb": "metal-toolbox",
  "ift": "infratographer",
  "infra9": "infratographer",
}

if len(sys.argv) < 2:
  print("No arguments provided")
  sys.exit(1)

input_text = sys.argv[1]
org = "default"
kw = input_text

# Check if input contains a space
if " " in input_text:
  first_part, rest = input_text.split(" ", 1)

  if first_part in orgs:
    org = first_part
    kw = rest

# Execute gh search repos command
org_name = orgs.get(org, org)
try:
  result = subprocess.run([
    'gh', 'search', 'repos',
    '--owner', org_name,
    kw,
    '--json=fullName,url'
  ], capture_output=True, text=True, check=True)

  # Parse JSON output
  repos = json.loads(result.stdout)

  if repos:
    # Print the URL of the first result
    first_repo = repos[0]
    print(first_repo['url'])
  else:
    print(f"No repositories found for '{kw}' in organization '{org_name}'")

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
