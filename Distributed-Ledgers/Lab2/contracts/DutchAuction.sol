// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./Auction.sol";

contract DutchAuction is Auction {

    uint public initialPrice;
    uint public biddingPeriod;
    uint public priceDecrement;

    uint internal auctionEnd;
    uint internal auctionStart;

    /// Creates the DutchAuction contract.
    ///
    /// @param _sellerAddress Address of the seller.
    /// @param _judgeAddress Address of the judge.
    /// @param _timer Timer reference
    /// @param _initialPrice Start price of dutch auction.
    /// @param _biddingPeriod Number of time units this auction lasts.
    /// @param _priceDecrement Rate at which price is lowered for each time unit
    ///                        following linear decay rule.
    constructor(
        address _sellerAddress,
        address _judgeAddress,
        Timer _timer,
        uint _initialPrice,
        uint _biddingPeriod,
        uint _priceDecrement
    )  Auction(_sellerAddress, _judgeAddress, _timer) {
        initialPrice = _initialPrice;
        biddingPeriod = _biddingPeriod;
        priceDecrement = _priceDecrement;
        auctionStart = time();
        // Here we take light assumption that time is monotone
        auctionEnd = auctionStart + _biddingPeriod;
    }

    event Log(uint timer, uint auctionStart, uint auctionEnd);

    /// In Dutch auction, winner is the first person who bids with
    /// bid that is higher than the current price.
    /// This method should be only called while the auction is active.
    function bid() public payable {
        require(outcome == Outcome.NOT_FINISHED);
        require(time() < auctionEnd);

        uint currentPrice = initialPrice - priceDecrement * (time() - auctionStart);

        if (msg.value < currentPrice) {
            payable(msg.sender).transfer(msg.value);
            require(msg.value >= currentPrice);
        }

        if (msg.value > currentPrice) {
            payable(msg.sender).transfer(msg.value - currentPrice);
        }

        outcome = Outcome.SUCCESSFUL;
        highestBidderAddress = msg.sender;
        finalize();
    }

    function enableRefunds() public {
        outcome = Outcome.NOT_SUCCESSFUL;
    }
}
