from QPSLClass.Base import *
from QPSLClass.QPSLWidgetBase import QPSLWidgetBase
from QPSLClass.QPSLPushButton import QPSLPushButton
from QPSLClass.QPSLGroupList import QPSLHorizontalGroupList


class QPSLComboBox(QComboBox, QPSLWidgetBase):

    def __init__(self, parent: QWidget, object_name: str):
        super().__init__(parent=parent)
        self.set_QPSL_parent(qpsl_parent=parent)
        self.setObjectName(object_name)

    def set_texts(self, texts: List[str]):
        old_text = self.currentText()
        self.clear()
        self.addItems(texts)
        if old_text in texts:
            self.setCurrentText(old_text)


class QPSLFreshTextComboBox(QPSLHorizontalGroupList):
    sig_fresh = pyqtSignal()

    def __init__(self,
                 parent: QWidget,
                 object_name: str,
                 text: str,
                 stretch: Tuple[int, ...] = (1, 3)):
        super().__init__(parent=parent, object_name=object_name)
        self.add_widget(
            QPSLPushButton(self, object_name="btn_fresh", text=text))
        self.add_widget(QPSLComboBox(self, object_name="cbox_data"))
        self.set_stretch(sizes=stretch)
        connect_direct(self.btn_fresh.sig_clicked, self.sig_fresh)

    def current_text(self) -> str:
        return self.cbox_data.currentText()

    def add_text(self, text: str):
        self.cbox_data.addItem(text)

    def add_texts(self, texts: List[str]):
        self.cbox_data.addItems(texts)

    def set_texts(self, texts: List[str]):
        self.cbox_data.set_texts(texts=texts)

    @property
    def btn_fresh(self) -> QPSLPushButton:
        return self.get_widget(0)

    @property
    def cbox_data(self) -> QPSLComboBox:
        return self.get_widget(1)