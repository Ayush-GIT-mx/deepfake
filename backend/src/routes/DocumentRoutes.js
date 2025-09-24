import { Router } from 'express';
import FileUpload from '../utils/FileUpload.js';
import DocumentController from '../controller/DocumentController.js';

const router = Router();
router.post('/upload', FileUpload.single('file'), DocumentController.upload);

const documentRoutes = router;
export default documentRoutes;
