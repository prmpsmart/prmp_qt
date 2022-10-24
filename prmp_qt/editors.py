from .frames import *
from .labels import *


class Labeled(VFrame):
    def __init__(
        self,
        editClass: QWidget,
        label: str,
        required: bool = False,
        parent: QWidget = None,
    ):
        super().__init__(parent=parent)

        lay = self.layout()
        lay.setSpacing(2)

        label = (
            RequiredLabel(text=label) if required else Label(text=label, name="bold")
        )

        if required:
            lay.addLayout(label)
        else:
            lay.addWidget(label)

        self.edit: QWidget = editClass()
        self.edit.setObjectName("labeled_edit")
        lay.addWidget(self.edit)

    def text(self) -> str:
        return self.edit.text()

    def setText(self, text: str) -> str:
        return self.edit.setText(text)


class LineEdit(QLineEdit):
    def __init__(self, name: str = "", placehoder: str = ""):
        super().__init__()

        if name:
            self.setObjectName(name)
        if placehoder:
            self.setPlaceholderText(placehoder)


class LabeledEdit(Labeled):
    def __init__(self, *args, placeholder: str = "", **kwargs):
        super().__init__(*args, **kwargs)
        self.edit.setPlaceholderText(placeholder)


class LabeledLineEdit(LabeledEdit):
    def __init__(self, **kwargs):
        super().__init__(QLineEdit, **kwargs)
        self.edit: QLineEdit


class LabeledTextEdit(LabeledEdit):
    def __init__(self, **kwargs):
        super().__init__(QTextEdit, **kwargs)
        self.edit: QTextEdit

    def text(self) -> str:
        return self.edit.toPlainText()

    def setText(self, text: str) -> str:
        return self.edit.setText(text)


class LabeledCombo(Labeled):
    def __init__(self, items: list = [], **kwargs):
        super().__init__(QComboBox, **kwargs)
        self.edit: QComboBox
        if items:
            self.edit.addItems(items)


class TextInput(QTextEdit):
    def __init__(
        self,
        container: QWidget = None,
        callback=None,
        min_height: int = 40,
        max_height: int = 150,
    ):
        super().__init__()

        self.container = container
        self.setPlaceholderText("Type your message ...")

        self.setMinimumHeight(min_height)
        self.setMaximumHeight(max_height)
        self.min_height = min_height
        self.max_height = max_height

        if callback:
            shortcut = QShortcut(QKeySequence("Ctrl+Return"), self)
            shortcut.activated.connect(callback)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.textChanged.connect(self.setTextInputSize)
        # self.textEdited.connect(self.setTextInputSize)

    def setTextInputSize(self):
        br = self.fontMetrics().boundingRect(
            0, 0, self.width(), -1, Qt.TextWrapAnywhere, self.toPlainText()
        )
        h = br.height()
        hh = abs(h)

        if hh < self.min_height:
            hh = self.min_height
        elif hh > self.max_height:
            hh = self.max_height

        if self.container:
            self.container.setMinimumHeight(hh)
            self.container.setMaximumHeight(hh)

    @property
    def text(self) -> str:
        return self.toPlainText().strip()

    def showEvent(self, arg__1: QShowEvent) -> None:
        self.setTextInputSize()
