import site

site.addsitedir(r"C:\Users\Administrator\Desktop\GITHUB_PROJECTS\audiowave\audiowave")

try:
    from audiowavelive import *
    AUDIOWAVE = True
except:
    AUDIOWAVE = False


from ..labels import *
from PySide6.QtMultimedia import (
    QMediaDevices,
    QCamera,
    QImageCapture,
    QMediaCaptureSession,
)


class Camera:
    def __init__(
        self,
        receiver: Callable[[QImage], None] = None,
        fps: int = 24,
        cam: int = 0,
        mirror: bool = False,
    ):
        self.receiver = receiver
        self.fps = 0
        self.mirror = mirror

        self.camera_device = QMediaDevices.videoInputs()[cam]
        self.camera = QCamera(self.camera_device)

        self.image_capture = QImageCapture(self.camera)
        self.image_capture.imageCaptured.connect(self.image_captured)
        self.image_capture.errorOccurred.connect(self.capture_error)

        self.capture_session = QMediaCaptureSession()
        self.capture_session.setCamera(self.camera)
        self.capture_session.setImageCapture(self.image_capture)

        self.timer = QTimer()
        self.timer.timeout.connect(self.image_capture.capture)

        self.set_fps(fps)

    def set_fps(self, fps):
        if fps:
            self.fps = 1000 / fps
            self.timer.setInterval(self.fps)

    def image_captured(self, id: int, image: QImage):
        image = image.convertToFormat(QImage.Format_ARGB32)

        if self.mirror:
            image.mirror(1, 0)

        if self.receiver:
            self.receiver(image)

    def start(self):
        self.camera.start()
        self.timer.start()

    def stop(self):
        self.camera.stop()

    def isActive(self):
        return self.camera.isActive()

    def show_status_message(self, message):
        print(message)

    def capture_error(self, id: int, error: QImageCapture.Error, error_string: str):
        self.show_status_message(error_string)
