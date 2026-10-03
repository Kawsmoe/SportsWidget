from func import nhlToday, getTeamImage, nhlYesterday
import sys
from PyQt6.QtWidgets import (
    QApplication, 
    QWidget, 
    QLabel, 
    QHBoxLayout, 
    QVBoxLayout, 
    QMainWindow
    )
from PyQt6.QtGui import QPixmap



class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        NHLtoday = nhlToday()
        NHLYestderday = nhlYesterday()
        self.setWindowTitle('Sports Hub')
        self.resize(400, 300)

        widget = QWidget(self)
        self.setCentralWidget(widget)
        layout = QVBoxLayout(widget)
        
        awayTeam = QPixmap()
        homeTeam = QPixmap()


        for game in NHLtoday:
            team = QHBoxLayout()
            scores = QHBoxLayout()

            awayTeam.loadFromData(getTeamImage(game['awayLogo']))
            awayLogo = QLabel()
            awayLogo.setPixmap(awayTeam.scaled(30, 30))
            team.addWidget(awayLogo)
            scores.addWidget(QLabel(str(game['awayScore'])))

            homeTeam.loadFromData(getTeamImage(game['homeLogo']))
            homeLogo = QLabel()
            homeLogo.setPixmap(homeTeam.scaled(30, 30))
            team.addWidget(homeLogo)
            scores.addWidget(QLabel(str(game['homeScore'])))

            layout.addLayout(team)
            layout.addLayout(scores)
            layout.setSpacing(2)

        QLabel("Yesterday")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QMainWindow, QWidget {
            background-color: #ffffff;
            color: #000000;
            font-family: "Inter", sans-serif;
            font-size: 16px;
        }
        QLabel {
            padding:2px;
        }
    """)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    
from PyQt6.QtGui import QPixmap








