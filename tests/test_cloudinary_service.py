import unittest
from unittest.mock import patch, Mock
from app.cloudinary_service import upload_image

class TestCloudinaryService(unittest.TestCase):

    @patch("app.cloudinary_service.cloudinary.uploader.upload")
    def test_upload_image(self, mock_upload):
        mock_upload.return_value = {"url": "http://example.com/image.jpg"}
        file = Mock()
        result = upload_image(file)
        self.assertEqual(result, "http://example.com/image.jpg")
        mock_upload.assert_called_once_with(file)

if __name__ == "__main__":
    unittest.main()
    