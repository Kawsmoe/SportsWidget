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
            if game['state'] == 'pre':
                awayText = ""
                homeText = ""
                timeText = str(game['time'])
            else:
                awayText = str(game['awayScore'])
                homeText = str(game['homeScore'])
                timeText = str(game['status'])

            card = QFrame()
            team = QHBoxLayout(card)
            team.setContentsMargins(0, 0, 0, 0)

            #AWAY TEAM
            awayCard = QFrame()
            awayCard.setObjectName("awayCard")
            awayCard.setContentsMargins(4, 0, 4, 0)
            awayCard.setFixedHeight(36)
            awayCard.setStyleSheet(f"#awayCard {{ background-color: #{game['awayTeamHEX']}; border-radius: 16px; }}")
            teamAway = QHBoxLayout(awayCard)

            awayTeam.loadFromData(getTeamImage(game['awayLogo']))
            awayLogo = QLabel()
            awayLogo.setPixmap(awayTeam.scaled(
                20, 20,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
                ))
            teamAway.addWidget(awayLogo)
            awayAbbr = QLabel(str(game['awayAbbr']))
            awayAbbr.setAlignment(Qt.AlignmentFlag.AlignCenter)
            awayAbbr.setFixedWidth(30)
            teamAway.addWidget(awayAbbr)
            awayScore = QLabel(awayText)
            awayScore.setAlignment(Qt.AlignmentFlag.AlignCenter)
            teamAway.addWidget(awayScore)

            team.addWidget(awayCard)



            team.addWidget(QLabel(str("AT")))

            #HOME TEAM
            homeCard = QFrame()
            homeCard.setObjectName("homeCard")
            homeCard.setContentsMargins(4, 0, 4, 0)
            homeCard.setFixedHeight(36)
            homeCard.setStyleSheet(f"#homeCard {{ background-color: #{game['homeTeamHEX']}; border-radius: 16px; }}")
            
            teamHome = QHBoxLayout(homeCard)

            homeTeam.loadFromData(getTeamImage(game['homeLogo']))
            homeLogo = QLabel()
            homeLogo.setPixmap(homeTeam.scaled(
                20, 20,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
                ))
            teamHome.addWidget(homeLogo)
            homeAbbr = QLabel(str(game['homeAbbr']))
            homeAbbr.setAlignment(Qt.AlignmentFlag.AlignCenter)
            homeAbbr.setFixedWidth(30)
            teamHome.addWidget(homeAbbr)
            homeScore = QLabel(homeText)
            homeScore.setAlignment(Qt.AlignmentFlag.AlignCenter)
            teamHome.addWidget(homeScore)

            team.addWidget(homeCard)
            #DEETS
            time = QLabel(timeText)
            time.setContentsMargins(4, 0, 4, 0)
            time.setFixedHeight(36)
            time.setAlignment(Qt.AlignmentFlag.AlignCenter)
            team.addWidget(time)

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
            background-color: transparent;
            color: #ffffff;
            font-size: 18px;
            border-radius: 8px;
        }
        
        QLabel {
            padding:0px;
            background: transparent;
        }

        #awayCard {

            border-radius: 4px;
        }

        #homeCard {

            border-radius: 4px;
        }

    """)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    








