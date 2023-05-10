import sys, os, csv, datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, \
    QRadioButton, QButtonGroup, QComboBox, QTextEdit, QWidget, QMessageBox


class AppointmentReminderApp(QMainWindow):
    def __init__(self):
        """
        Initialize the main window of the appointment reminder app
        """

        super().__init__()
        self.setWindowTitle("Appointment Reminder App")
        self.init_ui()

    def init_ui(self):
        """
        Initialize the user interface of the appointment reminder app
        """

        main_layout = QVBoxLayout()

        # Days
        days_layout = QHBoxLayout()
        days_label = QLabel("Day:")
        days_layout.addWidget(days_label)

        self.day_buttons = QButtonGroup()
        for i, day in enumerate(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]):
            button = QRadioButton(day)
            days_layout.addWidget(button)
            self.day_buttons.addButton(button, i)

        main_layout.addLayout(days_layout)

        # Time
        time_layout = QHBoxLayout()
        time_label = QLabel("Time:")
        time_layout.addWidget(time_label)

        self.time_input = QLineEdit()
        time_layout.addWidget(self.time_input)

        self.am_pm_dropdown = QComboBox()
        self.am_pm_dropdown.addItem("AM")
        self.am_pm_dropdown.addItem("PM")
        time_layout.addWidget(self.am_pm_dropdown)

        main_layout.addLayout(time_layout)

        # Reason
        reason_layout = QHBoxLayout()
        reason_label = QLabel("Reason:")
        reason_layout.addWidget(reason_label)

        self.reason_input = QTextEdit()
        reason_layout.addWidget(self.reason_input)

        main_layout.addLayout(reason_layout)

        # Buttons
        buttons_layout = QHBoxLayout()

        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_form)
        buttons_layout.addWidget(clear_button)

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.submit_form)
        buttons_layout.addWidget(submit_button)

        main_layout.addLayout(buttons_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def clear_form(self):
        """
        Clear the form inputs
        """
        for button in self.day_buttons.buttons():
            button.setAutoExclusive(False)
            button.setChecked(False)
            button.setAutoExclusive(True)

        self.time_input.clear()
        self.am_pm_dropdown.setCurrentIndex(0)
        self.reason_input.clear()

    def submit_form(self):
        """
        Submit the form inputs and save the appointment data to a CSV file
        """
        day = self.day_buttons.checkedId()
        if day == -1:
            return

        time = self.time_input.text().strip()
        try:
            # Split the time input into hours and minutes
            hours, minutes = time.split(':')
            hours = int(hours)
            minutes = int(minutes) if minutes else 0
            # Validate the hours and minutes
            if hours not in range(1, 13) or minutes not in range(0, 60):
                raise ValueError
        except ValueError:
            # Display a warning message for invalid time input
            QMessageBox.warning(self, "Invalid Time",
                                "Invalid input. Please enter a valid time (e.g. '1:00', '12:40').")
            return

        am_pm = self.am_pm_dropdown.currentText()
        reason = self.reason_input.toPlainText()

        date = self.calculate_date(day)
        date_str = date.strftime("%Y-%m-%d")
        day_str = date.strftime("%A")

        csv_file = "appointments.csv"

        if not os.path.exists(csv_file):
            with open(csv_file, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Date", "Day", "Time", "Reason"])

        with open(csv_file, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([date_str, day_str, f"{time} {am_pm}", reason])

        self.clear_form()

    def calculate_date(self, day):
        """
        Calculate the date of the next occurrence of the selected day of the week

        Args:
            day (int): The index of the selected day of the week (0-6)

        Returns:
            datetime.date: The date of the next occurrence of the selected day of the week
        """
        today = datetime.date.today()
        days_ahead = (day - today.weekday()) % 7
        return today + datetime.timedelta(days_ahead)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    appointment_reminder_app = AppointmentReminderApp()
    appointment_reminder_app.show()
    sys.exit(app.exec_())