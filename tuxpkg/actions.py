import os
from pathlib import Path


class Action:
    def __init__(self, target: str):
        self.target = target
        self.target_path = Path(__file__).parent / "data" / self.target

    def __call__(self) -> None:
        pass


class PointToFile(Action):
    def __call__(self) -> None:
        print(self.target_path)


get_makefile = PointToFile("tuxpkg.mk")
get_debian_rules = PointToFile("debianrules.mk")


class RunScript(Action):
    def __call__(self) -> None:
        os.execv(str(self.target_path), [self.target])


create_repository = RunScript("create-repository")
release = RunScript("release")
