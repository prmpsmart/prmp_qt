from enum import Enum
from PySide6.QtSvg import QSvgRenderer
from .commons import *


class SvgCompositions(Enum):
    Overlay = QPainter.CompositionMode_Overlay
    SourceIn = QPainter.CompositionMode_SourceIn
    SourceOut = QPainter.CompositionMode_SourceOut
    SourceAtop = QPainter.CompositionMode_SourceAtop


def QSvgPixmap(
    pixmap: QPixmap = None,
    color: QColor = Qt.black,
    composition: SvgCompositions = SvgCompositions.SourceIn,
) -> QPixmap:
    assert composition in SvgCompositions
    o = pixmap
    if not isinstance(pixmap, QPixmap):
        pixmap = QPixmap(pixmap)

    if pixmap.isNull():
        print(o)

    painter = QPainter(pixmap)
    painter.setCompositionMode(composition.value)
    painter.fillRect(pixmap.rect(), QColor(color))
    painter.end()
    return pixmap


def QSvgIcon(
    icon: str = "",
    size: QSize = None,
    color: QColor = Qt.black,
    composition: SvgCompositions = SvgCompositions.SourceIn,
) -> QIcon:
    if isinstance(icon, QIcon):
        icon = icon.pixmap(size)

    pixmap = QSvgPixmap(pixmap=icon, color=color, composition=composition)
    return QIcon(pixmap)
