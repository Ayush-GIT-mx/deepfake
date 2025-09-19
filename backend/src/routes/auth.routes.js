const express = require('express');
const router = express.Router();
const controller = require('../controller/auth.controller');
const { signupValidate, loginValidate } = require('../validators/auth.validator');

router.post('/signup', signupValidate, controller.signUp);
router.post('/login', loginValidate, controller.login);
router.get('/user/:id', controller.getUser);

module.exports = router;
