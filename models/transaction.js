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
  origPrice: {
    type: Number,
    required: false,
  },
  price: {
    type: Number,
    required: true,
  },
  shares: {
    type: Number,
    required: true,
  },
  remainingShares: {
    type: Number,
    required: false,
  }
});

module.exports = transactionSchema;
