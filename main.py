import argparse
import os
from pathlib import Path
import sys

from staticjinja import Site


def get_context() -> dict[str, str]:
    context = {}
    prefix = "SJP_"
    for key in os.environ.keys():
        if key.startswith(prefix):
            context[key.removeprefix(prefix).lower()] = os.environ[key]
    return context


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render HTML pages from Jinja templates",
    )
    parser.add_argument(
        "-w",
        "--watch",
        help="Render the site, and re-render on changes to <srcpath>",
        action="store_true",
    )
    parser.add_argument(
        "--srcpath",
        help="The directory to look in for templates (defaults to './templates)'",
        default=Path(".") / "templates",
        type=Path,
    )
    parser.add_argument(
        "--outpath",
        help="The directory to place rendered files in (defaults to './build')",
        default=Path(".") / "build",
        type=Path,
    )

    args = parser.parse_args()

    src_path = args.srcpath
    output_path = args.outpath
    static_path = Path(src_path) / "assets"

    try:
        if not src_path.exists():
            print("Отсутствует папка templates, рендеринг невозможен", file=sys.stderr)
            sys.exit(1)
    except PermissionError:
        print("Нет доступа к папке templates, рендеринг невозможен", file=sys.stderr)
        sys.exit(2)

    try:
        if not any(src_path.glob("*.html")):
            print("Не найдено исходных файлов .html в папке templates, рендеринг невозможен", file=sys.stderr)
            sys.exit(3)
    except PermissionError:
        print("Нет доступа к листингу каталога templates, рендеринг невозможен", file=sys.stderr)
        sys.exit(4)

    html_files = list(src_path.glob("*.html"))
    for f in html_files:
        try:
            with open(f, "r", encoding="utf-8") as file: _ = file.read(1)
        except PermissionError:
            print(f"Нет доступа к файлу {f}, рендеринг невозможен", file=sys.stderr)
            sys.exit(5)

    site = Site.make_site(
        searchpath=src_path,
        outpath=output_path,
        staticpaths=[
            str(static_path),
        ],
        contexts=[(".*.html", get_context)],
    )

    site.render(use_reloader=args.watch)


if __name__ == '__main__':
    main()
