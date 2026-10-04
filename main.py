from func import nhlToday, getImage, nhlYesterday
import sys
from PyQt6.QtCore import QTimer, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, 
    QWidget, 
    QLabel, 
    QHBoxLayout, 
    QVBoxLayout, 
    QMainWindow,
    QFrame,
    QToolTip,
    QPushButton,
    QGraphicsDropShadowEffect
    )
from PyQt6.QtGui import (
    QPixmap,
    QFontDatabase,
    QFont,
    QColor
    )
from PyQt6.QtCore import Qt

class TitleBar(QWidget):
    def __init__(self, window):
        super().__init__()
        self.win = window
        self.setObjectName("titleBar")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setFixedHeight(32)

        row = QHBoxLayout(self)
        row.setContentsMargins(12, 0, 0, 0)
        row.setSpacing(0)

        row.addWidget(QLabel(window.windowTitle()))
        row.addStretch()

        minimize = QPushButton("_")
        minimize.clicked.connect(window.showMinimized)
        close = QPushButton("X")
        close.setObjectName("closeButton")
        close.clicked.connect(window.close)
        for button in (minimize, close):
            button.setFixedSize(40, 32)
            row.addWidget(button)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.win.windowHandle().startSystemMove()

class ClickableFrame(QFrame):
    clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()

class GameWindow(QWidget):
    def __init__(self, game):
        super().__init__()
        self.setWindowTitle(f"{game['awayAbbr']} @ {game['homeAbbr']}")
        self.resize(250, 250)
        self.setObjectName("gameWindow")
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)

        self.awayTeamLogo = QPixmap()
        self.homeTeamLogo = QPixmap()

        #AWAY TEAM
        self.awayTeam = QFrame()
        self.awayTeam.setObjectName("awayTeamFrame")
        self.awayTeam.setStyleSheet(f"#awayTeamFrame {{ background-color: #{game['awayTeamHEX']}; border-radius: 8px; color: #ffffff; }}")

        self.teamAway = QHBoxLayout(self.awayTeam)
        self.awayTeamLogo.loadFromData(getImage(game['awayLogo']))       
        self.teamAwayLogo = QLabel()
        self.teamAwayLogo.setPixmap(self.awayTeamLogo.scaled(
            40, 40,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        ))
        self.teamAway.addWidget(self.teamAwayLogo)
        self.teamAway.addWidget(QLabel(f"{game['awayTeam']}"))
        self.teamAway.addWidget(QLabel(f"{game['awayScore']}"))
        self.teamAway.addWidget(QLabel(f"{game['awayRecord']}"))


        self.homeTeam = QFrame()
        self.homeTeam.setObjectName("homeTeamFrame")
        self.homeTeam.setStyleSheet(f"#homeTeamFrame {{ background-color: #{game['homeTeamHEX']}; border-radius: 8px; color: #ffffff;}}")

        self.teamHome = QHBoxLayout(self.homeTeam)
        self.teamHome.addWidget(QLabel(f"{game['homeTeam']}"))
        self.teamHome.addWidget(QLabel(f"{game['homeScore']}"))
        self.teamHome.addWidget(QLabel(f"{game['homeRecord']}"))



        self.layout.addWidget(self.awayTeam)
        self.layout.addWidget(self.homeTeam)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('NHL')
        self.resize(250, 250)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        widget = QWidget(self)
        self.setCentralWidget(widget)
        self.layout = QVBoxLayout(widget)
        self.layout.addWidget(TitleBar(self))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh)
        self.timer.start(60_000)
        self.refresh()

    def openGame(self, game):
        self.gameWindow = GameWindow(game)
        self.gameWindow.show()

    def refresh(self):

        while self.layout.count() > 1:
            item = self.layout.takeAt(1)
            item.widget().deleteLater()

        NHLtoday = nhlToday()
        
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


            card = ClickableFrame()
            card.clicked.connect(lambda g=game: self.openGame(g))
            card.setObjectName("gameRow")
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

            #AWAY SCORE
            awayScore = QLabel(awayText)
            awayScore.setAlignment(Qt.AlignmentFlag.AlignCenter)
            awayScore.setObjectName("awayScore")
            teamAway.addWidget(awayScore)
            team.addWidget(awayCard)       
            
            #AT
            at = QLabel(str("AT"))
            at.setObjectName("atCard")
            team.addWidget(at)



            #HOME TEAM
            homeCard = QFrame()
            homeCard.setObjectName("homeCard")
            homeCard.setContentsMargins(4, 0, 4, 0)
            homeCard.setFixedHeight(36)
            homeCard.setToolTip(
                f"<b>{game['homeTeam']}</b><br>"
                f"Record: {game['homeRecord']}"
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

            #HOME SCORE
            homeScore = QLabel(homeText)
            homeScore.setAlignment(Qt.AlignmentFlag.AlignCenter)
            homeScore.setObjectName("homeScore")
            teamHome.addWidget(homeScore)

            team.addWidget(homeCard)
            
            
            #DEETS
            time = QLabel(timeText)
            time.setContentsMargins(4, 0, 4, 0)
            time.setFixedHeight(36)
            time.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            time.setObjectName("time")
            team.addStretch()            
            team.addWidget(time)



            #LAYOUT
            self.layout.addWidget(card)



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
            font-size: 18px;
            border-radius: 8px;
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

        #titleBar {
            background-color: #000000;
            border-radius: 8px;      
        }

        #titleBar QPushButton {
            background: transparent;
            border: none;
            color: #8b92a5;
            border-radius: 8px;
        }

        #titleBar QPushButton:hover {
            background-color: #2a2e3d;
            color: #ffffff;
        }

        #closeButton:hover {
            background-color: #e5484d;
            color: #ffffff;
        }

        #atCard {
            color: #000000;
        }

        #awayScore {
            color: #ffffff;
        }

        #homeScore {
            color: #ffffff;
        }

        #time {
            color: #000000;
        }

        #gameRow {
            background-color: #ffffff;
        }

        #gameWindow {
            background-color: #ffffff;
            border-radius: 8px;
        }


    """)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    








