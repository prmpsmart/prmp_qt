from .commons import *


class Frame(QFrame):
    def __init__(self, objectName: str = "", parent: QWidget = None):
        super().__init__(parent)
        if objectName:
            self.setObjectName(objectName)


class VFrame(Frame):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setLayout(QVBoxLayout())

    def layout(self) -> QVBoxLayout:
        return super().layout()


class HFrame(Frame):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setLayout(QHBoxLayout())

    def layout(self) -> QHBoxLayout:
        return super().layout()


class FFrame(Frame):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setLayout(QFlowLayout())

    def layout(self) -> QFlowLayout:
        return super().layout()


class VLine(Frame):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setFrameShape(self.VLine)


class HLine(Frame):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setFrameShape(self.HLine)


def addHLine(lay, w=0, h=0, objectName=""):
    vlay = QVBoxLayout()
    lay.addLayout(vlay)
    vlay.addWidget(HLine(objectName=objectName))
    vlay.setContentsMargins(w, h, w, h)
