const express = require('express');
const authHandler = require('./helpers/auth-handler');
const router = express.Router();

router.get('/', authHandler, function (req, res, next) {
    let cardinfo = req.session.cardinfo
  
    if (cardinfo !== undefined) {
        for (let i = 0; i < cardinfo.length; i++) {
            const element = req.session.cardinfo[i];
            
            if (element === undefined) {
                element = "";
            }
    
            cardinfo[i] = element
        }
        
    } else {
         cardinfo = []
        for (let i = 0; i < 4; i++) {
            cardinfo[i] = "";
            
        }
    }

    res.render("card-payment", {
        title: "Payment",
        linkActive: 'cart',
        user: req.session.user,
        cardHolderName: cardinfo[0],
        cardNumber: cardinfo[1],
        cardCCV: cardinfo[2],
        cardExpiration: cardinfo[3]
    })
    
})

router.post('/order', function(req, res, next) {
    if (req.session.cardinfo !== undefined) {
        for (let i = 0; i < req.session.cardinfo.length; i++) {
            req.session.cardinfo[i] = ""
        }
    }
    
    res.redirect('/checkout')
})

router.post('/save', function(req, res, next) {
    let helper = []
    helper[0] = req.body.cardholdername;
    helper[1] = req.body.cardnumber;
    helper[2] = req.body.cardccv;
    helper[3] = req.body.cardexpiration;

    req.session.cardinfo = helper

    res.redirect('/cart')
})

router.post('/reset', function(req, res, next) {
    for (let i = 0; i < req.session.cardinfo.length; i++) {
        req.session.cardinfo[i] = ""
        
    }

    res.redirect('/card-payment')
})

module.exports = router;