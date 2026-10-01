from func import nhlToday
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QHBoxLayout

NHLtoday = nhlToday()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("Sports Hub")
    window.resize(400,300)
    window.show()
    layout = QHBoxLayout(window)

    for game in NHLtoday:
        row = QHBoxLayout()
        row.addWidget(QLabel(game['awayTeam']))
        row.addWidget(QLabel(game['awayScore']))
        layout.addLayout(row)

    sys.exit(app.exec())
    







