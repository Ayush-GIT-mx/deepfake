require('dotenv').config();
const express = require('express');
const loadExpress = require('./loaders/express');

function createApp() {
  const app = express();
  loadExpress(app);
  return app;
}

module.exports = createApp;
