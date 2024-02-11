// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./Auction.sol";

contract EnglishAuction is Auction {

    uint internal highestBid;
    uint internal initialPrice;
    uint internal biddingPeriod;
    uint internal lastBidTimestamp;
    uint internal minimumPriceIncrement;

    address internal highestBidder;

    constructor(
        address _sellerAddress,
        address _judgeAddress,
        Timer _timer,
        uint _initialPrice,
        uint _biddingPeriod,
        uint _minimumPriceIncrement
    ) Auction(_sellerAddress, _judgeAddress, _timer) {
        initialPrice = _initialPrice;
        biddingPeriod = _biddingPeriod;
        minimumPriceIncrement = _minimumPriceIncrement;

        // Start the auction at contract creation.
        lastBidTimestamp = time();
    }

    function bid() public payable {
        require(outcome == Outcome.NOT_FINISHED);
        require(time() - lastBidTimestamp < biddingPeriod);
        require(msg.value > highestBid && msg.value >= initialPrice);

        if (msg.value < highestBid + minimumPriceIncrement) {
            payable(msg.sender).transfer(msg.value);
            require(msg.value >= highestBid + minimumPriceIncrement);
        }

        //vracam pare prethodniku
        payable(highestBidder).transfer(highestBid);
        highestBid = msg.value;
        highestBidder = msg.sender;
        lastBidTimestamp = time();
    }

    function getHighestBidder() override public returns (address) {
        if ((time() - lastBidTimestamp >= biddingPeriod) && highestBidder != address(0)) {
            return highestBidder;
        }
        return address(0);
    }

    function enableRefunds() public {
        outcome = Outcome.NOT_SUCCESSFUL;
    }

}
