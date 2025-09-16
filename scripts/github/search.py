#!/usr/bin/env python3

import sys
from urllib.parse import quote

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

print(f"https://github.com/{orgs.get(org, org)}?q={quote(kw)}")
