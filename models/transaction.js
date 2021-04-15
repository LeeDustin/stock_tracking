const mongoose = require("mongoose");

const transactionSchema = new mongoose.Schema({
  date: {
    type: Date,
    default: Date.now(),
  },
  type: {
    type: String,
    required: true,
  },
  orig_price: {
    type: Number,
    required: true,
  },
  price: {
    type: Number,
    required: true,
  },
  amount: {
    type: Number,
    required: true,
  }
});

module.exports = transactionSchema;
