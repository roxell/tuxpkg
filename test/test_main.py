import pytest
import tuxpkg.__main__ as main_module


class TestMain:
    def test_calls_main(self, monkeypatch, mocker):
        monkeypatch.setattr(main_module, "__name__", "__main__")
        main = mocker.patch("tuxpkg.__main__.main", return_value=0)
        exit = mocker.patch("sys.exit")
        main_module.run()
        exit.assert_called_with(0)


    def test_main(self):
        assert main_module.main() == 0

