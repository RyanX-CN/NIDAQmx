from QPSLClass.Base import *
from QPSLClass.QPSLWidgetBase import QPSLWidgetBase
from QPSLClass.QPSLGroupList import QPSLLinearGroupList


class QPSLCheckBox(QCheckBox, QPSLWidgetBase):

    def __init__(self, parent: QWidget, object_name: str, text: str):
        super().__init__(text=text, parent=parent)
        self.set_QPSL_parent(qpsl_parent=parent)
        self.setObjectName(object_name)


class QPSLCheckBoxGroup(QPSLLinearGroupList):

    def __init__(self,
                 parent: QWidget,
                 object_name: str,
                 orientation: Qt.Orientation,
                 texts: Iterable[str] = [],
                 title: str = ""):
        super().__init__(parent=parent,
                         object_name=object_name,
                         orientation=orientation,
                         title=title)
        self.set_options(texts=texts)

    def set_options(self, texts: List[str]):
        self.clear_widgets()
        for opt in texts:
            self.add_widget(widget=QPSLCheckBox(
                self, text=opt, object_name="opt_{0}".format(opt)))


class QPSLCheckBoxHGroup(QPSLCheckBoxGroup):

    def __init__(self,
                 parent: QWidget,
                 object_name: str,
                 texts: Iterable[str] = [],
                 title: str = ""):
        super().__init__(parent=parent,
                         object_name=object_name,
                         orientation=Qt.Orientation.Horizontal,
                         texts=texts,
                         title=title)


class QPSLCheckBoxVGroup(QPSLCheckBoxGroup):

    def __init__(self,
                 parent: QWidget,
                 object_name: str,
                 texts: Iterable[str] = [],
                 title: str = ""):
        super().__init__(parent=parent,
                         object_name=object_name,
                         orientation=Qt.Orientation.Vertical,
                         texts=texts,
                         title=title)