import sys
import requests
import os

path, _ = os.path.split(os.path.realpath(__file__))

BORROWERS_PATH = f"{path}/../src/borrowers.sol"

 chain = str(sys.argv[1])
  fetch_by_block_number = ""

   try:
        block_number = sys.argv[2]
        fetch_by_block_number = f", where: {{_change_block: {{ number_gte: {block_number}}}}}"
    except:
        pass

    AAVE_GRAPH_URLS = {
        "polygon": "https://api.thegraph.com/subgraphs/name/ronlv10/aave-v3-polygon",
        "avalanche": "https://api.thegraph.com/subgraphs/name/yonach/aave-v3-avalanche",
        "arbitrum": "https://api.thegraph.com/subgraphs/name/ronlv10/aave-v3-arbitrum",
        "optimism": "https://api.thegraph.com/subgraphs/name/ronlv10/aave-v3-optimism-fix",
        "ethereum": "https://api.thegraph.com/subgraphs/name/aave/protocol-v3",
    }

    print(f"start fetching borrowers from chain {chain}")

    addresses = []

    aave_top_account_per_reserve = f"""  {{pools{{
      reserves{{
        symbol
        userReserves(first:5, orderBy: currentATokenBalance, orderDirection: desc, {fetch_by_block_number}){{
          user{{
            id
          }}
        }}
      }}
    }}
    }}
      """

    response = requests.post(
        AAVE_GRAPH_URLS[chain], json={"query": aave_top_account_per_reserve}, )
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
