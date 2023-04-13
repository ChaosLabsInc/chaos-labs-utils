// SPDX-License-Identifier: MIT
pragma solidity ^0.8.16;
import "forge-std/console.sol";
import "forge-std/Test.sol";

import {Constants} from "./borrowers.sol";
import {IPool} from "aave-address-book/AaveV3.sol";

import {AaveV3Ethereum, AaveV3EthereumAssets} from "aave-address-book/AaveV3Ethereum.sol";

contract SanityChecks is Test {
    function _testBorrowrsHealth(
        IPool pool
    ) internal returns (uint256[] memory) {
        address[] memory borrowers = new Constants().getBorrowers();
        uint256[] memory healthFactorArr = new uint256[](borrowers.length);

        console.log("Start test number of borrowers: ", borrowers.length);
        for (uint i = 0; i < borrowers.length; i++) {
            (, , , , , uint256 healthFactor) = pool.getUserAccountData(
                borrowers[i]
            );
            console.log(
                "healthFactor: %s of borrower %s",
                healthFactor,
                borrowers[i]
            );
            healthFactorArr[i] = healthFactor;
        }
        return healthFactorArr;
    }

    function validateBorrowersHealth(
        uint256[] memory countBefore,
        uint256[] memory countAfter,
        uint256 changeTolerancePercentage
    ) internal view {
        for (uint i = 0; i < countBefore.length; i++) {
            if (countBefore[i] == UINT256_MAX && countAfter[i] == UINT256_MAX) {
                continue;
            }
            require(
                (countBefore[i] * (100_00 + changeTolerancePercentage) >=
                    countAfter[i] * 100_00 &&
                    countBefore[i] * (100_00 - changeTolerancePercentage) <=
                    countAfter[i] * 100_00),
                "Health factor chagned more than the set tolerance percentage"
            );
        }
    }
}
