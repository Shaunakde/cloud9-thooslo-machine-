var express = require('express');
var router = express.Router();

var passport = require('passport');
var Account = require('../models/account.js');

/* GET home page. */
router.get('/', function(req, res) {
   res.render('index');
});

router.get('/register', function(req, res) {
    res.render('register', { });
});

router.post('/register', function(req, res) {
    Account.register(new Account({ username : req.body.email }), req.body.password, function(err, account) {
        if (err) {
            return res.render('register', { account : account });
        }

        passport.authenticate('local-signup')(req, res, function () {
            res.redirect('/');
        });
    });
});

router.get('/login', function(req, res) {
    res.render('login', { user : req.user, message: req.flash('message') });
});

//router.post('/login', passport.authenticate('local-login'), function(req, res) {
//    res.redirect('/');
//});

// process the login form
router.post('/login', passport.authenticate('local-login', {
    successRedirect : '/', // redirect to the secure profile section
    failureRedirect : '/login', // redirect back to the signup page if there is an error
    failureFlash : true // allow flash messages
}));

router.get('/logout', function(req, res) {
    req.logout();
    res.redirect('/');
});

/*
router.all('/flash',function(req, res) {
    req.flash('success', 'This is a flash message using the express-flash module.');
    res.redirect(301,'/');
})
*/

router.get('/ping', function(req, res){
    res.status(200).send(req.headers);
});

module.exports = router;
