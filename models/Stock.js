const mongoose = require("mongoose");
const transactionSchema = require("./transaction");

const stockSchema = new mongoose.Schema({
  stockName: {
    type: String,
    required: true,
  },
  createDate: {
    type: Date,
    default: Date.now(),
  },
  totalShares:{
    type: Number,
    required: true,
  },
  balance:{
    type: Number,
    required: true,
  },
  realizedProfit:{
    type: Number,
    required: true,
  },
  history: {
    type: [transactionSchema],
    require: true,
  },
});

const Stock = mongoose.model("Stock", stockSchema, "stocks");

module.exports = Stock;
