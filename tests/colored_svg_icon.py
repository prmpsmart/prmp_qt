import site, os

site.addsitedir("../")

from prmp_qt import *


dir = r"C:\Users\Administrator\Coding_Projects\Icons\tabler-icons\icons-png"
# provide a directory that contains on .svg files

ALL_SVGS = []
SVGS = []

for file in os.listdir(dir):
    if len(SVGS) == 15:
        ALL_SVGS.append(SVGS)
        SVGS = []
        if len(ALL_SVGS) == 3:
            break
    SVGS.append(os.path.join(dir, file))

COLOR = Qt.darkBlue

COMPOSITION_MODES = [
    SvgCompositions.Overlay,
    SvgCompositions.SourceIn,
    SvgCompositions.SourceOut,
    SvgCompositions.SourceAtop,
]

COUNT = 0
SIZE = 30

class Icon(QPushButton):
    def __init__(self, icon: str, icon_func=None):
        super().__init__(
            COMPOSITION_MODES[COUNT]
            .name
            if icon_func
            else ""
        )

        icon = icon_func(icon,color=COLOR) if icon_func else QIcon(icon)
        self.setIcon(icon)
        self.setIconSize(QSize(SIZE, SIZE))


class App(QApplication):
    def __init__(self):
        super().__init__()

        global COUNT

        self.setStyleSheet(
            """
        QLabel {
            background-color: #f2c88b;
            font-weight: bold;
            padding: 5px;
        }
        """
        )

        self.win = QWidget()
        self.win.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.win.move(200, 30)
        lay = QHBoxLayout(self.win)
        lay.setSpacing(50)

        icons_funcs = None, QSvgIcon
        icons_funcs_str = "Normal", "QSvgIcon"

        for label, icon_func in zip(icons_funcs_str, icons_funcs):
            l = QVBoxLayout()
            l.setSpacing(5)
            lay.addLayout(l)
            l.addWidget(QLabel(label))

            hlay = QHBoxLayout()
            l.addLayout(hlay)

            c = 0
            for svgs in ALL_SVGS:
                vlay = QVBoxLayout()
                hlay.addLayout(vlay)

                for svg in svgs:
                    c += 1
                    COUNT = c % len(COMPOSITION_MODES)
                    vlay.addWidget(Icon(svg, icon_func))
            # break

        self.win.show()
        self.exec()


App()
