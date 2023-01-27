from .frames import *


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


class SearchableItem:
    def __init__(self):
        ...

    def search(self, text: str) -> bool:
        return False


SearchableItems = list[SearchableItem]


class SearchableList(Scrollable):
    def __init__(self, reverse: bool = False, **kwargs):
        super().__init__(VFrame, **kwargs)

        self.items: SearchableItems = []
        self.reverse = reverse

        m = 2
        self.widgetLayout().setContentsMargins(m, m, m, m)
        self.widgetLayout().setSpacing(m)
        if reverse:
            self.widgetLayout().setDirection(QBoxLayout.Direction.BottomToTop)

        self.spacerItem = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.widgetLayout().addItem(self.spacerItem)

    @property
    def arranged_items(self) -> SearchableItems:
        return self.arrange_items(self.items)

    def add(
        self,
        item: SearchableItem,
        stretch: int = 0,
        alignment: Qt.Alignment = Qt.AlignCenter,
    ):
        assert isinstance(item, SearchableItem)

        lay = self.widgetLayout()
        
        args = [item, stretch]
        if alignment:
            args.append(alignment)
        lay.addWidget(*args)

    def addItem(self, item: SearchableItem, alignment: Qt.Alignment = Qt.AlignCenter):
        self.add(item)
        self.items.append(item)

    def remove(self, item: SearchableItem):
        assert isinstance(item, SearchableItem)
        self.widgetLayout().removeWidget(item)

    def removeItem(self, item: SearchableItem):
        self.remove(item)
        if item in self.items:
            self.items.remove(item)
            
        self.widget().update()
        self.update()

    def deleteItem(self, item: SearchableItem):
        self.removeItem(item)
        item.deleteLater()

    def deleteItems(self):
        for item in self.widget().children():
            if isinstance(item, SearchableItem):
                self.deleteItem(item)

    def clear(self):
        for item in self.widget().children():
            if isinstance(item, SearchableItem):
                self.remove(item)

    def search(self, text: str):
        self.clear()

        item: QWidget
        for item in self.items:
            if text:
                valid = item.search(text)
            else:
                valid = True

            item.setVisible(valid)

        self.fill(self.items)

    def fill(self, items: SearchableItems):
        items = self.arrange_items(items)

        for item in reversed(items):
            self.widgetLayout().insertWidget(0, item)

    def fillItems(self, items: SearchableItems):
        self.fill(items)
        self.items = items

    def arrange_items(self, items: SearchableItems) -> SearchableItems:
        "A method to customized the order of the search, it can be override in subclasses"
        return items



class TableItem:
    def __init__(
        self,
        value,
        foreground: Union[Qt.GlobalColor, QColor] = None,
        background: Union[Qt.GlobalColor, QColor] = None,
        editable=False,
    ):
        self.editable = editable
        self.text = str(value)

        self.foreground = foreground
        self.background = background

    def updateItem(self, item: QTableWidgetItem):
        item.setText(self.text)

        if self.foreground:
            item.setForeground(self.foreground)
        if self.background:
            item.setBackground(self.background)

        if self.editable:
            item.setFlags(Qt.ItemIsEditable)
        elif self.editable == False:
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        else:
            item.setFlags(Qt.NoItemFlags)

        item.setTextAlignment(Qt.AlignCenter)

    def __str__(self):
        return f"{self.__class__.__name__}({self.text})"

    def __repr__(self):
        return f"<{self}>"


class TableHeaderItem(TableItem):
    def __init__(
        self,
        *args,
        editableColumns=False,
        colorItems=False,
        itemsForeground: Union[Qt.GlobalColor, QColor] = None,
        itemsBackground: Union[Qt.GlobalColor, QColor] = None,
        useSelfColors=False,
        **kwargs,
    ):
        super().__init__(*args, editable=None, **kwargs)

        self.editableColumns = editableColumns
        self.colorItems = colorItems
        self.itemsForeground = itemsForeground
        self.itemsBackground = itemsBackground

        if useSelfColors:
            self.itemsForeground = itemsForeground or self.foreground
            self.itemsBackground = itemsBackground or self.background


SPLITTER = TableHeaderItem("█")


class Table(QTableWidget):
    COLUMNS: List[TableHeaderItem] = []
    BOLD_COLUMNS = []
    BOLD_ROWS = []
    INFINITE_ROWS = False

    def __init__(self, verticalVisible=True, **kwargs):
        QTableWidget.__init__(self)

        self.setAlternatingRowColors(True)
        self.setWordWrap(True)
        self.setShowGrid(True)
        self.setSelectionBehavior(self.SelectColumns)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.setColumnCount(len(self.COLUMNS))

        self.fillHeaders()

        self.verticalHeader().setVisible(verticalVisible)

        self.cellActivated.connect(self.onCellActivated)
        self.cellChanged.connect(self.onCellChanged)
        self.cellClicked.connect(self.onCellClicked)
        self.cellDoubleClicked.connect(self.onCellDoubleClicked)
        self.cellEntered.connect(self.onCellEntered)
        self.cellPressed.connect(self.onCellPressed)
        self.currentCellChanged.connect(self.onCurrentCellChanged)
        self.currentItemChanged.connect(self.onCurrentItemChanged)
        self.itemActivated.connect(self.onItemActivated)
        self.itemChanged.connect(self.onItemChanged)
        self.itemClicked.connect(self.onItemClicked)
        self.itemDoubleClicked.connect(self.onItemDoubleClicked)
        self.itemEntered.connect(self.onItemEntered)
        self.itemPressed.connect(self.onItemPressed)
        self.itemSelectionChanged.connect(self.onItemSelectionChanged)

    def fillHeaders(self):
        self.clear()

        self.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )

        for index, headerItem in enumerate(self.COLUMNS):

            item = QTableWidgetItem()
            headerItem.updateItem(item)
            font = item.font()
            font.setBold(True)
            font.setPointSize(12 if headerItem != SPLITTER else 8)
            item.setFont(font)

            self.setHorizontalHeaderItem(index, item)

    def pad_row(self, row: List):
        l = len(self.COLUMNS)
        r = len(row)

        if l > r:
            for _ in range(l - r):
                row.append(0)

    def fillTable(self, datas: List[List], prefixes: List[List] = []):
        if prefixes:
            print(len(datas), len(prefixes))
            assert len(datas) == len(prefixes)

        self.clearContents()

        l = len(datas)
        self.setRowCount(l if not self.INFINITE_ROWS else l + 10)
        l = len(self.COLUMNS)

        prefix = bool(prefixes)

        for row_index, data in enumerate(datas):
            if prefix:
                data = prefixes[row_index] + data

                if len(data) < l:
                    self.pad_row(data)

            for column_index, value in enumerate(data):
                item = QTableWidgetItem()
                item.setData(Qt.UserRole, value)
                if value:
                    column_header = self.COLUMNS[column_index]

                    dic = {}
                    if column_header.colorItems:
                        dic.update(
                            foreground=column_header.itemsForeground,
                            background=column_header.itemsBackground,
                        )

                    tableItem = TableItem(
                        value,
                        editable=column_header.editableColumns,
                        **dic,
                    )

                    if (row_index in self.BOLD_ROWS) or (
                        column_index in self.BOLD_COLUMNS
                    ):
                        font = item.font()
                        font.setBold(True)
                        font.setPointSize(12)
                        item.setFont(font)
                    tableItem.updateItem(item)
                else:
                    item.setFlags(Qt.NoItemFlags)

                self.setItem(row_index, column_index, item)

        self.fillSplitters()

    def fillSplitters(self):
        rows = self.rowCount()
        for column_index, column in enumerate(self.COLUMNS):
            if column == SPLITTER:
                for row_index in range(rows):
                    item = QTableWidgetItem()
                    font = item.font()
                    font.setPointSize(8)
                    item.setFont(font)
                    SPLITTER.updateItem(item)
                    self.setItem(row_index, column_index, item)

    def onCellActivated(self, row: int, column: int):
        ...

    def onCellChanged(self, row: int, column: int):
        ...

    def onCellClicked(self, row: int, column: int):
        ...

    def onCellDoubleClicked(self, row: int, column: int):
        ...

    def onCellEntered(self, row: int, column: int):
        ...

    def onCellPressed(self, row: int, column: int):
        ...

    def onCurrentCellChanged(
        self,
        currentRow: int,
        currentColumn: int,
        previousRow: int,
        previousColumn: int,
    ):
        ...

    def onCurrentItemChanged(
        self, current: QTableWidgetItem, previous: QTableWidgetItem
    ):
        ...

    def onItemActivated(self, item: QTableWidgetItem):
        ...

    def onItemChanged(self, item: QTableWidgetItem):
        ...

    def onItemClicked(self, item: QTableWidgetItem):
        ...

    def onItemDoubleClicked(self, item: QTableWidgetItem):
        ...

    def onItemEntered(self, item: QTableWidgetItem):
        ...

    def onItemPressed(self, item: QTableWidgetItem):
        ...

    def onItemSelectionChanged(self):
        ...


'''
Table class example.

class DCMonthlyAnalysisBookTable(DCTable):
    COLUMNS = [
        TableHeaderItem("Date"),
        TableHeaderItem("Current"),
        TableHeaderItem("Last"),
        TableHeaderItem("Next"),
        TableHeaderItem("Total", background=Qt.green),
        TableHeaderItem("Upfront Loan"),
        TableHeaderItem("Upfront Repaid"),
        TableHeaderItem("Paidout", background=Qt.darkRed, foreground=Qt.white),
        TableHeaderItem("B-T-O", background=Qt.darkGreen),
        TableHeaderItem("Excess", background=Qt.yellow),
        TableHeaderItem("Deficit", background=Qt.darkGray),
        TableHeaderItem("Withdrawal", background=Qt.red),
        TableHeaderItem("Total Debits", background=Qt.red),
    ]

'''
