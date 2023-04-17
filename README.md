# Chaos Labs Utils

This package contains a contract that enables extended testing coverage within the Aave protocol using Foundry.

## Getting Started

These tests allow you to fetch the health factor of the aave borrowers to validate the differences before and after the payload execution.

### Prerequisites

* Python - please follow the [instructions](https://packaging.python.org/en/latest/tutorials/installing-packages/) to install Python.

    - install requirements:
        ```bash
        pip install -r requirements.txt
        ```

## Usage with Foundry
With Foundry installed and in a Git repository:

```bash
forge install https://github.com/ChaosLabsInc/chaos-labs-utils —no-commit
```

## Usage with payload test contract

### Usage example 
YourPayloadTest.Sol:
```
    import {SanityChecks} from 'chaos-labs-utils/SanityChecks.sol';
    import {TestWithExecutor} from 'aave-helpers/GovHelpers.sol';
    import {YourPayload} from '../YourPayload.sol';

    ...

    contract YourPayloadTest is TestWithExecutor, SanityChecks {

      function setUp() public {
        vm.createSelectFork(vm.rpcUrl('{chain}'), 16974783);
        _selectPayloadExecutor({{chain_executor});
      }
  
      function testPayload() public {
        uint256[] memory healthsBefore = _testBorrowrsHealth(AaveV3{chain}.POOL);

        // 2. Execute payload
        _executePayload(address(new YourPayload()));

        uint256[] memory healthsAfter = _testBorrowrsHealth(AaveV3{chain}.POOL);

        validateBorrowersHealth(healthsBefore, healthsAfter, 1_00);
    }
}
```
### Functions definition

```_testBorrowrsHealth()```

This function returns all borrowers' health for the given protocol status.

```validateBorrowersHealth(healthsBefore, healthsAfter, changeTolerancePercentage)```

This function compares the health of the borrowers before and after the execution for a given tolerance percentage (1_00 represents +-1%, for zero tolerance pass 0).


## Usage MakeFile
Recommended practice to add to Makefile:
```solidity
test-name :; python3 lib/chaos-labs-utils/scripts/fetch-borrowers.py {chain_name} {block_number} && forge test -vvv --match-contract YourPayloadTest
```

Example for running tests and fetching borrowers from the latest block update on the graph:
```
test-name :; python3 lib/chaos-labs-utils/scripts/fetch-borrowers.py ethereum 16925078 && forge test -vvv --match-contract AaveEthV3PayloadTest
```

Another option - running the Python script lib/chaos-labs-utils/scripts/fetch-borrowers.py before running the test:
```bash
python3 lib/chaos-labs-utils/scripts/fetch-borrowers.py {chain_name} {block_number}
```

### Script argumansts
* chain_name - The name of the chain from this supported list: ```[polygon, avalanche, arbitrum, optimism, ethereum]```
* block_number - this is an optional argument; if nothing is passed, the script fetches the borrowers from the latest block in the graph.

## Borrowers Fetch Logic
For each reserve(token) of the chain, we fetch the top 5 suppliers that borrowed from at least one reserver - this should assure us that their health factor is less than infinite.

## FAQs

**Q: I got a timeout error while running the Python script ```requests.exceptions.ReadTimeout: HTTPSConnectionPool(host='api.thegraph.com', port=443): Read timed out.```**

**A:** This can happen for many reasons; please try to rerun the script.


**Q: I got an error while running the payload test**

**A:**  First iteration can fail on latency to archive node to fetch all the balances for the test; rerunning will help.


**Q: I got the required message "Health factor changed more than the set tolerance percentage." but the payload didn't change collateral parameters**

**A:** This should not happen; we advise you to check if the payload is correct. 
