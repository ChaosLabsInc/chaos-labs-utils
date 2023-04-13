import sys
import os
import requests

PATH, _ = os.path.split(os.path.realpath(__file__))

BORROWERS_PATH = f"{PATH}/../src/borrowers.sol"

CHAIN = str(sys.argv[1])
FETCH_BY_BLOCK_NUMBER = ""

try:
    BLOCK_NUMBER = sys.argv[2]
    FETCH_BY_BLOCK_NUMBER = f", where: {{_change_block: {{ number_gte: {BLOCK_NUMBER}}}}}"
except:
    pass

AAVE_GRAPH_URLS = {
    "polygon": "https://api.thegraph.com/subgraphs/name/aave/protocol-v3-polygon",
    "avalanche": "https://api.thegraph.com/subgraphs/name/aave/protocol-v3-avalanche",
    "arbitrum": "https://api.thegraph.com/subgraphs/name/aave/protocol-v3-arbitrum",
    "optimism": "https://api.thegraph.com/subgraphs/name/aave/protocol-v3-optimism",
    "ethereum": "https://api.thegraph.com/subgraphs/name/aave/protocol-v3",
}

print(f"start fetching borrowers from CHAIN {CHAIN}")

addresses = []

aave_top_account_per_reserve = f"""  {{pools{{
reserves{{
  symbol
  userReserves(first:5, orderBy: currentATokenBalance, orderDirection: desc, {FETCH_BY_BLOCK_NUMBER}){{
    user{{
      id
    }}
  }}
}}
}}
}}
"""

response = requests.post(
    AAVE_GRAPH_URLS[CHAIN], json={"query": aave_top_account_per_reserve}, timeout=5)
data = response.json()['data']['pools'][0]['reserves']
print("finished fetching borrowers")
for reserve_data in data:
    for account_data in reserve_data['userReserves']:
        addresses.append(account_data['user']['id'])

print("before remove duplicates: ", len(addresses))
addresses = list(dict.fromkeys(addresses))
print("after remove duplicates: ", len(addresses))

addresses_code = ""
for address in addresses:
    pad_address = "address(" + address[0:2] + \
        "00" + address[2:len(address)] + "),"
    addresses_code += pad_address

with open(BORROWERS_PATH, 'w') as f:
    template = f"""
  // SPDX-License-Identifier: MIT
pragma solidity ^0.8.16;

contract Constants {{
address[] public arr;

function getBorrowers() public returns (address[] memory) {{
  arr = [
{addresses_code[0:-1]}
  ];
  return arr;
}}
}}

  """
    f.write(template)

os.system("npx prettier --write src/*")
print(f"update borrowers in: {BORROWERS_PATH}")
