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
  const { stockName } = req.body;

  if (!stockName) {
    res.render("newEntry", {
        error_msg: "Please enter stock name"
      });
  } 
  else {
    Stock.findOne({ stockName: stockName}).then((stock) => {
        // check if customer with same name from same region exists
        if (stock) {
            res.render("newEntry", {
            error_msg: `The stock ${stockName} already exists`
            });
        } else {
            const newStock = new Stock({
                stockName: stockName,
                totalShares:0,
                balance:0,
                realizedProfit:0,
                history: []
              });
              newStock
                .save()
                .then((stock) => {
                  req.flash(
                    "success_msg",
                    `stock ${stock.stockName} added to database, please add in transaction data`
                  );
                  res.redirect("/transaction");
                })
                .catch((err) => console.log(err));
        }
        })
    }
});

module.exports = router