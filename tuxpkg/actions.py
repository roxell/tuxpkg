from datetime import datetime
import os
import subprocess
from jinja2 import Template
from pathlib import Path
import shutil

# Global variables to store init command options
init_platform: str = "auto"
init_force: bool = False


def detect_platform() -> str:
    try:
        result = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            capture_output=True,
            text=True,
            check=True,
        )
    except FileNotFoundError:
        raise RuntimeError("git is not installed")
    except subprocess.CalledProcessError:
        raise RuntimeError(
            "Failed to detect platform: no git remote configured. "
            "Use --platform to specify github or gitlab."
        )
    remote_url = result.stdout.strip()
    if "github.com" in remote_url:
        return "github"
    return "gitlab"


class Action:
    def __call__(self) -> None:
        pass


class FileAction(Action):
    def __init__(self, source: str):
        self.source = source
        self.source_path = Path(__file__).parent / "data" / self.source


class PointToFile(FileAction):
    def __call__(self) -> None:
        print(self.source_path)


get_makefile = PointToFile("tuxpkg.mk")
get_debian_rules = PointToFile("debianrules.mk")


class RunScript(FileAction):
    def __call__(self) -> None:
        if init_force:
            os.environ["TUXPKG_FORCE"] = "1"
        os.execv(str(self.source_path), [self.source])


create_repository = RunScript("create-repository")
check_repository_key = RunScript("check-repository-key")
release = RunScript("release")


class CopyDirectory(FileAction):
    def __init__(self, source: str):
        super().__init__(source)
        self.variables = {
            "project": Path(".").absolute().name,
            "module": Path(".").absolute().name.replace("-", "_"),
            "timestamp": datetime.utcnow(),
        }

    def __call__(self) -> None:
        if init_platform == "auto":
            self.platform = detect_platform()
        else:
            self.platform = init_platform

        cwd = os.getcwd()
        os.chdir(self.source_path)
        try:
            root = Path(".")
            self.copy(root, Path(cwd).absolute())
        finally:
            os.chdir(cwd)

    def should_skip_for_platform(self, source: Path) -> bool:
        source_str = str(source)
        if self.platform == "github":
            if ".gitlab-ci.yml" in source_str:
                return True
        else:
            if ".github" in source_str:
                return True
        return False

    def copy(self, source: Path, target: Path) -> None:
        if self.should_skip_for_platform(source):
            return

        if source.is_dir():
            (target / self.render(str(source))).mkdir(exist_ok=True)
            for child in source.iterdir():
                self.copy(child, target)
        else:
            if source.name.endswith(".jinja2"):
                self.expand_template(source, target)
            else:
                self.copy_file(source, target)

    def expand_template(self, source: Path, target: Path) -> None:
        destname = self.render(str(source.with_suffix("")))
        dest = target / destname
        if dest.exists() and not init_force:
            print(f"  SKIP {destname} (already exists)")
            return
        action = "UPDATE" if dest.exists() else "CREATE"
        dest.write_text(self.render(source.read_text()))
        dest.chmod(source.stat().st_mode)
        print(f"{action} {destname}")

    def copy_file(self, source: Path, target: Path) -> None:
        destname = self.render(str(source))
        dest = target / destname
        if dest.exists() and not init_force:
            print(f"  SKIP {destname} (already exists)")
            return
        action = "UPDATE" if dest.exists() else "CREATE"
        shutil.copyfile(str(source), str(dest))
        print(f"{action} {destname}")

    def render(self, template_text: str) -> str:
        template = Template(template_text)
        return template.render(**self.variables)


class CompositeAction(Action):
    def __init__(self, *actions):
        self.actions = actions

    def __call__(self):
        for action in self.actions:
            action()


init = CompositeAction(CopyDirectory("init"), RunScript("init.sh"))
