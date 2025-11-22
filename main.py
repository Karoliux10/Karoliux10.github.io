# Gets championship contenders points
# Gets how many races are left
# Calculates how each driver can win the championship
# Displays the results in a GUI


from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QRadioButton
from PyQt5.QtCore import Qt
import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Championship Calculator")
        self.setGeometry(200, 200, 1300, 500)
        self.first_driver_input = QLineEdit("Norris", self)
        self.second_driver_input = QLineEdit("Piastri", self)
        self.third_driver_input = QLineEdit("Verstappen", self)
        self.first_points_input = QLineEdit("390", self)
        self.second_points_input = QLineEdit("366", self)
        self.third_points_input = QLineEdit("341", self)
        self.races_left_input = QLineEdit("3", self)
        self.sprints_left_input = QLineEdit("1", self)
        self.submit = QPushButton("Calculate", self)
        self.result_label = QLabel("", self)
        self.race_points_system = [25,18,15,12,10,8,6,4,2,1,0]
        self.sprint_points_system = [8,7,6,5,4,3,2,1,0]  
        self.is_sprint = QRadioButton("Sprint first", self)
        self.init_UI()

    def init_UI(self):

        self.first_driver_input.setFixedWidth(200)
        self.second_driver_input.setFixedWidth(200)
        self.third_driver_input.setFixedWidth(200)
        self.first_points_input.setFixedWidth(200)
        self.second_points_input.setFixedWidth(200)
        self.third_points_input.setFixedWidth(200)
        self.submit.setFixedWidth(200)

        layout = QVBoxLayout()

        first_layout = QHBoxLayout()
        first_layout.addWidget(QLabel("1st Place: "))
        first_layout.addWidget(self.first_driver_input)
        first_layout.addWidget(QLabel("Points: "))
        first_layout.addWidget(self.first_points_input)
        first_layout.addStretch()
        second_layout = QHBoxLayout()
        second_layout.addWidget(QLabel("2nd Place: "))
        second_layout.addWidget(self.second_driver_input)
        second_layout.addWidget(QLabel("Points: "))
        second_layout.addWidget(self.second_points_input)
        second_layout.addStretch()
        third_layout = QHBoxLayout()
        third_layout.addWidget(QLabel("3rd Place: "))
        third_layout.addWidget(self.third_driver_input)
        third_layout.addWidget(QLabel("Points: "))
        third_layout.addWidget(self.third_points_input)
        third_layout.addStretch()
        fourth_layout = QHBoxLayout()
        fourth_layout.addWidget(QLabel("Races Left: "))
        fourth_layout.addWidget(self.races_left_input)
        fourth_layout.addWidget(QLabel("Sprints Left: "))
        fourth_layout.addWidget(self.sprints_left_input)
        fourth_layout.addStretch()
        
        layout.addLayout(first_layout)
        layout.addLayout(second_layout)
        layout.addLayout(third_layout)
        layout.addLayout(fourth_layout)
        layout.addWidget(self.is_sprint)
        layout.addWidget(self.submit)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

        self.setStyleSheet("""
            QLineEdit {
                font-size: 24px;
                padding: 10px;
            }
        """)

        self.submit.clicked.connect(self.calculate_championship)

    def calculate_championship(self):       
        try:
            first_points = int(self.first_points_input.text())
            second_points = int(self.second_points_input.text())
            third_points = int(self.third_points_input.text())
            races_left = int(self.races_left_input.text())
            sprints_left = int(self.sprints_left_input.text()) 
        except ValueError:
            self.result_label.setText("Please enter valid integer points.")

        d1_in_contention = True
        d2_in_contention = True
        d3_in_contention = True

        d1 = self.first_driver_input.text()
        d2 = self.second_driver_input.text()
        d3 = self.third_driver_input.text()

        max_first_points = first_points + races_left * 25 + sprints_left * 8
        max_second_points = second_points + races_left * 25 + sprints_left * 8
        max_third_points = third_points + races_left * 25 + sprints_left * 8
        max_possible_points = races_left * 25 + sprints_left * 8

        if first_points > max_second_points:
            result = f"{d2} can no longer win the championship.\n"
            self.result_label.setText(result)
            d2_in_contention = False
            return
        if first_points > max_third_points:
            result = f"{d3} can no longer win the championship.\n"
            self.result_label.setText(result)
            d3_in_contention = False
        
        required_second = first_points - second_points + 1
        required_third = first_points - third_points + 1

        if d2_in_contention and d3_in_contention:
            situation_second = self.situation_calculator(required_second, max_possible_points, d1, d2)       
            situation_third = self.situation_calculator(required_third, max_possible_points, d1, d3)
            situation_second = situation_second if situation_second else ""
            situation_third = situation_third if situation_third else ""
            result = f"{d2} needs to outscore {d1} by {required_second} points to win the championship.\n{d3} needs to outscore {d1} by {required_third} points to win the championship.\n"
            self.result_label.setText(f"{result}\n{d1} wins the championship if:\n{situation_second}\n{d3} is no longer in contention if:\n{situation_third}")
        elif d2_in_contention:
            situation_third = f"\n{d3} can no longer win the championship.\n"
            situation_second = self.situation_calculator(required_second, max_possible_points, d1, d2)
            result = f"{d2} needs to outscore {d1} by {required_second} points to win the championship.\n"
            self.result_label.setText(f"{result}\n{d1} wins the championship if:\n{situation_second}{situation_third}")
        elif not d3_in_contention and not d2_in_contention:
            result = f"{d1} has won the championship!\n"
            self.result_label.setText(result)
    
    def situation_calculator(self, required_points, max_possible_points, d1, d2):
        situation = ""
        situations = []
        situation_display = ""
        if self.is_sprint.isChecked():
            for x in self.sprint_points_system:
                for y in self.sprint_points_system:
                    if max_possible_points - 8 < required_points+x-y:
                        if x > 0 and y > 0 and not x == y:
                            situation = f"{d1} finishes in p{self.sprint_points_system.index(x)+1} or higher and {d2} finishes in p{self.sprint_points_system.index(y)+1} or lower.\n"
                            situations.append(situation)
                            situation = ""
                            break
                        elif x > 0 and y == 0 and not x == y:
                            situation = f"{d1} finishes in p{self.sprint_points_system.index(x)+1} or higher and {d2} does not score.\n"
                            situations.append(situation)
                            situation = ""
                            break
                        elif y == 0 and x == 0 and not x == y:
                            situation = f"if {d1} and {d2} do not score.\n"
                            situations.append(situation)
                            situation = ""
                            break
        else:
            for x in self.race_points_system:
                for y in self.race_points_system:
                    if max_possible_points - 25 < required_points+x-y:
                        if x > 0 and y > 0 and not x == y:
                            situation = f"{d1} finishes in p{self.race_points_system.index(x)+1} or higher and {d2} finishes in p{self.race_points_system.index(y)+1} or lower.\n"
                            situations.append(situation)
                            situation = ""
                            break
                        elif x > 0 and y == 0 and not x == y:
                            situation = f"{d1} finishes in p{self.race_points_system.index(x)+1} or higher and {d2} does not score.\n"
                            situations.append(situation)
                            situation = ""
                            break
                        elif y == 0 and x == 0 and not x == y:
                            situation = f"if {d1} and {d2} do not score.\n"
                            situations.append(situation)
                            situation = ""
                            break
        
        for x in situations:
            situation_display += x

        return situation_display


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())