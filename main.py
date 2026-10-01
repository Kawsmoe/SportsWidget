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

NHLtoday = nhlToday()

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Sports Hub')
        self.resize(400, 300)
        
        layout = QVBoxLayout(self)
        for game in nhlToday():
            row = QHBoxLayout()
            row.addWidget(QLabel(game('awayTeam')))
            row.addWidget(QLabel(str(game['awayScore'])))
            layout.addLayout(row)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    







