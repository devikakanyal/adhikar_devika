// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FIRSystem {
    struct FIR {
        string name;
        string description;
        string ipfsHash;
        uint timestamp;
    }

    mapping(uint => FIR) public firs;
    uint public firCount;

    function fileFIR(string memory name, string memory description, string memory ipfsHash) public {
        firs[firCount] = FIR(name, description, ipfsHash, block.timestamp);
        firCount++;
    }

    function getFIR(uint id) public view returns (string memory, string memory, string memory, uint) {
        FIR memory f = firs[id];
        return (f.name, f.description, f.ipfsHash, f.timestamp);
    }
}
