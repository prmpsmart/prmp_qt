from .commons import *


class Scrollable(QScrollArea):
    def __init__(
        self,
        widgetClass: QWidget = QFrame,
        widgetKwargs={},
        hbar=0,
        vbar=1,
        objectName="",
    ):
        QScrollArea.__init__(self)
        self.setObjectName(objectName)

        self._widget: QWidget = widgetClass(**widgetKwargs)

        self.setWidget(self._widget)
        self.setWidgetResizable(True)

        if hbar:
            self.show_hbar()
        else:
            self.hide_hbar()

        if vbar:
            self.show_vbar()
        else:
            self.hide_vbar()

    def widgetLayout(self) -> QBoxLayout:
        return self._widget.layout()

    def hide_hbar(self):
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def hide_vbar(self):
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def hide_bars(self):
        self.hide_hbar()
        self.hide_vbar()

    def show_hbar(self):
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def show_vbar(self):
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def show_bars(self):
        self.show_hbar()
        self.show_vbar()

    def scroll_down(self, minimum, maximum):
        self.verticalScrollBar().setSliderPosition(maximum)

    def disable_hbar(self):
        self.horizontalScrollBar().setDisabled(True)

    def disable_vbar(self):
        self.verticalScrollBar().setDisabled(True)

    def enable_hbar(self):
        self.horizontalScrollBar().setEnabled(True)
        self.horizontalScrollBar()

    def enable_vbar(self):
        self.verticalScrollBar().setEnabled(True)
