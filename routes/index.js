const express = require('express');
const router = express.Router();

// Dashboard
router.get('/', (req, res) => res.render("dashboard"));

// CSS
router.get('/views/css/views.css', (req, res) => {
    var options = {
        headers: {
          'Content-Type': text/css
        }
      }
    res.sendFile('/views/css/views.css', options);
})

// New Entry
router.use('/newEntry', require('./newEntry'))


module.exports = router;