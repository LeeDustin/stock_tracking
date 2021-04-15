const express = require("express");
const router = express.Router();

// Load in models
const Stock = require("../models/Stock");
// const region_helper = require("../../models/helpers/region_helper");


// New Entry Page
router.get("/", (req, res) => {
    res.render("newEntry");
  });
  
// New Entry Handle
router.post("/", (req, res) => {
  const { stock } = req.body;

  if (!stock) {
    res.render("newEntry", {
        error_msg: "Please enter stock name"
      });
  } 
  else {
    Stock.findOne({ stockName: stock}).then((_stock) => {
        // check if customer with same name from same region exists
        if (_stock) {
            res.render("newEntry", {
            error_msg: `The stock ${stock} already exists`
            });
        } else {
            const newStock = new Stock({
                stockName: stock,
                data:{history:[]}
              });
              newStock
                .save()
                .then((_stock) => {
                  req.flash(
                    "success_msg",
                    `stock ${_stock.stockName} added to database, please add in transaction data`
                  );
                  res.redirect("/");
                })
                .catch((err) => console.log(err));
        }
        })
    }
});

module.exports = router