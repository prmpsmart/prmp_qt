import site

site.addsitedir("../")

from prmp_qt import *


class App(QApplication):
    def __init__(self):
        super().__init__()

        self.setStyleSheet(
            """
            IconTextButton {
                border: none;
                max-width: 30px;
                max-height: 30px;
                border-radius: 30px;
            }
            IconTextButton:hover {
                border: 1px solid black;
            }
            CameraWidget {
                border-radius: 10px;
                background: green;
            }
            """
        )
        self.w = QWidget()
        lay = QVBoxLayout(self.w)
        lay.setSpacing(5)

        self.cam = CameraWidget(
            default=r"C:\Users\Administrator\Desktop\GITHUB_PROJECTS\Amebo\desktop\ui\utils\resources\photo-off.svg",
            output=True,
            radius=10,
        )
        self.cam.setMinimumSize(600, 300)
        lay.addWidget(self.cam, 1)

        cam_but = IconTextButton(
            icon=r"C:\Users\Administrator\Desktop\GITHUB_PROJECTS\Amebo\desktop\ui\utils\resources\camera.svg",
            icon_size=30,
            togglable=1,
        )
        cam_but.toggled.connect(self.toggle)
        lay.addWidget(cam_but, 0, Qt.AlignCenter | Qt.AlignBottom)

        self.w.show()

    def toggle(self, toggle: bool):
        if toggle:
            self.cam.start()
        else:
            self.cam.stop()


a = App()
a.exec()
