import sys

from PyQt5.QtWidgets import (QApplication, QGridLayout, QGroupBox, QPushButton, QRadioButton,
                             QStyleFactory, QTabWidget, QVBoxLayout, QWidget)

from GUI.Config.config_updaters import set_region

class Widget(QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)

        self.create_settings()
        self.create_dashboard()
        self.show()

        tab_widget = QTabWidget()
        tab_widget.addTab(self.dashboard, '&Dashboard')
        tab_widget.addTab(self.settings, '&Settings')


        self.overall_layout = QGridLayout()
        self.overall_layout.addWidget(tab_widget, 0, 0)

        self.setLayout(self.overall_layout)
        self.setWindowTitle('Champ Select Analyser')
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        QApplication.setPalette(QApplication.style().standardPalette())

    def create_dashboard(self):
        self.dashboard = QGroupBox('Dashboard')

    def create_settings(self):
        self.settings = QGroupBox('Region')

        LCKButton = QRadioButton('LCK')
        LCKButton.clicked.connect(lambda: set_region('LCK'))
        LCKButton.setChecked(True)

        LCSButton = QRadioButton('LCS')
        LCSButton.clicked.connect(lambda: set_region('LCS'))

        LECButton = QRadioButton('LEC')
        LECButton.clicked.connect(lambda: set_region('LEC'))

        LPLButton = QRadioButton('LPL')
        LPLButton.clicked.connect(lambda: set_region('LPL'))

        layout = QVBoxLayout()
        layout.addWidget(LCKButton)
        layout.addWidget(LCSButton)
        layout.addWidget(LECButton)
        layout.addWidget(LPLButton)

        self.settings.setMaximumHeight(layout.count() * 40)
        self.settings.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec_())
