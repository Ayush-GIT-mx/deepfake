import DocumentService from '../services/DocumentService.js';

class DocumentController {
  static async upload(req, res) {
    try {
      const { userId, username } = req.query; // or req.query if passed via query
      const file = req.file;

      if (!userId || !username) {
        return res
          .status(400)
          .json({ error: 'userId and username are required' });
      }

      const document = await DocumentService.uploadDocument(
        file,
        parseInt(userId),
        username,
      );

      res.status(201).json({
        success: true,
        message: 'Document uploaded successfully',
        data: document,
      });
    } catch (error) {
      console.error('Upload Error:', error.message);
      res.status(500).json({ error: error.message });
    }
  }
}

export default DocumentController;
