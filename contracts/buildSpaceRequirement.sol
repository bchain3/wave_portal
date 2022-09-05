// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "./safeMath.sol";

contract WavePortalBuildSpace {

    using SafeMath for uint;

    address public admin;
    uint public totalWaves = 0;
    uint public seed;

    mapping(address => uint) public waveCount;
    mapping(address => uint) public timePassedSinceWave;

    event waveLog(uint _timeStamp, uint _seed, address indexed _from, string _message);

    struct Wave {
        uint _timeStamp;
        address _from;
        string _message;
    }

    Wave[] public waves;

    // if you make the constructor payable in brownie you can just specify the initial fund in value. The contract will be funded from the balance of the deploying address
    constructor() payable {
        admin = msg.sender;
        seed = (block.timestamp + block.difficulty) % 100;
    }

    function wave(string memory _message) public {

        address payable waver = payable(msg.sender);

        require (timePassedSinceWave[waver] + 15 minutes < block.timestamp, "Wait 15 minutes");
        timePassedSinceWave[waver] = block.timestamp;

        waveCount[admin] = waveCount[admin].add(1);
        totalWaves = totalWaves.add(1);

        waves.push(Wave(block.timestamp, msg.sender, _message));

        seed = (seed + block.timestamp + block.difficulty) % 100;

        if (seed < 50) {
            require(address(this).balance >= 1 ether);
            // transfer automatically takes the address of the contract it is written in
            waver.transfer(1 ether);
        }
        
        emit waveLog(block.timestamp, seed, msg.sender, _message);
    }

    // to get the entire array we need to define a custom getter function - default solidity getter function resulting due to marking array public only makes  the values of array accesible not the entire array
    function getWaves() public view returns (Wave[] memory) {
        return waves;
    }

}