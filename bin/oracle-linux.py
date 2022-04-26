#!/usr/bin/env python3

import pyquery
import re
import repomd
import sys


def parse_release_page(release: str):
    site = "https://yum.oracle.com"
    release_page = pyquery.PyQuery(f"{site}/oracle-{release}.html")

    headers = [""]
    rows = []

    for repo in release_page("h3"):
        if not repo.text:
            print(
                "ignore", release, "->",
                repo.text_content(), file=sys.stderr)
            continue
        repo_name = repo.text.strip()

        columns = {}
        for arch in repo.getchildren():
            arch_name = arch.text.strip()
            url = arch.get("href", "")

            if not re.fullmatch("/repo/.+/index.html", url):
                print(
                    "ignore", release, "->",
                    repo_name, arch_name, url, file=sys.stderr)
                continue

            arch_name = arch_name.lower()
            if arch_name not in headers:
                headers.append(arch_name)

            url = url.rstrip("index.html")
            packages = repomd.load(site + url)
            columns[arch_name] = "{:,.2f} GiB ({:,})".format(
                sum(p.package_size for p in packages) / (1 << 30),
                len(packages))

        if not columns:
            continue

        columns[""] = repo_name
        rows.append(columns)

    release_name = release_page("h1").text().strip()
    print_markdown(release_name, headers, rows)


def print_markdown(release_name: str, headers: list, rows: list):
    print("###", release_name)
    print_table_row(headers)
    print("|-" * len(headers), end="|\n")
    for r in rows:
        print_table_row(r.get(c, "") for c in headers)


def print_table_row(row):
    print(end="| ")
    print(*row, sep=" | ", end=" |\n")


if __name__ == "__main__":
    for release in [f"linux-{i}" for i in range(4, 9)] + ["vm-3"]:
        parse_release_page(release)
