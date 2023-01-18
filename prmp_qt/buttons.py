from .svgs import QSvgIcon, SvgCompositions
from .commons import *


class Button(QPushButton):
    clicked: SignalInstance
    toggled: SignalInstance(bool)

    def __init__(
        self,
        text: str = "",
        icon: Union[QIcon, str] = None,
        icon_size: int = 0,
        objectName: str = "",
        iconColor: QColor = Qt.black,
        composition: SvgCompositions = SvgCompositions.SourceIn,
        direction: Qt.LayoutDirection = Qt.LeftToRight,
        clickable: bool = True,
        togglable: bool = False,
    ):
        super().__init__()

        self.iconColor = iconColor
        if text:
            self.setText(text)
        if icon:
            self.setIcon(icon, iconColor, composition)
        if icon_size:
            self.setIconSize(QSize(icon_size, icon_size))
        if clickable:
            self.setCursor(Qt.PointingHandCursor)
        if objectName:
            self.setObjectName(objectName)
        self.setLayoutDirection(direction)
        self.setCheckable(togglable)

    def setIcon(
        self,
        icon: Union[QIcon, str],
        iconColor: QColor = None,
        composition: SvgCompositions = SvgCompositions.SourceIn,
    ):
        if not isinstance(icon, QIcon):
            icon = QSvgIcon(
                icon,
                color=iconColor or self.iconColor,
                composition=composition,
            )
        super().setIcon(icon)

    def setIconColor(
        self,
        iconColor: QColor,
        composition: SvgCompositions = SvgCompositions.SourceIn,
    ):
        icon = QSvgIcon(
            self.icon(),
            size=self.iconSize(),
            color=iconColor,
            composition=composition,
        )
        super().setIcon(icon)


class TextButton(Button):
    ...


class LinkButton(Button):
    ...


class LinkIconButton(LinkButton):
    ...


class IconButton(Button, Icon):
    def __init__(
        self,
        icon: str,
        icon_size: int,
        parent: QWidget = None,
        border=True,
        objectName: str = "",
        color: QColor = Qt.black,
        clickable: bool = True,
    ):
        Button.__init__(
            self,
            parent,
            icon=icon,
            icon_size=icon_size,
            objectName=objectName,
            iconColor=color,
            clickable=clickable,
        )
        Icon.__init__(self, icon_size, border=border)


class IconTextButton(Button):
    ...


class RaisedIconTextButton(IconTextButton):
    ...


class Switch(QAbstractButton):
    def __init__(
        self,
        parent=None,
        track_radius=10,
        thumb_radius=8,
        thumb_offset=4,
        useOffset=True,
        text_margin=4,
    ):
        super().__init__(parent=parent)
        self.setCheckable(True)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.text_margin = text_margin
        self._track_radius = track_radius
        self._thumb_radius = thumb_radius
        self._thumb_offset = thumb_offset
        self._useOffset = useOffset
        self._offset = self._thumb_offset

        palette = self.palette()
        if self._thumb_radius > self._track_radius:
            self._trackColor = {
                True: palette.highlight(),
                False: palette.dark(),
            }
            self._thumbColor = {
                True: palette.highlight(),
                False: palette.light(),
            }
            self._textColor = {
                True: palette.highlightedText().color(),
                False: palette.dark().color(),
            }
            self._thumb_text = {
                True: "",
                False: "",
            }
            self._track_opacity = 0.5
        else:
            self._thumbColor = {
                True: palette.highlightedText(),
                False: palette.light(),
            }
            self._trackColor = {
                True: palette.highlight(),
                False: palette.dark(),
            }
            self._textColor = {
                True: palette.highlight().color(),
                False: palette.dark().color(),
            }
            self._thumb_text = {
                True: "✔",
                False: "✕",
            }
            self._thumb_text = {
                True: "1",
                False: "0",
            }
            self._track_opacity = 1

    @Property(int)
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = value
        self.update()

    @property
    def thumb_radius(self):
        if self._useOffset:
            return self.height() - self._thumb_offset * 2
        else:
            return self._thumb_radius

    @property
    def thumb_y_offset(self):
        if self._useOffset:
            return self._thumb_offset
        else:
            return (self.height() - self._thumb_radius) / 2

    @property
    def next_offset(self):
        if self.isChecked():
            return self.width() - self.thumb_radius - self.thumb_x_offset
        else:
            return self.thumb_x_offset

    @property
    def thumb_x_offset(self):
        if self._useOffset:
            return self._thumb_offset
        else:
            return (self.height() - self._thumb_radius) / 2

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update()

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setPen(Qt.NoPen)
        track_opacity = self._track_opacity
        thumb_opacity = 1.0
        text_opacity = 1.0

        if self.isEnabled():
            track_brush = self._trackColor[self.isChecked()]
            thumb_brush = self._thumbColor[self.isChecked()]
            textColor = self._textColor[self.isChecked()]
        else:
            track_opacity *= 0.8
            track_brush = self.palette().shadow()
            thumb_brush = self.palette().mid()
            textColor = self.palette().shadow().color()

        # drawing the track
        p.setBrush(track_brush)
        p.setOpacity(track_opacity)
        p.drawRoundedRect(
            0,
            0,
            self.width(),
            self.height(),
            self._track_radius,
            self._track_radius,
        )

        # drawing the thumb
        p.setBrush(thumb_brush)
        p.setOpacity(thumb_opacity)
        p.drawEllipse(
            self.offset,
            self.thumb_y_offset,
            self.thumb_radius,
            self.thumb_radius,
        )

        # drawing the thumb
        p.setPen(textColor)
        p.setOpacity(text_opacity)
        font = p.font()
        font.setPixelSize(int(0.8 * self.thumb_radius))
        p.setFont(font)
        p.drawText(
            QRectF(
                self.offset,
                self.thumb_y_offset,
                self.thumb_radius,
                self.thumb_radius,
            ),
            Qt.AlignCenter,
            self._thumb_text[self.isChecked()],
        )

    def mouseReleaseEvent(self, event: QMoveEvent):
        super().mouseReleaseEvent(event)
        if event.button() == Qt.LeftButton:
            anim = QPropertyAnimation(self, b"offset", self)
            anim.setDuration(120)
            anim.setStartValue(self.offset)
            anim.setEndValue(self.next_offset)
            anim.start()

    def enterEvent(self, event: QEnterEvent):
        self.setCursor(Qt.PointingHandCursor)
        super().enterEvent(event)
