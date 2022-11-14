from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window

# Sets window size
Window.size = (500,700)

# Loads kivy file
Builder.load_file("design.kv")

# Class that handles all the logic
class MyLayout(Widget):
    # Variables used for storage
    operators = ["plus", "minus", "divide", "multiply"]
    cur_operator = ""
    pre_operator = ""
    value = ""
    error = ""
    total = 0

    # Fits to CE button
    def clear(self):
        self.ids.calc_dis.text = '0'
        self.total = 0
        self.ids.top_dis.text = "--"
        self.pre_operator = ""
        self.cur_operator = ""
        self.value = ""

    # Fits to C button
    def clear_line(self):
        self.ids.calc_dis.text = '0'
        self.value = ""

    # Used in all operators buttons function
    def operations(self, operation):
        if operation == "plus":
            self.total += float(self.ids.calc_dis.text)
            # To get clean formatted text
            self.ids.calc_dis.text = "{:.8f}".format((self.total)).rstrip("0").rstrip(".")

        elif operation == "minus":
            # Only subtracts to when total is more than zero to avoid runtime errors
            if self.total != 0:
                self.total -= float(self.ids.calc_dis.text)
            else:
                self.total += float(self.ids.calc_dis.text)
            self.ids.calc_dis.text = "{:.8f}".format((self.total)).rstrip("0").rstrip(".")

        elif operation == "multiply":
            # Same with these as mentioned above
            if self.total != 0:
                self.total *= float(self.ids.calc_dis.text)
            else:
                self.total += float(self.ids.calc_dis.text)
            self.ids.calc_dis.text = "{:.8f}".format((self.total)).rstrip("0").rstrip(".")
                
        elif operation == "divide":
            try:
                if self.total != 0:
                    self.total /= float(self.ids.calc_dis.text)
                else:
                    self.total += float(self.ids.calc_dis.text)
                self.ids.calc_dis.text = "{:.8f}".format((self.total)).rstrip("0").rstrip(".")
            except ZeroDivisionError:
                self.total = 0
                self.ids.calc_dis.text = "Syntax Error"

        self.ids.top_dis.text = "{:.8f}".format((self.total)).rstrip("0").rstrip(".")
        self.pre_operator = self.cur_operator
        self.value = ""

    # All the operators buttons
    def plus(self):
        self.cur_operator = self.operators[0]
        if self.pre_operator != "":
            self.operations(self.pre_operator)
        else:
            self.operations(self.operators[0])

    def minus(self):
        self.cur_operator = self.operators[1]
        if self.pre_operator != "":
            self.operations(self.pre_operator)
        else:
            self.operations(self.cur_operator)
            
    def multiply(self):
        self.cur_operator = self.operators[3]
        if self.pre_operator != "":
            self.operations(self.pre_operator)
        else:
            self.operations(self.cur_operator)

    def divide(self):
        self.cur_operator = self.operators[2]
        if self.pre_operator != "":
            self.operations(self.pre_operator)
        else:
            self.operations(self.cur_operator)

    def input(self, num):
        self.value += str(num)
        self.ids.calc_dis.text = self.value

    def input_point(self):
        if "." not in self.ids.calc_dis.text:
            self.value += self.ids.point.text
            self.ids.calc_dis.text = self.value

    # Used to calculate percentage
    def percentage(self):
        if self.cur_operator == "multiply" and "." not in self.ids.calc_dis.text:
            self.ids.calc_dis.text = str(float(self.ids.calc_dis.text) / 100)

    # Equal button
    def equal(self):

        self.operations(self.pre_operator)
        self.total = 0
        self.pre_operator = ""
        self.cur_operator = ""

    # so swap to the value - or +
    def get_abs(self):
        if "-" not in self.ids.calc_dis.text:
            self.ids.calc_dis.text = "-" + self.ids.calc_dis.text
        else:
            self.ids.calc_dis.text = self.ids.calc_dis.text.replace("-", "")

# Runs the main app
class CalculatorApp(App):
    def build(self):
        return MyLayout()

if __name__ == "__main__":
    CalculatorApp().run()

