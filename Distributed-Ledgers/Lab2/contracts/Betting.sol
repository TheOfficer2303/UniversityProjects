// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./BoxOracle.sol";

contract Betting {

    struct Player {
        uint8 id;
        string name;
        uint totalBetAmount;
        uint currCoef;
    }
    struct Bet {
        address bettor;
        uint amount;
        uint player_id;
        uint betCoef;
    }

    address private betMaker;
    BoxOracle public oracle;
    uint public minBetAmount;
    uint public maxBetAmount;
    uint256 public totalBetAmount;
    uint public thresholdAmount;
    uint public winningAmount;
    uint public actualClaimedWins;

    Bet[] private bets;
    Player public player_1;
    Player public player_2;

    bool private suspended = false;
    mapping (address => uint) public balances;

    constructor(
        address _betMaker,
        string memory _player_1,
        string memory _player_2,
        uint _minBetAmount,
        uint _maxBetAmount,
        uint _thresholdAmount,
        BoxOracle _oracle
    ) {
        betMaker = (_betMaker == address(0) ? msg.sender : _betMaker);
        player_1 = Player(1, _player_1, 0, 200);
        player_2 = Player(2, _player_2, 0, 200);
        minBetAmount = _minBetAmount;
        maxBetAmount = _maxBetAmount;
        thresholdAmount = _thresholdAmount;
        oracle = _oracle;

        totalBetAmount = 0;
    }

    receive() external payable {}

    fallback() external payable {}

    function makeBet(uint8 _playerId) public payable {
        require(!suspended);
        require(oracle.getWinner() != 1 && oracle.getWinner() != 2);
        require(msg.sender != betMaker);
        require(msg.value >= minBetAmount && msg.value <= maxBetAmount);
        require(_playerId == 1 || _playerId == 2);

        uint _playerBetCoef;

        if (_playerId == 1) {
            _playerBetCoef = player_1.currCoef;
            player_1.totalBetAmount += msg.value;
        } else {
            _playerBetCoef = player_2.currCoef;
            player_2.totalBetAmount += msg.value;
        }

        bets.push(
            Bet({
                bettor: msg.sender,
                amount: msg.value,
                player_id: _playerId,
                betCoef: _playerBetCoef
            })
        );

        balances[msg.sender] += msg.value;
        totalBetAmount += msg.value;

        // korigiranje koeficijenata
        if (totalBetAmount > thresholdAmount) {
            if (totalBetAmount == player_1.totalBetAmount || totalBetAmount == player_2.totalBetAmount) {
                suspended = true;
            }

            if (player_1.totalBetAmount > 0) {
                player_1.currCoef = 100 * totalBetAmount / player_1.totalBetAmount;
            }

            if (player_2.totalBetAmount > 0) {
                player_2.currCoef = 100 * totalBetAmount / player_2.totalBetAmount;
            }
        }
    }

    function claimSuspendedBets() public {
        require(suspended);

        uint winnings = 0;
        for (uint i = 0; i < bets.length; i++) {
            if (msg.sender == bets[i].bettor) {
                winnings += bets[i].amount;
            }
        }

        payable(msg.sender).transfer(winnings);
        balances[msg.sender] = 0;

    }

    function claimWinningBets() public {
        require(!suspended);
        require(oracle.getWinner() == 1 || oracle.getWinner() == 2);
        require(balances[msg.sender] > 0);

        uint winnings = 0;
        for (uint i = 0; i < bets.length; i++) {
            if (msg.sender == bets[i].bettor && bets[i].player_id == oracle.getWinner()) {
                winnings += bets[i].amount * bets[i].betCoef / 100;
                actualClaimedWins += 1;
            }
        }

        payable(msg.sender).transfer(winnings);
        balances[msg.sender] = 0;
    }

    function claimLosingBets() public {
        require(oracle.getWinner() == 1 || oracle.getWinner() == 2);
        require(msg.sender == betMaker);

        uint claimedWins = 0;

        for (uint256 i = 0; i < bets.length; i++) {
            if (bets[i].player_id == oracle.getWinner()) {
                claimedWins += 1;
            }
        }

        require(claimedWins == actualClaimedWins);

        payable(msg.sender).transfer(address(this).balance);
    }
}
