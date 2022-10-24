from .frames import *
from .labels import *


class TitleRadio(QRadioButton):
    def __init__(self, title: str, label: str, parent: QWidget = None):
        super().__init__(parent=parent)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(40, 5, 5, 5)
        lay.setSpacing(5)

        lay.addWidget(Label(text=title, name="bold"))
        lay.addWidget(Label(text=label, name="title_radio_label"))
