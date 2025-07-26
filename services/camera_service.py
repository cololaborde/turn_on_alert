from cv2 import VideoCapture, imwrite
from services.os_service import OSService


class CameraService:

    def __init__(self, photo_name=None):
        os_service = OSService()
        os_service.set_environ("OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS", "0")
        self.photo_name = photo_name or os_service.get_environ("photo_name") or "photo.jpg"
        self.capture = VideoCapture(0)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """ Release the camera and remove the photo file if it exists """
        self.capture.release()
        from os import remove, path
        if path.exists(self.photo_name):
            remove(self.photo_name)

    def take_photo(self):
        """ try to take a photo using default cam """

        if not self.capture or not self.capture.isOpened():
            return None

        ret, frame = self.capture.read()

        if not ret:
            return None

        imwrite(self.photo_name, frame)
        photo = open(self.photo_name, 'rb')
        return photo
