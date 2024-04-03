import cv2

class CameraService:

    def __init__(self, photo_name: str):
        self.photo_name = photo_name
        self.capture = cv2.VideoCapture(0)
    
    def __exit__(self):
        self.capture.release()

    def take_photo(self):
        from os import remove
        """ try to take a photo using default cam """

        if not self.capture or not self.capture.isOpened():
            return None

        ret, frame = self.capture.read()

        if not ret:
            return None
        
        cv2.imwrite(self.photo_name, frame)
        photo = open(self.photo_name, 'rb')
        remove(self.photo_name)
        return photo