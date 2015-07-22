var express = require('express');
var request = require('request');
var router = express.Router();

/* GET users listing. */
router.get('/', function(req, res, next) {
  //res.send('respond with a resource');
  
  var options = {
    url: 'https://affiliate-api.flipkart.net/affiliate/offers/v1/top/json',
    headers: {
        'User-Agent': 'ClrFeed',
        'Fk-Affiliate-Id': 'shaunakde1',
        'Fk-Affiliate-Token': '89532f8e94cb4972a49e88025db0aeda'
    }    };
    
    function callback(error, response, body) {
        if (!error && response.statusCode == 200) {
        var info = JSON.parse(body);
        //console.log(body);
        

        s = '';
        for(var i=0;i<info.topOffersList.length;i++){
        
        s += info.topOffersList[i].url
        s += '<br>'
        s += info.topOffersList[i].title
        s += '<br>'
        s += info.topOffersList[i].description
        s += '<br>'
        s += info.topOffersList[i].imageUrls[0].url
        s += '<br>'
        s += info.topOffersList[i].availability
        s += '<br>'
        s += '<hr>'
        
        }
        res.send(s);
    }};
    
    request(options, callback);
  
  
});

module.exports = router;





