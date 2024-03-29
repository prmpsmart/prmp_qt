from .svgs import QSvgPixmap
from .commons import *


class Label(QLabel):
    def __init__(self, text: str = "", objectName: str = "", parent: QWidget = None):
        super().__init__(text, parent)

        if objectName:
            self.setObjectName(objectName)


class ImageLabel(Label):
    def __init__(
        self,
        pixmap: QPixmap = None,
        image: Union[QImage, str] = None,
        objectName: str = "",
        default: str = "",
        radius: int = 0,
    ):
        super().__init__(objectName=objectName)

        self.radius = radius
        self.default = default
        self.setScaledContents(True)

        if default:
            self.setImage(pixmap, image)

    def setImage(
        self,
        pixmap: QPixmap = None,
        image: Union[QImage, str] = None,
        image_data: str = "",
    ):

        pixmap = PIXMAP(image_data, self.default, round=self.radius)

        if self.radius:
            image = ROUND_IMAGE(image or pixmap.toImage(), self.radius, self.rect())

        if not pixmap:
            pixmap = QPixmap(image)

        self.setPixmap(pixmap)


class IconLabel(Label, Icon):
    def __init__(
        self,
        icon: str,
        icon_size: int,
        parent: QWidget = None,
        border=True,
        objectName: str = "",
        color: Union[Qt.GlobalColor, QColor] = Qt.black,
        **kwargs,
    ):
        Label.__init__(self, parent=parent, objectName=objectName)
        Icon.__init__(self, icon_size, border=border, **kwargs)
        self.setPixmap(QSvgPixmap(icon, color).scaled(self.icon_size, self.icon_size))


class ColorfulTag(Label):
    def __init__(self, text: str = "", objectName=""):
        super().__init__(text=text, objectName=objectName)


class AlignLabel(Label):
    def __init__(self, alignment: Qt.Alignment = Qt.AlignCenter, **kwargs):
        super().__init__(**kwargs)
        self.setAlignment(alignment)


class TextIcon(AlignLabel):
    def __init__(self, text: str, **kwargs):
        super().__init__(text=text, **kwargs)

        self.setAlignment(Qt.AlignCenter)


class LeftAlignLabel(AlignLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, alignment=Qt.AlignLeft, **kwargs)


class RightAlignLabel(AlignLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, alignment=Qt.AlignRight, **kwargs)


class RequiredLabel(QHBoxLayout):
    def __init__(self, text: str):
        super().__init__()
        self.setSpacing(2)
        self.addWidget(Label(text=text, objectName="bold"))
        self.addWidget(Label(text="*", objectName="required"))
        self.addStretch()
