import argparse
import sys
import tuxpkg
import tuxpkg.get_makefile
import tuxpkg.get_debian_rules
import tuxpkg.create_repository
import tuxpkg.release


def main():
    parser = argparse.ArgumentParser(
        prog="tuxpkg",
        description=tuxpkg.__doc__.strip(),
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {tuxpkg.__version__}",
    )
    parser.set_defaults(func=parser.print_usage)

    subparsers = parser.add_subparsers(
        title="Subcommands",
        description="All tuxpkg is available through one of its subcommands.",
    )

    get_makefile = subparsers.add_parser(
        "get-makefile",
        aliases=["mk"],
        help="Prints the path to the tuxpkg shared makefile. It can be included in a Makefile using a construct like like `$(include $(shell tuxpkg get-makefile))`.",
    )
    get_makefile.set_defaults(func=tuxpkg.get_makefile.run)

    get_debian_rules = subparsers.add_parser(
        "get-debian-rules",
        help="Prints the path to the tuxpkg shared debian/rules. It can be included in a your debian/rules using a construct like like `$(include $(shell tuxpkg get-makefile))`. You just need to set PYBUILD_NAME first.",
    )
    get_debian_rules.set_defaults(func=tuxpkg.get_debian_rules.run)

    create_repository = subparsers.add_parser(
        "create-repository",
        aliases=["repo"],
        help="Creates Debian and RPM repository from files in dist/."
    )
    create_repository.set_defaults(func=tuxpkg.create_repository.run)

    release = subparsers.add_parser(
        "release",
        help="Makes a release"
    )
    release.set_defaults(func=tuxpkg.release.run)

    options = parser.parse_args(sys.argv[1:])
    options.func()

    return 0


def run() -> None:
    if __name__ == "__main__":
        sys.exit(main())


run()
