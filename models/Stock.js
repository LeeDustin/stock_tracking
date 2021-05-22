const mongoose = require("mongoose");
const transactionSchema = require("./transaction");

const stockSchema = new mongoose.Schema({
  stockName: {
    type: String,
    required: true,
  },
  createDate: {
    type: String,
    default: Date().toLocaleString('en-US', {timeZone: 'Hongkong'}),
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
