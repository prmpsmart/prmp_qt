import base64, math
import PySide6
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from typing_extensions import *
from typing import *
from .qss import PrmpWindowQss

WINDOW_TITLE_BAR_HEIGHT = 31


class Expandable:
    def __init__(
        self: QWidget,
        max_width: int,
        min_width: int = 0,
        easing_curve: QEasingCurve = QEasingCurve.InOutQuart,
    ):
        if max_width < min_width:
            max_width = min_width

        self.min_width = min_width
        self.max_width = max_width

        self.animation_group = QParallelAnimationGroup(self)
        self.__anim_group: list[QPropertyAnimation] = []

        for prop in [b"minimumWidth", b"maximumWidth"]:
            anim = QPropertyAnimation(self, prop)
            anim.setDuration(500)
            anim.setEasingCurve(easing_curve)
            self.animation_group.addAnimation(anim)
            self.__anim_group.append(anim)

        self.expanded = False
        self.setMinimumWidth(min_width)
        self.setMaximumWidth(min_width)

    def _anim_group(self):
        return self.__anim_group

    def toggle(self: Union["Expandable", QWidget]):
        for anim in self.__anim_group:
            anim.setStartValue(self.max_width if self.expanded else self.min_width)
            anim.setEndValue(self.min_width if self.expanded else self.max_width)
        self.animation_group.start()
        self.expanded = not self.expanded


class Icon:
    def __init__(self: QWidget, icon_size: int, border=True, color_str: str = "black"):
        self.icon_size = icon_size

        self.setStyleSheet(
            f"""
            border: {int(border)}px solid {color_str};
            min-height: {icon_size}px;
            max-height: {icon_size}px;
            min-width: {icon_size}px;
            max-width: {icon_size}px;
            border-radius: {icon_size/2}px;
            border-radius: 5px;
            padding: 2px;
            """
        )


_QApplication = QApplication


class QApplication(_QApplication):
    def __init__(self, args: list = []):
        super().__init__(args)
        self.setStyleSheet(PrmpWindowQss)

    def add_style_sheet(self, qss: str):
        self.setStyleSheet(PrmpWindowQss + qss)


class QFlowLayout(QLayout):
    def __init__(self, parent=None, margin=0, spacing=-1):
        super().__init__(parent)

        if parent is not None:
            self.setContentsMargins(margin, margin, margin, margin)

        self.setSpacing(spacing)

        self._items = []
        self.__pending_positions = {}

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, a0: QLayoutItem) -> None:
        try:
            position = self.__pending_positions[a0.widget()]
            self._items.insert(position, a0)
            del self.__pending_positions[a0.widget()]
        except KeyError:
            self._items.append(a0)

    def addWidget(self, w: QWidget, position: int = None) -> None:
        if position:
            self.__pending_positions[w] = position
        super().addWidget(w)

    def count(self):
        return len(self._items)

    def expandingDirections(self):
        return Qt.Orientations(Qt.Orientation(0))

    def itemAt(self, index: int) -> QLayoutItem:
        if 0 <= index < len(self._items):
            return self._items[index]

        return None

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self._doLayout(QRect(0, 0, width, 0), True)
        return height

    def minimumSize(self):
        size = QSize()

        for item in self._items:
            size = size.expandedTo(item.minimumSize())

        margin, _, _, _ = self.getContentsMargins()

        size += QSize(2 * margin, 2 * margin)
        return size

    def removeItem(self, a0: QLayoutItem) -> None:
        a0.widget().deleteLater()

    def removeWidget(self, w: QWidget) -> None:
        w.deleteLater()

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self._doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def takeAt(self, index: int) -> QLayoutItem:
        if 0 <= index < len(self._items):
            return self._items.pop(index)

        return None

    def _doLayout(self, rect, testOnly):
        """This does the layout. Dont ask me how. Source: https://github.com/baoboa/pyqt5/blob/master/examples/layouts/flowlayout.py"""
        x = rect.x()
        y = rect.y()
        line_height = 0

        for item in self._items:
            wid = item.widget()
            space_x = self.spacing() + wid.style().layoutSpacing(
                QSizePolicy.PushButton,
                QSizePolicy.PushButton,
                Qt.Horizontal,
            )
            space_y = self.spacing() + wid.style().layoutSpacing(
                QSizePolicy.PushButton,
                QSizePolicy.PushButton,
                Qt.Vertical,
            )
            next_x = x + item.sizeHint().width() + space_x
            if next_x - space_x > rect.right() and line_height > 0:
                x = rect.x()
                y = y + line_height + space_y
                next_x = x + item.sizeHint().width() + space_x
                line_height = 0

            if not testOnly:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = next_x
            line_height = max(line_height, item.sizeHint().height())

        return y + line_height - rect.y()


def addShadow(
    self: QWidget,
    shadowColor: Union[QColor, Qt.GlobalColor] = Qt.black,
    shadow_offset=1,
    shadow_radius=5,
) -> None:
    effect = QGraphicsDropShadowEffect(self)
    effect.setBlurRadius(shadow_radius)
    effect.setColor(shadowColor)
    effect.setOffset(shadow_offset)
    self.setGraphicsEffect(effect)


def removeShadow(self: QWidget) -> None:
    self.setGraphicsEffect(None)


class Shadow:
    def __init__(*args, **kwargs):
        addShadow(*args, **kwargs)


def B64_ENCODE(data: Union[str, bytes]) -> str:
    data = data.encode() if isinstance(data, str) else data
    encoded = base64.b64encode(data)
    str_decoded = encoded.decode()
    return str_decoded


def B64_DECODE(str_decoded: Union[str, bytes]) -> bytes:
    str_encoded = str_decoded.encode() if isinstance(str_decoded, str) else str_decoded
    data = base64.b64decode(str_encoded)
    return data


def B64_DECODE_TO_STRING(str_decoded: Union[str, bytes]) -> str:
    return B64_DECODE(str_decoded).decode()


def MASK_IMAGE(image: QImage, size=128) -> QImage:
    image = image.convertToFormat(QImage.Format_ARGB32)

    imgsize = min(image.width(), image.height())
    rect = QRect(
        (image.width() - imgsize) / 2, (image.height() - imgsize) / 2, imgsize, imgsize
    )
    image = image.copy(rect)

    out_img = QImage(imgsize, imgsize, QImage.Format_ARGB32)
    out_img.fill(Qt.transparent)

    brush = QBrush(image)

    painter = QPainter(out_img)
    painter.setBrush(brush)
    painter.setPen(Qt.NoPen)
    painter.setRenderHint(QPainter.Antialiasing, True)
    painter.drawEllipse(0, 0, imgsize, imgsize)
    painter.end()

    _image = out_img.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    _image.setDevicePixelRatio(QWindow().devicePixelRatio())

    return _image


class RoundedPolygon(QPolygon):
    def __init__(self, radius: int):
        super().__init__()

        self.radius = radius

    def distance(self, p1: QPoint, p2: QPoint):
        d = (p1.x() - p2.x()) ** 2 + (p1.y() - p2.y()) ** 2
        return math.sqrt(d)

    def line(self, i: int):
        pt = QPointF()
        pt1 = self.at(i)
        pt2 = self.at((i + 1) % self.count())
        d = self.distance(pt1, pt2)
        if not d:
            d = 1
        rat = self.radius / d
        if rat > 0.5:
            rat = 0.5
        return pt, pt1, pt2, rat

    def line_start(self, i: int) -> QPointF:
        pt, pt1, pt2, rat = self.line(i)
        pt.setX((1.0 - rat) * pt1.x() + rat * pt2.x())
        pt.setY((1.0 - rat) * pt1.y() + rat * pt2.y())
        return pt

    def line_end(self, i: int) -> QPointF:
        pt, pt1, pt2, rat = self.line(i)
        pt.setX(rat * pt1.x() + (1.0 - rat) * pt2.x())
        pt.setY(rat * pt1.y() + (1.0 - rat) * pt2.y())
        return pt

    def path(self):
        path = QPainterPath()
        pt1 = QPointF()
        pt2 = QPointF()
        for i in range(self.count()):
            pt1 = self.line_start(i)
            if i == 0:
                path.moveTo(pt1)
            else:
                path.quadTo(self.at(i), pt1)
            pt2 = self.line_end(i)
            path.lineTo(pt2)
        pt1 = self.line_start(0)
        path.quadTo(self.at(0), pt1)
        return path

    @classmethod
    def get_path(cls, radius: int, rect: Union[QRect, QRectF]):
        point = lambda p: p.toPoint() if isinstance(p, QPointF) else p

        poly = cls(radius)
        (
            poly
            << point(rect.topLeft())
            << point(rect.topRight())
            << point(rect.bottomRight())
            << point(rect.bottomLeft())
        )
        return poly.path()


def ROUND_IMAGE(image: Union[QImage, str], radius: int, rect: QRectF) -> QImage:
    image = QImage(image)

    out_img = QImage(*image.size().toTuple(), QImage.Format_ARGB32)
    out_img.fill(Qt.transparent)

    painter = QPainter(out_img)
    painter.setBrush(QBrush(image))
    painter.drawPath(RoundedPolygon.get_path(radius, rect))
    painter.end()

    return out_img


def IMAGE(
    image_data: Union[str, int],
    image: str,
    mask=0,
    scale: QSize = None,
    round: int = 0,
    rect: QRect = None,
) -> QPixmap:
    _image = None

    if image_data:
        image_data = (
            B64_DECODE(image_data) if isinstance(image_data, str) else image_data
        )
        _image = QImage.fromData(image_data, "PNG") or QImage.fromData(
            image_data, "JPEG"
        )

    else:
        _image = QImage(image)

    if scale:
        _image = _image.scaled(scale, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    if round and rect:
        _image = ROUND_IMAGE(_image, round, rect)

    if mask:
        _image = MASK_IMAGE(_image, mask)

    return _image


def PIXMAP(*args, **kwargs) -> QPixmap:
    image = IMAGE(*args, **kwargs)
    return QPixmap(image)


def ROUND_PIXMAP(*args, **kwargs) -> QPixmap:
    image = ROUND_IMAGE(*args, **kwargs)
    return QPixmap(image)


def ICON(*args, **kwargs) -> QIcon:
    pixmap = PIXMAP(*args, **kwargs)
    return QIcon(pixmap)


def ROUND_ICON(*args, **kwargs) -> QIcon:
    pixmap = ROUND_PIXMAP(*args, **kwargs)
    return QIcon(pixmap)


def IMAGE_DATA(image: QImage) -> bytes:
    buffer = QBuffer()
    image.save(buffer, "PNG")
    data = buffer.data().data()
    return data


def PIXMAP_DATA(pixmap: QPixmap) -> bytes:
    return IMAGE_DATA(pixmap.toImage())


def ICON_DATA(icon: QIcon, size: QSize) -> bytes:
    return PIXMAP_DATA(icon.pixmap(size))


def MOVE_TO_CURSOR(
    widget: QWidget,
    x: bool = False,
    y: bool = False,
    cx: bool = False,
    cy: bool = False,
    rx: bool = False,
    ty: bool = False,
    lx: bool = False,
    by: bool = False,
):
    pos = QCursor.pos()
    w, h = widget.size().toTuple()
    if x:
        if cx:
            w /= 2
        elif rx:
            w = -w
        elif lx:
            ...
        pos -= QPoint(w, 0)
    if y:
        if cy:
            h /= 2
        elif ty:
            ...
        elif by:
            h = -h
        pos -= QPoint(0, h)

    widget.move(pos)
    widget.show()
