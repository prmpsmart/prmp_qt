from .core import *

if AUDIOWAVE:
    from audiolivewaveform import *


class CameraWidget(ImageLabel):
    def __init__(
        self,
        fps: int = 50,
        cam: int = 0,
        start: bool = False,
        output: bool = False,
        receiver: Callable[[QImage], None] = None,
        mirror: bool = True,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.output = output
        self.receiver = receiver

        self.camera = Camera(self.image_captured, fps=fps, cam=cam, mirror=mirror)

        self.image: QImage = None

        if start:
            self.start()

    def image_captured(self, image: QImage):
        image = image.scaled(
            self.size(),
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        self.image = image
        if self.output:

            self.setImage(image=image)

        if self.receiver:
            self.receiver(image)

    def set_fps(self, fps: int):
        if fps:
            self.fps = 1000 / fps

    def start(self):
        self.camera.start()

    def stop(self):
        self.camera.stop()

    def closeEvent(self, event: QCloseEvent):
        if self.camera.isActive():
            self.camera.stop()
        event.accept()
