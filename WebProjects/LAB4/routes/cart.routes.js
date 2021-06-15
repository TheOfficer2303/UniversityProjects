const express = require('express');
const router = express.Router();
const cart = require('../models/CartModel')
const cartSanitizer = require('./helpers/cart-sanitizer');

// Ulančavanje funkcija međuopreme
router.get('/', cartSanitizer, function (req, res, next) {
    //####################### ZADATAK #######################
    res.render("cart", {
        title: "Cart",
        linkActive: 'cart',
        user: req.session.user,
        cart: req.session.cart,
        err: undefined
    })

    //#######################################################
});


router.get('/add/:id', async function (req, res, next) {
    //####################### ZADATAK #######################
    if (req.session.cart === undefined || req.session.cart.invalid === true) {
        req.session.cart = cart.createCart();
    }
    let id = req.params.id;

    await cart.addItemToCart(req.session.cart, id, 1)
    res.redirect("/")

    //#######################################################
});

router.get('/remove/:id', async function (req, res, next) {
    //####################### ZADATAK #######################
    let id = req.params.id;

    if (req.session.cart === undefined || req.session.cart.invalid === true) {
        req.session.cart = cart.createCart();
    }

    
    await cart.removeItemFromCart(req.session.cart, id, 1)
    
    res.redirect("/")

    //#######################################################


});

module.exports = router;