from func import nhlToday, getTeamImage, nhlYesterday
import sys
from PyQt6.QtWidgets import (
    QApplication, 
    QWidget, 
    QLabel, 
    QHBoxLayout, 
    QVBoxLayout, 
    QMainWindow,
    QFrame
    )
from PyQt6.QtGui import (
    QPixmap,
    QFontDatabase,
    QFont
    )
from PyQt6.QtCore import Qt



class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        NHLtoday = nhlToday()
        NHLYestderday = nhlYesterday()
        self.setWindowTitle('Sports Hub')
        self.resize(250, 250)

        widget = QWidget(self)
        self.setCentralWidget(widget)
        layout = QVBoxLayout(widget)
        
        awayTeam = QPixmap()
        homeTeam = QPixmap()

        for game in NHLtoday:
            card = QFrame()
            team = QHBoxLayout(card)
            team.setContentsMargins(0, 0, 0, 0)

            #AWAY TEAM
            awayCard = QFrame()
            awayCard.setObjectName("awayCard")
            awayCard.setContentsMargins(4, 0, 4, 0)
            teamAway = QHBoxLayout(awayCard)

            awayTeam.loadFromData(getTeamImage(game['awayLogo']))
            awayLogo = QLabel()
            awayLogo.setPixmap(awayTeam.scaled(
                14, 14,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
                ))
            teamAway.addWidget(awayLogo)
            awayAbbr = QLabel(str(game['awayAbbr']))
            awayAbbr.setAlignment(Qt.AlignmentFlag.AlignCenter)
            teamAway.addWidget(awayAbbr)
            awayScore = QLabel(str(game['awayScore']))
            awayScore.setAlignment(Qt.AlignmentFlag.AlignCenter)
            teamAway.addWidget(awayScore)

            team.addWidget(awayCard)



            team.addWidget(QLabel(str("AT")))

            #HOME TEAM
            homeCard = QFrame()
            homeCard.setObjectName("homeCard")
            homeCard.setContentsMargins(4, 0, 4, 0)
            teamHome = QHBoxLayout(homeCard)

            homeTeam.loadFromData(getTeamImage(game['homeLogo']))
            homeLogo = QLabel()
            homeLogo.setPixmap(homeTeam.scaled(
                14, 14,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
                ))
            teamHome.addWidget(homeLogo)
            homeAbbr = QLabel(str(game['homeAbbr']))
            homeAbbr.setAlignment(Qt.AlignmentFlag.AlignCenter)
            teamHome.addWidget(homeAbbr)
            homeScore = QLabel(str(game['homeScore']))
            homeScore.setAlignment(Qt.AlignmentFlag.AlignCenter)
            teamHome.addWidget(homeScore)

            team.addWidget(homeCard)
            #DEETS
            team.addWidget(QLabel(str(game['time'])))

            team.addStretch()

            #LAYOUT
            layout.addWidget(card)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    fontID = QFontDatabase.addApplicationFont("fonts/BebasNeue-Regular.ttf")
    family = QFontDatabase.applicationFontFamilies(fontID)[0]
    app.setFont(QFont(family, 16))

    app.setStyleSheet("""
        QMainWindow, QWidget {
            background-color: #000000;
            color: #ffffff;
            font-size: 18px;
        }
        
        QLabel {
            padding:0px;
        }

        #awayCard {
            background-color: #67d;
            border-radius: 16px;
        }

        #homeCard {
            background-color: #69a;
            border-radius: 16px;
        }

    """)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    








