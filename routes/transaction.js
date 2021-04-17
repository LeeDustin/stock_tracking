const express = require("express");
const router = express.Router();
const _ = require("lodash")

// Load in models
const Stock = require("../models/Stock");
// const region_helper = require("../../models/helpers/region_helper");

const commission_percentage = 1

// New Entry Page
router.get("/", (req, res) => {
    res.render("transaction", {
      success_msg: `Commission percentage for buying is ${commision_percentage}%`
    });
  });
  
// New Entry Handle
router.post("/", (req, res) => {
  let { stockName, transactionType, origPrice, stockAmount } = req.body;
  let errors = [];

  if (!stockName || !transactionType || !origPrice || !stockAmount) {
    errors.push({ msg: "Please fill in all fields" });
  }
  else{
    if (isNaN(origPrice)){
      errors.push({ msg: "Stock price must be a number" });
    }
    if (isNaN(stockAmount)){
      errors.push({ msg: "Stock amount must be a number" });
    }
    else if (!isInteger(stockAmount)){
      errors.push({ msg: "Stock amount must be an integer" });
    }
  }
  if (errors.length > 0) {
    res.render("transaction", {
      errors,
      stockName,
      origPrice,
      stockAmount
    })
  }
  else {
    origPrice = parseFloat(origPrice)
    stockAmount = parseInt(stockAmount)

    Stock.findOne({ stockName: stockName}).then((stock) => {
      // check if customer with same name from same region exists
      if (!stock) {
          return res.render("transaction", {
            error_msg: `The stock ${stockName} does not exist`,
            stockName,
            origPrice,
            stockAmount
          });
      } 
      let newTransaction = {
        type: transactionType,
        origPrice: origPrice,
        shares: stockAmount
      }
      if (transactionType == "Buy"){
        let price = origPrice*(1+commision_percentage/100)

        newTransaction.price = price
        newTransaction.remainingShares = stockAmount

        stock.totalShares += stockAmount
        stock.balance -= stockAmount * price
      }
      else if (transactionType == "Sell"){
        if (stockAmount < stock.totalShares){
          return res.render("transaction", {
            error_msg: `Your total amount of shares in ${stockName} is less than  ${stockAmount}`,
            stockName,
            origPrice
          });
        }
        newTransaction.price = origPrice
        delete newTransaction.origPrice

        stock.totalShares -= stockAmount
        stock.balance += stockAmount * origPrice
        stock.realized_profit += getRealizedProfit(stock.history, origPrice, stockAmount)
      }
      stock.history.unshift(newTransaction)
      stock
        .save()
        .then(() => {
          req.flash(
            "success_msg",
            `Transaction added to database`
          );
          res.render("transaction");
        })
        .catch((err) => console.log(err));
      })
    }
});

function isInteger(value) {
  return /^\d+$/.test(value);
}


function getRealizedProfit (history, price, amount){
  let index = 0;
  let realized_profit = 0;

  while (amount > 0){
    if (history[index].type == "Sell") continue
    if (amount <= history[index].remainingShares){
      history[index].remainingShares -= amount
      realized_profit += (price-history[index].price) * amount
      amount = 0
    }
    else if (amount > history[index].remainingShares){
      history[index].remainingShares = 0
      realized_profit += (price-history[index].price) * history[index].remainingShares
      amount -= history[index].remainingShares
    }
  }
  return realized_profit;
}

module.exports = router