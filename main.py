from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel
from PyQt6 import uic
import sys

from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl
# (ukelele) Sound Effect by <a href="https://pixabay.com/users/dominique_garnier-43933898/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=334693">Dominique GARNIER</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=334693">Pixabay</a>
from PyQt6.QtCore import QTimer

from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize
# https://fonts.google.com/icons?selected=Material+Symbols+Outlined:timer_pause:FILL@0;wght@400;GRAD@0;opsz@48&icon.size=60&icon.color=%23FFFFFF&icon.query=timer&icon.platform=web
# https://fonts.google.com/icons?selected=Material+Symbols+Outlined:timer_play:FILL@0;wght@400;GRAD@0;opsz@48&icon.size=60&icon.color=%23FFFFFF&icon.query=timer&icon.platform=web

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi("pomodoro.ui", self)

        self.setWindowTitle("POMODORO TRACKER")

        # Parameters
        self.work = True                     # True: Work               False: Break
        self.pauseButton = False             # True: time stopped       False: time goes on
        self.percentage.setText(f"0%")       # What percentage of work has been completed?
        self.showOrHideProgressBar = False   # True: show bar           False: hide bar

        # Hiding progressBar and percentage at the beginning
        self.percentage.hide()
        self.progressBar.hide()

        # Let's Connect the Button Signals
        self.startButton.clicked.connect(self.goToSelectPomodoroPage)

        self.pom_25_5.clicked.connect(lambda: self.goToChooseHowManySessionPage(25, 5))
        self.pom_45_15.clicked.connect(lambda: self.goToChooseHowManySessionPage(45, 15))
        self.pom_60_15.clicked.connect(lambda: self.goToChooseHowManySessionPage(60, 15))
        self.pom_90_30.clicked.connect(lambda: self.goToChooseHowManySessionPage(90, 30))

        self.howManyInput.returnPressed.connect(self.goToLetsGoPage)

        self.letsGoButton.clicked.connect(self.goToWorkBreakPage)

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateCountdown)

        self.pauseOrContinueButton.clicked.connect(self.pauseContinue)

        self.byeButton.clicked.connect(self.closeApp)


        # Adding an icon to the Pause/Continue button
        self.pauseOrContinueButton.setIcon(QIcon("timer_pause.png"))
        self.pauseOrContinueButton.setIconSize(QSize(60, 60))


        # Add sound
        self.musicPlayer = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.musicPlayer.setAudioOutput(self.audioOutput)   # Without this line, there will be no sound.

        self.audioOutput.setVolume(0.4)     # We adjust the volume. (Between 0.0 and 1.0)

        
    
    # Functions
    def goToSelectPomodoroPage(self):        # Go to second page (0, 1, 2, ...)
        self.stackedWidget.setCurrentIndex(1)
        self.howManyInput.clear()  # Cleaning the input is good for the user

    def goToChooseHowManySessionPage(self, workD, breakD):
        self.workDuration = workD
        self.breakDuration = breakD
        self.stackedWidget.setCurrentIndex(2)

    def goToLetsGoPage(self):
        try:
            self.howMany = int(self.howManyInput.text())    # If the number is not entered, ask to enter it again.
        except:
            self.howManyInput.clear()
            self.howManyQuestion.setText("You should input a number.<br>Try again.")
            return

        self.totalTimeInMinutes = ((self.workDuration * self.howMany) + (self.breakDuration * (self.howMany - 1)))
        self.totalRemainingSeconds = self.totalTimeInMinutes * 60

        if ((self.workDuration * self.howMany) + (self.breakDuration * (self.howMany - 1))) <= 24 * 60:
            self.stackedWidget.setCurrentIndex(3)
        else:
            self.howManyInput.clear()
            self.howManyQuestion.setText("Even superheroes need sleep!<br>Try a more realistic goal under 24 hours.")

    def goToWorkBreakPage(self):
        self.stackedWidget.setCurrentIndex(4)

        self.musicPlayer.setSource(QUrl.fromLocalFile("calypso-ukulele-6-seconds.mp3"))
        self.musicPlayer.play()

        if self.work == True:
            self.workOrBreak.setText("WORK")
            self.pauseOrContinueButton.show()

            self.stackedWidget.setStyleSheet("""
            color: rgb(255, 255, 255);
            background-color: rgb(134, 165, 231);
            """)

            self.countdownLabel.setStyleSheet("""
            color: rgb(255, 255, 255);
            border: 2px solid rgb(79, 110, 180);
            background-color: rgb(93, 124, 218);
            padding-top: 10px;
            border-radius: 15px;
            """)

            self.progressBar.setFixedHeight(10)
            self.progressBar.setTextVisible(False)
            self.progressBar.setStyleSheet("""
            QProgressBar {
            background-color: rgb(134, 165, 231);
            }
            QProgressBar::chunk {
            border: 2px solid rgb(79, 110, 180);
            background-color: rgb(93, 124, 218);
            border-right: 5px solid white;
            border-radius: 15px;
            }
            """)

            self.remainingMinutes = self.workDuration
            self.remainingSeconds = self.remainingMinutes * 60
        else:
            self.workOrBreak.setText("BREAK")
            self.pauseOrContinueButton.hide()

            self.stackedWidget.setStyleSheet("""
            background-color: rgb(166, 164, 238)
            """)
            self.countdownLabel.setStyleSheet("""
            color: rgb(255, 255, 255);
            background-color: rgb(135, 128, 209);
            border: 2px solid rgb(115, 101, 184);
            padding-top: 10px;
            border-radius: 15px;
            """)

            self.progressBar.setFixedHeight(10)
            self.progressBar.setTextVisible(False)
            self.progressBar.setStyleSheet("""
            QProgressBar {
            background-color: rgb(166, 164, 238);
            }
            QProgressBar::chunk {
            background-color: rgb(135, 128, 209);
            border: 2px solid rgb(115, 101, 184);
            border-right: 5px solid white;
            border-radius: 15px;
            }
            """)

            
            self.remainingMinutes = self.breakDuration
            self.remainingSeconds = self.remainingMinutes * 60

        self.countdownLabel.setText(f"{self.remainingMinutes:02d}:00")

        self.timer.start(1000)  # Runs every 1 second

    def updateCountdown(self):
        self.progress = float(((self.totalTimeInMinutes * 60) - self.totalRemainingSeconds) / (self.totalTimeInMinutes * 60) * 100)
        self.percentage.setText(f"{int(self.progress)}%")
        self.progressBar.setValue(int(self.progress))

        if self.checkProgress.isChecked():
            showOrHideProgressBar = True
            self.progressBar.show()
            self.percentage.show()
        else:
            showOrHideProgressBar = False
            self.progressBar.hide()
            self.percentage.hide()

        if self.remainingSeconds > 0:
            self.totalRemainingSeconds -= 1
            self.remainingSeconds -= 1
            self.minutes = self.remainingSeconds // 60
            self.seconds = self.remainingSeconds % 60
            self.countdownLabel.setText(f"{self.minutes:02d}:{self.seconds:02d}")
        else:
            self.timer.stop()
            
            if self.work == False or self.howMany == 1:
                self.howMany -= 1
                self.work = True
            else:
                self.work = False

            if self.howMany == 0:
                self.musicPlayer.setSource(QUrl.fromLocalFile("calypso-ukulele-6-seconds.mp3"))
                self.musicPlayer.play()
                self.stackedWidget.setCurrentIndex(5)
            else:
                self.goToWorkBreakPage()

    def pauseContinue(self):
        if self.pauseButton == False:
            self.timer.stop()
            
            self.pauseOrContinueButton.setIcon(QIcon("timer_play.png"))
            self.pauseOrContinueButton.setIconSize(QSize(60, 60))

            self.pauseButton = True
        else:
            self.timer.start(1000)

            self.pauseOrContinueButton.setIcon(QIcon("timer_pause.png"))
            self.pauseOrContinueButton.setIconSize(QSize(60, 60))

            self.pauseButton = False

    def closeApp(self):
        self.close()

        

app = QApplication(sys.argv)         # or app = QApplication([])

window = MainWindow()
window.showFullScreen()

sys.exit(app.exec())