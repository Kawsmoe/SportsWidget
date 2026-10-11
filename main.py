from func import (
    nhlToday, 
    getImage, 
    periodName, 
    getGoals,
    getShots
    )
import sys
from PyQt6.QtCore import (
    QTimer, 
    pyqtSignal,
    QPointF,
    QRectF
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
    QColor,
    QPainter,
    QPen,
    QBrush,
    QPainterPath,
    QRadialGradient
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
            
            playerNameLabel = QLabel(f"{goal['scorer']} ({goal['scorerYTDGoals']})")
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
            
            #TIME OF GAME
            togLabel = QLabel(f"{goal['tog']} - {goal['strength']} - {goal['shotType']}")
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


class Rink(QWidget):


    def __init__(self, game, goals, shots):
        super().__init__()
        self.game = game
        self.goals = goals
        self.shots = shots
        self.setFixedSize(500,212)

        self.awayLogo = QPixmap()
        self.awayLogo.loadFromData(getImage(self.game['awayLogo']))
        self.awayLogo = self.awayLogo.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.homeLogo = QPixmap()
        self.homeLogo.loadFromData(getImage(self.game['homeLogo']))
        self.homeLogo = self.homeLogo.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)


    def paintEvent(self, event):

        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        W, H = self.width(), self.height()

        fx = W / 200
        fy = H /85

        def X(x): return (x + 100) * fx
        def Y(y): return (42.5 - y) * fy

        #WHOLE ICE
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QBrush(QColor("#eef")))
        p.drawRoundedRect(QRectF(1, 1, W - 2, H - 2), 28 * fx, 28 * fy)

        #RED LINE
        p.setPen(QPen(QColor("#c33"), 2))
        p.drawLine(QPointF(W / 2, 0), QPointF(W / 2, H))

        #LEFT BLUE LINE
        p.setPen(QPen(QColor("blue"), 2))
        p.drawLine(QPointF((-25 + 100) / 200 * W , 0), QPointF((-25 + 100) / 200 * W , H))

        #RIGHT BLUE LINE
        p.setPen(QPen(QColor("blue"), 2))
        p.drawLine(QPointF((25 + 100) / 200 * W , 0), QPointF((25 + 100) / 200 * W , H))

        #CENTER ICE CIRCLE
        p.setPen(QPen(QColor("blue"), 1))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawEllipse(QPointF(W / 2, H / 2), 15 * (W / 200), 15 * (H / 85))

        #CENTER ICE DOT
        p.setPen(QPen(QColor("blue"), 1))
        p.setBrush(QBrush(QColor("blue")))
        p.drawEllipse(QPointF(W / 2, H / 2), 0.5 * fx, 0.5 * fy)


        #LEFT GOAL LINE
        p.setPen(QPen(QColor("red"), 1))
        p.drawLine(QPointF((89 + 100) / 200 * W , 17), QPointF((89 + 100) / 200 * W , H - 17))

        #RIGHT GOAL LINE
        p.setPen(QPen(QColor("red"), 1))
        p.drawLine(QPointF((-89 + 100) / 200 * W , 17), QPointF((-89 + 100) / 200 * W , H - 17))

        #LEFT NET
        p.setPen(QPen(QColor("red"), 1))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawRect(QRectF((-93 + 100) / 200 * W, (42.5 - 3) / 85 * H, 4 * W / 200, 6 * H /85))

        #RIGHT NET
        p.setPen(QPen(QColor("red"), 1))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawRect(QRectF((89 + 100) / 200 * W, (42.5 - 3) / 85 * H, 4 * W / 200, 6 * H /85))

        #CREASES
        p.setPen(QPen(QColor("red"), 1))
        p.setBrush(QBrush(QColor("#bde")))
        for side in (-1, 1):

            x0 = X(89 * side)
            cy = Y(0)
            out = -side * 4.47 * fx
            box = QRectF(x0 - 6 * fx, cy - 6 * fy, 12 * fx, 12 * fy)

            path = QPainterPath()
            path.moveTo(x0, cy - 4 * fy)
            path.lineTo(x0 + out, cy - 4 * fy)
            if side == -1:
                path.arcTo(box, 41.8, -83.6)
            else:
                path.arcTo(box, 138.2, 83.6)
            path.lineTo(x0, cy + 4 * fy)
            path.closeSubpath()
            p.drawPath(path)

        #END ZONE FACEOFF CIRCLES AND DOTS
        for side in (-1, 1):
            for row in (-1, 1):
                cx, cy = X(69 * side), Y(22 * row)
                p.setPen(QPen(QColor("red"), 1))
                p.setBrush(Qt.BrushStyle.NoBrush)
                p.drawEllipse(QPointF(cx, cy), 15 * fx, 15 * fy)
                p.setBrush(QBrush(QColor("red")))
                p.drawEllipse(QPointF(cx, cy), 1 * fx, 1 * fy)

        #NEUTRAL ZONE DOTS
        p.setPen(QPen(QColor("red"), 1))
        p.setBrush(QBrush(QColor("red")))
        for side in (-1, 1):
            for row in (-1, 1):
                p.drawEllipse(QPointF(X(20 * side), Y(22 * row)), 1 * fx, 1 * fy)

        for s in self.shots:

            x = s['xCoord']
            y = s['yCoord']
            teamID = s['teamID']

            if x is None or y is None:
                continue

            if teamID is None:
                continue

            if s['teamID'] == self.game['awayTeamID']:
                color = self.game['awayTeamHEX']

                if x < 0:
                    x, y = -x, -y
                
            else:
                color = self.game['homeTeamHEX']
                if x > 0:
                    x, y = -x, -y

            px = (x + 100) / 200 * W
            py = (42.5 - y) / 85 * H

            c = QColor(f"#{color}")
            c.setAlpha(255)
            clear = QColor(f'#{color}')
            clear.setAlpha(0)

            grad = QRadialGradient(QPointF(px,py), 3 * fx)
            grad.setColorAt(0, c)
            grad.setColorAt(1, clear)

            p.setPen(QPen(Qt.PenStyle.NoPen))
            p.setBrush(QBrush(grad))
            p.drawEllipse(QPointF(px, py), 9 * fx, 9 * fx)

        for g in self.goals:

            x = g['xCoord']
            y = g['yCoord']

            if x is None or y is None:
                continue

            if g['teamID'] == self.game['awayTeamID']:
                color = self.game['awayTeamHEX']
                if x < 0:
                    x, y = -x, -y
                
            else:
                color = self.game['homeTeamHEX']
                if x > 0:
                    x, y = -x, -y
                
            px = (x + 100) / 200 * W
            py = (42.5 - y) / 85 * H
            p.setPen(QPen(QColor("white"), 1))
            p.setBrush(QBrush(QColor(f"#{color}")))
            p.drawEllipse(QPointF(px, py), 5, 5)

        #AWAY LOGO
        p.drawPixmap(QPointF(X(12) - self.awayLogo.width() / 2, Y (0) - self.awayLogo.height() / 2), self.awayLogo)

        #HOME LOGO
        p.drawPixmap(QPointF(X(-12) - self.homeLogo.width() / 2, Y (0) - self.homeLogo.height() / 2), self.homeLogo)


        #OUTLINE
        p.setPen(QPen(QColor("#9bb"), 2))
        p.setBrush(QBrush(Qt.BrushStyle.NoBrush))
        p.drawRoundedRect(QRectF(1, 1, W - 2, H - 2), 28 * fx, 28 * fy)




class GameWindow(QWidget):
    def __init__(self, game):
        super().__init__()

        goals = getGoals(game['gameID'])
        shots = getShots(game['gameID'])

        layout = QHBoxLayout(self)
        #WINDOW
        layoutLeft = QVBoxLayout(self)
        layoutLeft.addWidget(TeamRow(
            game['awayLogo'], 
            game['awayTeam'],
            game['awayRecord'],
            game['awayScore'],
            game['awayTeamHEX']
            ))
        layoutLeft.addWidget(TeamRow(
            game['homeLogo'],
            game['homeTeam'],
            game['homeRecord'],
            game['homeScore'],
            game['homeTeamHEX']
        ))
        layoutLeft.addWidget(boxScore(game))
        layoutLeft.addWidget(GoalScorers(game))
        
        rink = Rink(game, goals, shots)

        layout.addLayout(layoutLeft)
        layout.addWidget(rink, alignment=Qt.AlignmentFlag.AlignTop)




class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('NHL')
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.gameWindow = None

        widget = QWidget(self)
        self.setCentralWidget(widget)
        self.layout = QVBoxLayout(widget)
        self.layout.addWidget(TitleBar(self))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh)
        self.timer.start(60_000)
        self.refresh()

    def openGame(self, game):   
        
        oldPOS = None
        
        if self.gameWindow is not None:
            oldPOS = self.gameWindow.pos()
            self.gameWindow.close()
            
        self.gameWindow = GameWindow(game)    
        
        if oldPOS is not None:
            self.gameWindow.move(oldPOS)
        
        
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
    








