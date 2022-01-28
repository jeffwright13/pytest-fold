import pytest
import sys
import subprocess


class FoldPlugin:
    def pytest_sessionfinish(self):
        # subprocess.run(f"python {Path.cwd()}/tui.py")
        subprocess.run(["python", "/Users/jwr003/coding/pytest-fold/tui_asciimatics.py"])


if __name__ == "__main__":
    sys.exit(pytest.main(["-vv", "--fold"], plugins=[FoldPlugin()]))
