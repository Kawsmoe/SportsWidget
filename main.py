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
from PyQt6.QtCore import Qt



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

            #AWAY TEAM
            awayTeam.loadFromData(getTeamImage(game['awayLogo']))
            awayLogo = QLabel()
            awayLogo.setPixmap(awayTeam.scaled(30, 30))
            team.addWidget(awayLogo)
            awayAbbr = QLabel(str(game['awayAbbr']))
            awayAbbr.setAlignment(Qt.AlignmentFlag.AlignCenter)
            team.addWidget(awayAbbr)
            awayScore = QLabel(str(game['awayScore']))
            awayScore.setAlignment(Qt.AlignmentFlag.AlignCenter)
            team.addWidget(awayScore)


            team.addWidget(QLabel(str("AT")))


            #HOME TEAM
            homeTeam.loadFromData(getTeamImage(game['homeLogo']))
            homeLogo = QLabel()
            homeLogo.setPixmap(homeTeam.scaled(30, 30))
            team.addWidget(homeLogo)
            homeAbbr = QLabel(str(game['homeAbbr']))
            homeAbbr.setAlignment(Qt.AlignmentFlag.AlignCenter)
            team.addWidget(homeAbbr)
            homeScore = QLabel(str(game['homeScore']))
            homeScore.setAlignment(Qt.AlignmentFlag.AlignCenter)
            team.addWidget(homeScore)

            #LAYOUT
            layout.addLayout(team)
            layout.setSpacing(2)

        QLabel("Yesterday")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QMainWindow, QWidget {
            background-color: #000000;
            color: #ffffff;
            font-family: "Helvetica", sans-serif;
            font-size: 16px;
            font-weight: bold;
        }
        QLabel {
            padding:2px;
        }

    """)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    
from PyQt6.QtGui import QPixmap








