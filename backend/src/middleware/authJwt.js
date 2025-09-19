const jwt = require('jsonwebtoken');
const ApiError = require('../utils/ApiError');

const JWT_SECRET = process.env.JWT_SECRET;
if (!JWT_SECRET) throw new Error('JWT_SECRET is not defined');

module.exports = function (req, res, next) {
  const authHeader = req.headers['authorization'] || req.headers['Authorization'];
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return next(new ApiError(401, 'No Token Provided'));
  }

  const token = authHeader.split(' ')[1]; // fixed split
  try {
    const payload = jwt.verify(token, JWT_SECRET);
    req.user = { id: payload.sub, email: payload.email };
    next();
  } catch (error) {
    next(new ApiError(401, 'Invalid or Expired Token'));
  }
};
