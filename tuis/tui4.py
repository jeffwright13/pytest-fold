import utils
import py_cui
from pathlib import Path

RESULTS_FILE = "pytest_fold/console_output.fold"

class ResultsData:
    def __init__(self, path: Path):
        self.results_file = path
        self.sections = []

    def get_results(self):
        with open(self.results_file, "r") as results_file:
            results_lines = results_file.readlines()
        self.sections = utils.sectionize(results_lines)



class TUI:
    results_data = ResultsData(RESULTS_FILE)
    results_data.get_results()

    root = py_cui.PyCUI(len(results_data.sections), 1)
    label = root.add_label('Label Text', 0, 0)
    # button = root.add_button('Button Text', 1, 2, column_span=2, command=None)
    root.start()

def main():
    resultsfile = Path.cwd() / RESULTS_FILE
    resultsdata = ResultsData(resultsfile)

    TUI()

if __name__ == "__main__":
    main()
