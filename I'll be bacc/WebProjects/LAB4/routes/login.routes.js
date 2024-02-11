const express = require('express');
const { fetchByUsername } = require('../models/UserModel');
const router = express.Router();
const User = require('../models/UserModel');
const { use } = require('./logout.routes');


router.get('/', function (req, res, next) {
    let temporaryError = req.session.err
    req.session.err = undefined
    res.render('login', {
        title: 'Login',
        linkActive: 'login',
        user: req.session.user,
        err: temporaryError
    });
});

router.post('/', async function (req, res, next) {
    //####################### ZADATAK #######################
    let username = req.body.username;

    let user = await User.fetchByUsername(username);

    if (!user.isPersisted() || !user.checkPassword(req.body.password)) {
        let error = "Invalid username or password"
        res.render('login', {
            title: 'Login',
            linkActive: 'login',
            user: req.session.user,
            err: error
        });
    } else {
        req.session.user = user;
        res.redirect("./")
    }
    //#######################################################

});


module.exports = router;