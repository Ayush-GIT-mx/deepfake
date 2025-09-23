import { Router } from 'express';
import AuthController from '../controller/AuthController.js'; // ✅ default import
import { signupValidate, loginValidate } from '../validators/AuthValidator.js';

const router = Router();

router.post('/signup', signupValidate, AuthController.signUp);
router.post('/login', loginValidate, AuthController.login);
router.get('/user/:id', AuthController.getUser);

export default router;
