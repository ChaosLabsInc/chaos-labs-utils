# How to use 

## Python script
run: ```py3 fetch-borrowers.py {chain_name} {block_number?}```

* chain_name - The name of the chain from this supported list: ```[polygon, avalanche, arbitrum, optimism, ethereum]```

* block_number - this is an optional, if not pass the borrowers from the latest block will be fetched.



## Solidiy test contract

in the solidity test contract:

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

```_testBorrowrsHealth()```

this function get all borrowers health for the given protocol status.

```validateBorrowersHealth(healthsBefore, healthsAfter, changeTolerancePercentage)```

this function compares the health of the borrowed before and after the execution for a given tolerance percentage (1_00 present +-1%, for zero tolerance pass 0)
