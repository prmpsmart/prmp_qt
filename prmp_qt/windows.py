from turtle import right
from .labels import *
from .frames import VFrame, HFrame


BUTTON_HINTS = [
    Qt.WindowCloseButtonHint,
    Qt.WindowMinimizeButtonHint,
    Qt.WindowMaximizeButtonHint,
]


class _Bar(HFrame):
    def __init__(self, parent: "PrmpWindow"):
        super().__init__(parent=parent)

        self.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed))


class _StatusBar(_Bar):
    def __init__(self, parent: "PrmpWindow"):
        super().__init__(parent)
        self.setObjectName("statusBar")

    def addWidget(self, widget: QWidget):
        self.layout().addWidget(widget)


class _TitleBar(_Bar):
    def __init__(self, window: "PrmpWindow", macStyle=False):
        super().__init__(window.windowFrame())

        self.__mousePressed = False

        # defaults
        self.__window = window

        self.setObjectName("titleBar")

        lay = self.layout()
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        self.lblTitle = Label(text="Title", parent=self)
        self.lblTitle.setObjectName("lblTitle")
        self.lblTitle.setAlignment(Qt.AlignCenter)

        spButtons = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.btnMinimize = QToolButton(self)
        self.btnMinimize.setObjectName("btnMinimize")
        self.btnMinimize.setSizePolicy(spButtons)

        self.btnMaximize = QToolButton(self)
        self.btnMaximize.setObjectName("btnMaximize")
        self.btnMaximize.setSizePolicy(spButtons)

        self.btnClose = QToolButton(self)
        self.btnClose.setObjectName("btnClose")
        self.btnClose.setSizePolicy(spButtons)

        if macStyle:
            lay.addWidget(self.btnClose)
            lay.addWidget(self.btnMaximize)
            lay.addWidget(self.btnMinimize)
            lay.addWidget(self.lblTitle)
        else:
            lay.addWidget(self.lblTitle)
            lay.addWidget(self.btnMinimize)
            lay.addWidget(self.btnMaximize)
            lay.addWidget(self.btnClose)

        QMetaObject.connectSlotsByName(self)

    def setTitle(self, title: str):
        self.lblTitle.setText(title)

    def isMaximized(self) -> bool:
        return self.__window.isMaximized()

    @Slot()
    def on_btnMinimize_clicked(self):
        self.setWindowState(Qt.WindowMinimized)

    @Slot()
    def on_btnMaximize_clicked(self):
        self.setWindowState(
            Qt.WindowNoState if self.isMaximized() else Qt.WindowMaximized
        )

    @Slot()
    def on_btnClose_clicked(self):
        self.__window.close()

    def windowState(self):
        return self.__window.windowState()

    def setWindowState(self, state: Qt.WindowStates):
        return self.__window.setWindowState(state)

    def setWindowButtonState(self, hint: Qt.WindowType, state: bool):
        btns = dict(
            zip(
                BUTTON_HINTS,
                (
                    self.btnClose,
                    self.btnMinimize,
                    self.btnMaximize,
                ),
            )
        )
        button = btns.get(hint)
        button.setEnabled(state)

        allButtons = [
            self.btnClose,
            self.btnMinimize,
            self.btnMaximize,
        ]
        if True in [b.isEnabled() for b in allButtons]:
            for b in allButtons:
                b.setVisible(True)
            self.lblTitle.setContentsMargins(0, 0, 0, 0)
        else:
            for b in allButtons:
                b.setVisible(False)
            self.lblTitle.setContentsMargins(0, 2, 0, 0)

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        self.on_btnMaximize_clicked()

    def mousePressEvent(self, event: QMouseEvent):
        self.__mousePressed = True
        self.__mousePos = event.globalPosition().toPoint()
        self.__windowPos = self.__window.pos()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.__mousePressed:
            if self.isMaximized():
                # restore the window firstly
                self.on_btnMaximize_clicked()
                # move the window back on the mouse
                self.__window.move(
                    self.__mousePos
                    - QPoint(
                        0.5 * self.geometry().width(),
                        0.5 * self.geometry().height(),
                    )
                )
                # refresh __windowPos
                self.__windowPos = self.__window.pos()
            self.__window.move(
                self.__windowPos + (event.globalPosition().toPoint() - self.__mousePos)
            )

    def mouseReleaseEvent(self, _):
        self.__mousePressed = False


class BaseWindow_:

    resized = Signal()
    moved = Signal()

    def moveEvent(self, _: QMoveEvent) -> None:
        self.moved.emit()

    def resizeEvent(self, _: QResizeEvent) -> None:
        self.resized.emit()

    def showEvent(self, _: QShowEvent) -> None:
        self.resized.emit()


class BaseWindow(BaseWindow_, QWidget):
    def __init__(self, parent: QWidget = None):
        QWidget.__init__(self, parent)
        BaseWindow_.__init__(self)


class BaseDialog(BaseWindow, QDialog):
    def __init__(self, parent: QWidget = None):
        QDialog.__init__(self, parent)
        BaseWindow_.__init__(self)


class FrameLessWindow(BaseWindow):
    def __init__(
        self,
        parent: QObject = None,
        shadowColor: Union[QColor, Qt.GlobalColor] = Qt.black,
        shadow_offset=1,
        shadow_radius=5,
        add_shadow=False,
    ):
        BaseWindow.__init__(self, parent)

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)

        m = shadow_offset + 2
        lay = QHBoxLayout(self)
        lay.setContentsMargins(m, m, m, m)

        self.__windowFrame = VFrame(parent=self, name="window_frame")
        lay.addWidget(self.__windowFrame)

        vlayout = self.__windowFrame.layout()
        vlayout.setContentsMargins(m, m, m, m)
        vlayout.setSpacing(0)

        if add_shadow:
            Shadow.__init__(
                self.__windowFrame,
                shadow_radius=shadow_radius,
                shadowColor=shadowColor,
                shadow_offset=shadow_offset,
            )
            lay.setContentsMargins(0, 0, shadow_radius, shadow_radius)

    def windowLayout(self) -> QVBoxLayout:
        return self.__windowFrame.layout()

    def windowFrame(self) -> QWidget:
        return self.__windowFrame

    def height(self):
        return self.__windowFrame.height()


class RoundWindow(FrameLessWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.windowFrame().setObjectName("round_frame")


class RoundDialog(RoundWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def event(self, event: QEvent):
        if event.type() == event.Type.WindowDeactivate:
            self.close()
        return super().event(event)


class PrmpWindow(RoundWindow):
    def __init__(self, *args, titleBarKwargs={}, **kwargs):
        RoundWindow.__init__(self, *args, **kwargs)

        vlayout = self.windowLayout()
        m = 3
        vlayout.setContentsMargins(m, m, m, m)

        # widgets
        self.titleBar = _TitleBar(self, **titleBarKwargs)
        vlayout.addWidget(self.titleBar)

        self.content_layout = QStackedLayout()
        vlayout.addLayout(self.content_layout)

        self.statusBar = _StatusBar(self)
        vlayout.addWidget(self.statusBar)

        # default options
        self.setWindowFlags(
            Qt.Window
            | Qt.FramelessWindowHint
            | Qt.WindowSystemMenuHint
            | Qt.WindowCloseButtonHint
            | Qt.WindowMinimizeButtonHint
            | Qt.WindowMaximizeButtonHint
        )

        self.top_left_grip = QSizeGrip(self)
        self.top_right_grip = QSizeGrip(self)
        self.bottom_left_grip = QSizeGrip(self)
        self.bottom_right_grip = QSizeGrip(self)
        self.left_grip = QSizeGrip(self)
        self.right_grip = QSizeGrip(self)
        self.top_grip = QSizeGrip(self)
        self.bottom_grip = QSizeGrip(self)

        self.grips = [
            self.top_left_grip,
            self.top_right_grip,
            self.bottom_left_grip,
            self.bottom_right_grip,
            self.left_grip,
            self.right_grip,
            self.top_grip,
            self.bottom_grip,
        ]

        h = self.titleBar.height()
        for grip in self.grips:
            grip.hide()
            grip.setMaximumSize(h, h)

    def resizeEvent(self, _: QShowEvent) -> None:
        w, h = self.width(), self.height()
        x2, y2 = w - self.top_right_grip.width(), h - self.bottom_left_grip.height()
        self.top_left_grip.move(0, 0)
        self.top_right_grip.move(x2, 0)
        self.bottom_left_grip.move(0, y2)
        self.bottom_right_grip.move(x2, y2)

        self.right_grip.move(x2, self.right_grip.y())
        self.bottom_grip.move(self.bottom_grip.x(), y2)

    def hide_grips(self):
        for grip in self.grips:
            grip.hide()

    def event(self, event: QEvent):
        type = event.type()

        if type in [event.Enter, event.MouseMove, event.Leave]:
            if type != event.Leave:
                m = self.titleBar.height()
                w, h = self.width(), self.height()
                x, y = event.pos().toTuple()

                self.top_left_grip.setVisible(x < m and y < m)
                self.top_right_grip.setVisible(x > w - m and y < m)
                self.bottom_left_grip.setVisible(x < m and y > h - m)
                self.bottom_right_grip.setVisible(x > w - m and y > h - m)

                left = (x < m) and (m < y < h - m)
                self.left_grip.setVisible(left)
                self.left_grip.move(0, y)

                right = (x > w - m) and (m < y < h - m)
                self.right_grip.setVisible(right)
                self.right_grip.move(w - m, y)

                top = (m < x < w - m) and (y < m)
                self.top_grip.setVisible(top)
                self.top_grip.move(x, y)

                bottom = (m < x < w - m) and (h - m < y)
                self.bottom_grip.setVisible(bottom)
                self.bottom_grip.move(x, h - m)

            else:
                self.hide_grips()

        elif event in [QMouseEvent, QEvent]:
            self.hide_grips()

        return super().event(event)

    def pos(self) -> QPoint:
        pos = super().pos()
        x, y = pos.toTuple()
        margins = self.layout().contentsMargins()
        left = margins.left()
        top = margins.top()

        pos += QPoint(left, top)

        return pos

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        x, y = event.x(), event.y()
        self.top_left_grip.setVisible(x < 100 and y < 100)

        return super().mouseMoveEvent(event)

    def setContentWidget(self, widget: QWidget):
        self.content_layout.addWidget(widget)
        self.content_layout.setCurrentWidget(widget)

    def setWindowTitle(self, title):
        super().setWindowTitle(title)
        self.titleBar.setTitle(title)

    def setWindowFlag(self, windowType: Qt.WindowType, on: bool = True):
        if not hasattr(self, "titleBar"):
            return

        if windowType in BUTTON_HINTS:
            self.titleBar.setWindowButtonState(windowType, on)
        else:
            super().setWindowFlag(windowType, on)

    def setWindowFlags(self, windowFlags: Qt.WindowFlags):
        if not hasattr(self, "titleBar"):
            return

        for hint in BUTTON_HINTS:
            self.titleBar.setWindowButtonState(hint, bool(windowFlags & hint))

        super().setWindowFlags(windowFlags)


class _Drawer(Expandable):
    def __init__(
        self: QWidget,
        window: QWidget,
        *args,
        x: int = 0,
        y: int = 0,
        y_getter: Callable = None,
        height: int = 0,
        height_getter: Callable = None,
        popup_mode: bool = False,
        **kwargs,
    ):
        Expandable.__init__(self, *args, min_width=0, **kwargs)

        self.setMaximumWidth(self.max_width)

        self._window = window
        self._x = x
        self.y_getter = y_getter
        self._y = y
        self._height = height
        self.height_getter = height_getter

        self._window.moved.connect(self.updatePosition)
        self._window.resized.connect(self.updateHeight)

        self.setWindowFlags(
            Qt.FramelessWindowHint
            # | Qt.WindowStaysOnTopHint
            # | Qt.WindowCloseButtonHint
            | [Qt.Drawer, Qt.Popup][popup_mode]
            # | Qt.Dialog
            # | Qt.WindowModal
        )

        self.animation_group.finished.connect(self.finished)
        self.layout().setContentsMargins(0, 0, 5, 0)

    def getY(self: Union["_Drawer", QWidget]):
        y = self.y_getter() if self.y_getter else self._y

        if not bool(self._window.windowFlags() & Qt.FramelessWindowHint):
            y += WINDOW_TITLE_BAR_HEIGHT
        if isinstance(self._window, PrmpWindow):
            if self._window.titleBar.isVisible():
                y += self._window.titleBar.height() + self._window.layout().spacing()

        return y

    def getX(self: Union["_Drawer", QWidget]):
        x = self._x
        if not bool(self._window.windowFlags() & Qt.FramelessWindowHint):
            x += 11
        return x

    def updatePosition(self: Union["_Drawer", QWidget]):
        self.move(self._window.pos() + QPoint(self._x + 1, self.getY()))

    def updateHeight(self: Union["_Drawer", QWidget]):
        if self.height_getter:
            h = self.height_getter()
        else:
            wh = self._window.height()
            if isinstance(self._window, PrmpWindow):
                if self._window.titleBar.isVisible():
                    wh -= (
                        self._window.titleBar.height() + self._window.layout().spacing()
                    )
                if self._window.statusBar.isVisible():
                    wh -= (
                        self._window.statusBar.height()
                        + self._window.layout().spacing() * 2
                    )
            h = self._height or wh

        self.setMinimumHeight(h)
        self.setMaximumHeight(h)
        self.updatePosition()

    def toggle_drawer(self: Union["_Drawer", QWidget]):
        self.finished()

        if self.expanded:
            self.updatePosition()
            self.updateHeight()

        if self.isHidden():
            self.first = 1
            self.updatePosition()
            self.updateHeight()
            QTimer.singleShot(100, self.show)

        self.toggle()

    def finished(self: Union["_Drawer", QWidget]):
        self.animation_group.stop()
        # self.setVisible(self.expanded)
        if self.expanded:
            self.show()
        else:
            self.hide()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.toggle_drawer()
        self.expanded = False

    def closeEvent(self, event: QMouseEvent) -> None:
        self.expanded = False

    def event(self, event: QEvent):
        type = event.type()
        if type == QEvent.Type.WindowDeactivate:
            # self.close()
            ...

        elif type in [QEvent.Type.Hide, QEvent.Type.HideToParent]:
            self.close()

        return super().event(event)


class DrawerWindow(_Drawer, FrameLessWindow):
    def __init__(
        self,
        *args,
        shadow_kwargs={},
        parent: QWidget = None,
        **kwargs,
    ):
        FrameLessWindow.__init__(self, parent=parent, **shadow_kwargs)
        _Drawer.__init__(self, *args, **kwargs)


class RoundDrawerWindow(_Drawer, RoundWindow):
    def __init__(
        self,
        *args,
        parent: QWidget = None,
        shadow_kwargs={},
        **kwargs,
    ):
        RoundWindow.__init__(self, parent=parent, **shadow_kwargs)
        _Drawer.__init__(self, *args, **kwargs)


class LeftRoundDrawerWindow(RoundDrawerWindow):
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        RoundDrawerWindow.__init__(self, *args, **kwargs)
        self.windowFrame().setObjectName("left_round_frame")
