const express = require("express");
const router = express.Router();
const _ = require("lodash")

// Load in models
const Stock = require("../models/Stock");

// New Entry Page
router.get("/", (req, res) => {
    res.render("checkProfit");
});

commission_percentage = 1

// New Entry Handle
router.post("/", async (req, res) => {
    let { stockName, transactionType, origPrice, stockAmount } = req.body;
    let errors = [];

    if (!stockName || !transactionType || !origPrice || !stockAmount) {
        errors.push({ msg: "Please fill in all fields" });
    }
    else {
        if (isNaN(origPrice)) {
            errors.push({ msg: "Stock price must be a number" });
        }
        if (isNaN(stockAmount)) {
            errors.push({ msg: "Stock amount must be a number" });
        }
        else if (!isInteger(stockAmount)) {
            errors.push({ msg: "Stock amount must be an integer" });
        }
    }
    if (errors.length > 0) {
        return res.render("transaction", {
            errors,
            stockName,
            origPrice,
            stockAmount
        })
    }
    origPrice = parseFloat(origPrice)
    stockAmount = parseInt(stockAmount)

    Stock.findOne({ stockName: stockName }).then(async (stock) => {
        // check if customer with same name from same region exists
        if (!stock) {
            return res.render("transaction", {
                error_msg: `The stock ${stockName} does not exist`,
                stockName,
                origPrice,
                stockAmount
            });
        }
        let overallOrigBalance = 0
        let overallOrigRealizedProfit = 0

        await Stock.find({}, function(err, stocks) {        
            stocks.forEach(function(_stock) {
                overallOrigBalance += _stock.balance
                overallOrigRealizedProfit += _stock.realizedProfit
            });
          });

        let origBalance = stock.balance
        let origRealizedProfit = stock.realizedProfit
        let origUnrealizedProfit = getRealizedProfit(stock.history, origPrice, 0, true)


        let newTransaction = {
            type: transactionType,
            origPrice: origPrice,
            shares: stockAmount
        }
        if (transactionType == "Buy") {
            let price = origPrice * (1 + commission_percentage / 100)
            price = price.toFixed(2)

            newTransaction.price = price
            newTransaction.remainingShares = stockAmount

            stock.totalShares += stockAmount
            stock.balance -= stockAmount * price
        }
        else if (transactionType == "Sell") {
            if (stockAmount > stock.totalShares) {
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
            stock.realizedProfit += getRealizedProfit(stock.history, origPrice, stockAmount)
            console.log("realizedProfit:", stock.realizedProfit)
        }
        stock.history.unshift(newTransaction)

        let newBalance = stock.balance
        let newRealizedProfit = stock.realizedProfit
        let newUnrealizedProfit = getRealizedProfit(stock.history, origPrice, 0, true)

        let stockData = {
            stockName,
            origBalance,
            origRealizedProfit,
            origUnrealizedProfit,
            newBalance,
            newRealizedProfit,
            newUnrealizedProfit,
        }

        let overallNewBalance = overallOrigBalance + newBalance - origBalance
        let overallNewRealizedProfit = overallOrigRealizedProfit + newRealizedProfit - origRealizedProfit
        let overallData = {
            overallOrigBalance,
            overallOrigRealizedProfit,
            overallNewBalance,
            overallNewRealizedProfit
        }
        res.render("results", { stockData, overallData })
    });
});

function isInteger(value) {
    return /^\d+$/.test(value);
}


function getRealizedProfit(history, price, amount, unrealized_flag=false) {
    let stock_amount = amount
    let index = history.length -1;
    let realized_profit = 0;
  
    console.log(history.length, price, amount,unrealized_flag)
  
    while ((stock_amount > 0 || unrealized_flag) && index >= 0) {
      if (history[index].type == "Sell" || history[index].remainingShares == 0) {
        index--;
        continue
      }
      if (stock_amount <= history[index].remainingShares) {
          history[index].remainingShares -= stock_amount
          realized_profit += (price - history[index].price) * stock_amount
          stock_amount = 0
      }
      else if (stock_amount > history[index].remainingShares) {
          stock_amount -= history[index].remainingShares
          realized_profit += (price - history[index].price) * history[index].remainingShares
          history[index].remainingShares = 0
      }
      console.log(`turn ${index}, stock_amount: ${stock_amount}, remaining shares: ${history[index].remainingShares}`)
      index--
    }
    return realized_profit.toFixed(2);
  }

module.exports = router