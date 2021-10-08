from pathlib import Path
from tuxpkg.actions import Action
from tuxpkg.actions import PointToFile
from tuxpkg.actions import RunScript


class TestAction:
    def test_is_callable(self):
        action = Action("foobar")
        action()


class TestPointToFile:
    def test_shows_content(self, capsys):
        action = PointToFile("tuxpkg.mk")
        action()
        out, _ = capsys.readouterr()
        file = Path(out.strip())
        assert file.exists


class TestRunScript:
    def test_runs_script(self, mocker):
        execv = mocker.patch("os.execv")
        run_script = RunScript("create-repository")
        run_script()
        execv.assert_called()
        script_path = Path(execv.call_args[0][0])
        assert script_path.name == "create-repository"
        assert script_path.exists()
        assert type(execv.call_args[0][1]) in [list, tuple]
