// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./Timer.sol";

/// This contract represents most simple crowdfunding campaign.
/// This contract does not protects investors from not receiving goods
/// they were promised from crowdfunding owner. This kind of contract
/// might be suitable for campaigns that does not promise anything to the
/// investors except that they will start working on some project.
/// (e.g. almost all blockchain spinoffs.)
contract Crowdfunding {

    address private owner;

    Timer private timer;

    uint256 public goal;

    uint256 public endTimestamp;

    mapping (address => uint256) public investments;

    constructor(
        address _owner,
        Timer _timer,
        uint256 _goal,
        uint256 _endTimestamp
    ) {
        owner = (_owner == address(0) ? msg.sender : _owner);
        timer = _timer; // Not checking if this is correctly injected.
        goal = _goal;
        endTimestamp = _endTimestamp;
    }

    function invest() public payable {
        require(timer.getTime() < endTimestamp);
        investments[msg.sender] += msg.value;
    }

    function claimFunds() public {
        uint contractBalance = address(this).balance;
        require(msg.sender == owner);
        require(timer.getTime() >= endTimestamp && contractBalance >= goal);
        payable(owner).transfer(contractBalance);
    }

    function refund() public {
        uint contractBalance = address(this).balance;
        require(timer.getTime() >= endTimestamp && contractBalance < goal);
        payable(msg.sender).transfer(investments[address(msg.sender)]);
    }

}
