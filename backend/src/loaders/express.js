const express = require('express'); // ✅ missing
const helmet = require('helmet');
const cors = require('cors');
const morgan = require('morgan');
const authRoutes = require('../routes/auth.routes');
const errorHandler = require('../middleware/errorHandler');

function loadExpress(app) {
  app.use(express.json());
  app.use(express.urlencoded({ extended: true }));
  app.use(helmet());
  app.use(cors());
  app.use(morgan('dev'));

  // API versioning
  app.use('/api/v1/auth', authRoutes);

  // Health check
  app.get('/health', (req, res) => res.status(200).json({ success: true, message: "Healthy" }));

  // Error handler (last middleware)
  app.use(errorHandler);
}

module.exports = loadExpress;
