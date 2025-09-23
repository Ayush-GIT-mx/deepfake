import { json, urlencoded } from 'express'; // ✅ missing
import helmet from 'helmet';
import cors from 'cors';
import morgan from 'morgan';
import authRoutes from '../routes/AuthRoutes.js';
import errorHandler from '../middleware/errorHandler.js';

function loadExpress(app) {
  app.use(json());
  app.use(urlencoded({ extended: true }));
  app.use(helmet());
  app.use(cors());
  app.use(morgan('dev'));

  // API versioning
  app.use('/api/v1/auth', authRoutes);

  // Health check
  app.get('/health', (req, res) =>
    res.status(200).json({ success: true, message: 'Healthy' }),
  );

  // Error handler (last middleware)
  app.use(errorHandler);
}

export default loadExpress;
