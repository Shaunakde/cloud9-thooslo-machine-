var express = require('express');
var router = express.Router();


/* GET users listing. */
router.get('/', function(req, res, next) {


console.log(req.query)
res.end(JSON.stringify(req.query, null, 2));
  
});

module.exports = router;






