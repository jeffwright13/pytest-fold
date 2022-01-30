import utils
import npyscreen
from pathlib import Path

RESULTS_FILE = "pytest_fold/console_output.fold"

class ResultsData:
    def __init__(self, path: Path = RESULTS_FILE):
        self.results_file = path
        self.sections = []

    def get_results(self):
        with open(self.results_file, "r") as results_file:
            results_lines = results_file.readlines()
        self.sections = utils.sectionize(results_lines)

# class TestApp(npyscreen.NPSApp):
#     def main(self):
#         results_data = ResultsData(RESULTS_FILE)
#         results_data.get_results()

#         F  = npyscreen.Form(name = "Pytest Results",)
#         test_title_box_1  = F.add(npyscreen.SimpleGrid, columns=1, rows=len(results_data.sections), name="TTB1:",)

#         # This lets the user interact with the Form.
#         F.edit()

        # print(ms.get_selected_objects())

# if __name__ == "__main__":
#     App = TestApp()
#     App.run()



class MyTestApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.registerForm("MAIN", MainForm())


class MainForm(npyscreen.Form):
    def create(self):
        self.results_data = ResultsData()
        self.results_data.get_results()
        self.add(npyscreen.Textfield, name = "Pytest Output")
        self.add(npyscreen.Textfield, values=self.results_data.sections[1])
        # for section in self.results_data.sections:
        #     self.add(npyscreen.Pager, values=section)


    def afterEditing(self):
        self.parentApp.setNextForm(None)


if __name__ == '__main__':
    test_app = MyTestApp()
    test_app.run()
