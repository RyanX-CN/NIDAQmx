from Tool import *
from QPSLClass.QPSLStartMode import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = QPSLStartMode_Normal()
    main_window.show()
    sys.exit(app.exec())

