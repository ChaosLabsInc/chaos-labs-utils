# Chaos Labs Utils

This repository contains tests frame work to test 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites


* python
```
Give examples
```

## Usage with foundry
With Foundry installed and being in a Git repository:

```
forge install https://github.com/ChaosLabsInc/chaos-labs-utils
```

## Usage with payload test contract

### Usage example
```
    import {SanityChecks} from 'chaos-labs-utils/SanityChecks.sol';
    ...

    contract YourPayloadTest is SanityChecks {

      function testPayload() public {
        uint256[] memory healthsBefore = _testBorrowrsHealth(AaveV3{chain}.POOL);

        // 2. execute payload
        _executePayload(address(proposalPayload));

        uint256[] memory healthsAfter = _testBorrowrsHealth(AaveV3{chain}.POOL);

        validateBorrowersHealth(healthsBefore, healthsAfter, 1_00);
    }
}
```
### Functions definition

```_testBorrowrsHealth()```

this function get all borrowers health for the given protocol status.

```validateBorrowersHealth(healthsBefore, healthsAfter, changeTolerancePercentage)```

this function compares the health of the borrowed before and after the execution for a given tolerance percentage (1_00 present +-1%, for zero tolerance pass 0)

## Usage MakeFile
add to MakeFile:
```
test-name :; python lib/chaos-labs-utils/scripts/fetch-borrowers.py {chain_name} {block_number} && forge test -vvv --match-contract YourPayloadTest
```

example:
```
test-name :; python lib/chaos-labs-utils/scripts/fetch-borrowers.py ethreum && forge test -vvv --match-contract AaveEthV3PayloadTest
```

lib/chaos-labs-utils/scripts/fetch-borrowers.py script argumansts:
* chain_name - The name of the chain from this supported list: ```[polygon, avalanche, arbitrum, optimism, ethereum]```
* block_number - this is an optional argument, if not pass the script withh fetch the borrowers from the latest block in the graph.


## Acknowledgments

### FQA





# Intro

# How to use 

## Python script
run: ```py3 fetch-borrowers.py {chain_name} {block_number?}```

* chain_name - The name of the chain from this supported list: ```[polygon, avalanche, arbitrum, optimism, ethereum]```

* block_number - this is an optional, if not pass the borrowers from the latest block will be fetched.



## Solidiy test contract

### Functions definition

```_testBorrowrsHealth()```

this function get all borrowers health for the given protocol status.

```validateBorrowersHealth(healthsBefore, healthsAfter, changeTolerancePercentage)```

this function compares the health of the borrowed before and after the execution for a given tolerance percentage (1_00 present +-1%, for zero tolerance pass 0)


### Usage example
```
    import {SanityChecks} from 'chaos-labs-utils/SanityChecks.sol';
    ...

    contract XXXTest is SanityChecks {

      function testPayload() public {
        uint256[] memory healthsBefore = _testBorrowrsHealth(AaveV3{chain}.POOL);

        // 2. execute payload
        _executePayload(address(proposalPayload));

        uint256[] memory healthsAfter = _testBorrowrsHealth(AaveV3{chain}.POOL);

        validateBorrowersHealth(healthsBefore, healthsAfter, 1_00);
    }
}
```

## MakeFile
add to MakeFile:
```
test-name :; python lib/chaos-labs-utils/scripts/fetch-borrowers.py {chain_name} && forge test -vvv --match-contract XXX_Test
```
