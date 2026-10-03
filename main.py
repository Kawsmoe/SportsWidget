from func import nhlToday
import sys
from PyQt6.QtWidgets import (
    QApplication, 
    QWidget, 
    QLabel, 
    QHBoxLayout, 
    QVBoxLayout, 
    QMainWindow
    )



class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        NHLtoday = nhlToday()
        self.setWindowTitle('Sports Hub')
        self.resize(400, 300)

        widget = QWidget(self)
        self.setCentralWidget(widget)
        layout = QVBoxLayout(widget)

        for game in NHLtoday:
            row = QHBoxLayout()
            row.addWidget(QLabel(str(
                game['awayTeam'] + " " +
                game['awayScore'] + " " +
                " at " +
                game['homeTeam'] + " " +
                game['homeScore']
                )))
            row.addWidget(QLabel(str(game['awayScore'])))
            layout.addLayout(row)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    







