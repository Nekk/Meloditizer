from Menu import *
from Piano import *
import sys

def main():
    app = QApplication(sys.argv)

    w = menu()
    w.show()

    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())
