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

        console.log("Start fetch healt factor for the number of borrowers: ", borrowers.length);
        for (uint i = 0; i < borrowers.length; i++) {
            (, , , , , uint256 healthFactor) = pool.getUserAccountData(
                borrowers[i]
            );
            healthFactorArr[i] = healthFactor;
        }
        return healthFactorArr;
    }

    function validateBorrowersHealth(
        uint256[] memory healthBefore,
        uint256[] memory healthAfter,
        uint256 changeTolerancePercentage
    ) internal view {
        unit256 factor = 100_00;
        for (uint i = 0; i < healthBefore.length; i++) {
            if (healthBefore[i] == UINT256_MAX && healthAfter[i] == UINT256_MAX) {
                continue;
            }
            require(
                (healthBefore[i] * (factor + changeTolerancePercentage) >=
                    healthAfter[i] * factor &&
                    healthBefore[i] * (factor - changeTolerancePercentage) <=
                    healthAfter[i] * factor),
                "Health factor changed more than the set tolerance percentage"
            );
            console.log("Finished validating health factor for the number of borrowers: ",healthBefore.length);
        }
    }
}
