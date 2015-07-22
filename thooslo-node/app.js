var express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var mongoose = require('mongoose');

var passport = require('passport');
var cookieParser = require('cookie-parser');
var session = require('express-session');
var flash = require('express-flash');
var handlebars = require('express-handlebars')

var Grant = require('grant-express')
  , grant = new Grant(require('./config/grant.json'))



var routes = require('./routes/index');
var users = require('./routes/users');
var dashboard = require('./routes/dashboard');

var app = express();

// Configs
var configDB = require('./config/database.js');

// configuration 
mongoose.connect(configDB.url); // connect to our database



// view engine setup
app.set('views', path.join(__dirname, 'views'));
//app.set('view engine', 'hjs');
var exphbs = require('express-handlebars');
app.engine('.hbs', exphbs({defaultLayout: 'main', extname: '.hbs'}));
app.set('view engine', '.hbs');

// uncomment after placing your favicon in /public
//app.use(favicon(__dirname + '/public/favicon.ico'));
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(require('less-middleware')(path.join(__dirname, 'public')));
app.use(express.static(path.join(__dirname, 'public')));


// User Installed middleware
//Grant
app.use(grant)
app.use(session({
  name: 'grant', secret: 'SOMESECRET',
  saveUninitialized: true, resave: true
}))

//Passport
app.use(session({ secret: 'ilovescotchscotchyscotchscotch' }));
app.use(passport.initialize());
app.use(passport.session()); // persistent login sessions
app.use(flash()); // use connect-flash for flash messages stored in session

require('./config/passport.js')(passport); // pass passport for configuration


// ROUTING ---------------------------------------------------------------------
app.use('/', routes);
app.use('/users', users);
app.use('/dashboard',dashboard)



// catch 404 and forward to error handler
app.use(function(req, res, next) {
  var err = new Error('Not Found');
  err.status = 404;
  next(err);
});

// error handlers

// development error handler
// will print stacktrace
if (app.get('env') === 'development') {
  app.use(function(err, req, res, next) {
    res.status(err.status || 500);
    res.render('error', {
      message: err.message,
      error: err,
      layout:false
    });
  });
}

// production error handler
// no stacktraces leaked to user
app.use(function(err, req, res, next) {
  res.status(err.status || 500);
  res.render('error', {
    message: err.message,
    error: {},
    layout: false
  });
});


module.exports = app;