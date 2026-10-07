from func import (
    nhlToday, 
    getImage, 
    periodName, 
    getGoals
    )
import sys
from PyQt6.QtCore import (
    QTimer, 
    pyqtSignal
    )
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
    QGraphicsDropShadowEffect,
    QGridLayout
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




class TeamRow(QFrame):
    def __init__(self, logoURL, name, record, score, color):
        super().__init__()
        self.setFixedSize(325, 75)
        self.setStyleSheet(f"background-color: #{color}; border-radius: 8px;")
        self.setFixedHeight(60)

        row = QHBoxLayout(self)

        pixmap = QPixmap()
        pixmap.loadFromData(getImage(logoURL))
        logo = QLabel()
        logo.setPixmap(pixmap.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

        nameLabel = QLabel(name)
        nameLabel.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        recordLabel = QLabel(record)
        recordLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        recordLabel.setFixedWidth(60)

        scoreLabel = QLabel(score)
        scoreLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scoreLabel.setFixedWidth(30)

        row.addWidget(logo)
        row.addWidget(nameLabel, 1)
        row.addWidget(recordLabel)
        row.addWidget(scoreLabel)




class boxScore(QWidget):
    def __init__(self, game):
        super().__init__()

        layout = QGridLayout(self)

        away = game['awayAbbr']
        awayLabel = QLabel(away)
        awayP1 = game['awayPeriods']
        awayP1Label = QLabel()

        for i, goals in enumerate(game['awayPeriods']):
            layout.addWidget(QLabel(goals), 1, i + 1)

        home = game['homeAbbr']
        homeLabel = QLabel(home)

        for i, goals in enumerate(game['homePeriods']):
            layout.addWidget(QLabel(goals), 2, i + 1)

        for i in range(len(game['awayPeriods'])):
            layout.addWidget(QLabel(periodName(i + 1)), 0, i + 1)

        layout.addWidget(awayLabel, 1, 0)
        layout.addWidget(homeLabel, 2, 0)




class GoalScorers(QWidget):
    def __init__(self, game):
        super().__init__()

        goals = getGoals(game['gameID'])

        layout = QVBoxLayout(self)

        for goal in goals:
            
            if goal['teamID'] == game['awayTeamID']:
                color = game['awayTeamHEX']
            else:
                color = game['homeTeamHEX']

            frame = QFrame()
            frame.setObjectName("goalFrame")
            frame.setStyleSheet(f"#goalFrame {{ background-color: #{color}; border-radius: 8px; }}")
            frame.setFixedHeight(70)
            scoringBox = QHBoxLayout(frame)
            
            #PLAYER PHOTO
            playerPhoto = QPixmap()
            playerPhoto.loadFromData(getImage(goal['scorerIMG']))
            scorerIMG = QLabel()
            scorerIMG.setPixmap(playerPhoto.scaled(70, 70, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            scorerIMG.setFixedWidth(70)

            #PLAYER NAME
            
            playerNameLabel = QLabel(goal['scorer'] + " (" + str(goal['scorerYTDGoals']) + ")")
            playerNameLabel.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            playerNameLabel.setFixedHeight(20)


            #ASSIST NAMES
            assistNames = []

            if goal['primaryAssistName']:
                assistNames.append(f'{goal['primaryAssistName']} ({goal['primaryAssistYTD']})')
            if goal['secondaryAssistName']:
                assistNames.append(f'{goal['secondaryAssistName']} ({goal['secondaryAssistYTD']})')

            if assistNames:
                assistText = "Assists: " + ", ".join(assistNames)
            else:
                assistText = "Unassisted"

            assistsLabel = QLabel(assistText)
            assistsLabel.setObjectName("assistsLabel")
            assistsLabel.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            assistsLabel.setFixedHeight(20)
            
            togLabel = QLabel(goal['tog'])
            togLabel.setObjectName("tog")

            textColumn = QVBoxLayout()
            textColumn.setSpacing(0)
            textColumn.setContentsMargins(0, 0, 0, 0)
            textColumn.addWidget(playerNameLabel)
            textColumn.addWidget(assistsLabel)
            textColumn.addWidget(togLabel)

            scoringBox.addWidget(scorerIMG)
            scoringBox.addLayout(textColumn)

            layout.addWidget(frame)
            layout.addStretch()





class GameWindow(QWidget):
    def __init__(self, game):
        super().__init__()

        #WINDOW
        layout = QVBoxLayout(self)
        layout.addWidget(TeamRow(
            game['awayLogo'], 
            game['awayTeam'],
            game['awayRecord'],
            game['awayScore'],
            game['awayTeamHEX']
            ))
        layout.addWidget(TeamRow(
            game['homeLogo'],
            game['homeTeam'],
            game['homeRecord'],
            game['homeScore'],
            game['homeTeamHEX']
        ))
        layout.addWidget(boxScore(game))
        layout.addWidget(GoalScorers(game))





class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('NHL')
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
            #self.adjustSize()


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
            font-size: 36px;
        }

        #assistsLabel {
            font-size: 14px;
        }

        #tog {
            font-size: 12px;
        }

    """)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    








