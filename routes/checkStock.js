const express = require("express");
const router = express.Router();
const _ = require("lodash")

// Load in models
const Stock = require("../models/Stock");

// New Entry Page
router.get("/", (req, res) => {
    res.render("checkStock");
});

commission_percentage = 1

// New Entry Handle
router.post("/", async (req, res) => {
    let { stockName } = req.body;

    if (!stockName) {
        return res.render("checkStock", {
            error_msg: "Please fill in stock name"
        })
    }

    Stock.findOne({ stockName: stockName }).then(async (stock) => {
        // check if customer with same name from same region exists
        if (!stock) {
            return res.render("checkStock", {
                error_msg: `The stock ${stockName} does not exist`,
            });
        }

        let stockHistory = {
            stockName: stockName,
            stockHistory: stock.history
        }
        res.render("results", { stockHistory })
    });
});

module.exports = router