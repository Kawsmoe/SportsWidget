from func import nhlToday, getImage, nhlYesterday
import sys
from PyQt6.QtWidgets import (
    QApplication, 
    QWidget, 
    QLabel, 
    QHBoxLayout, 
    QVBoxLayout, 
    QMainWindow,
    QFrame,
    QToolTip
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
        self.setWindowTitle('NHL')
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
            awayCard.setToolTip(
                f"<b>{game['awayTeam']}</b><br>"
                f"Record: {game['awayRecord']}<br>"
                f"Probable Goaltender: {game['awayProbGoalie']}" 
            )
            awayCard.setStyleSheet(f"#awayCard {{ background-color: #{game['awayTeamHEX']}; border-radius: 8px; }}")
            teamAway = QHBoxLayout(awayCard)

            awayTeam.loadFromData(getImage(game['awayLogo']))
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
            homeCard.setToolTip(
                f"<b>{game['homeTeam']}</b><br>"
                f"Record: {game['homeRecord']}<br>"
                f"Probable Goaltender: {game['homeProbGoalie']}" 
            )
            homeCard.setStyleSheet(f"#homeCard {{ background-color: #{game['homeTeamHEX']}; border-radius: 8px; }}")
            
            teamHome = QHBoxLayout(homeCard)

            homeTeam.loadFromData(getImage(game['homeLogo']))
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

    bebasNeue = QFontDatabase.addApplicationFont("fonts/BebasNeue-Regular.ttf")
    BNfamily = QFontDatabase.applicationFontFamilies(bebasNeue)[0]
    app.setFont(QFont(BNfamily, 16))

    libertine = QFontDatabase.addApplicationFont("fonts/LinLibertine_R.ttf")
    Lfamily = QFontDatabase.applicationFontFamilies(libertine)[0]
    QToolTip.setFont(QFont(Lfamily, 16))

    app.setStyleSheet("""
        QMainWindow, QWidget {
            background-color: #000000;
            color: #ffffff;
            font-size: 18px;
        }
        
        QLabel {
            padding:0px;
            background: transparent;
        }

        QToolTip{
            font-family: "Linux Libertine";
            font-size: 14px;
            color: #ffffff;
        }
        
        #awayCard {
            border-radius: 1px;
        }

        #homeCard {
            border-radius: 1px;
        }

    """)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    








