#!/usr/bin/env python3
"""Find product source trees for this workspace. Only setup --clone-missing uses the network."""

import argparse
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


REDDIT = Path(__file__).resolve().parents[1]
WORKSPACE = REDDIT.parents[1]
LOCAL = REDDIT / ".local" / "repos"
REFERENCE = re.compile(r"^\[([\w.-]+)\]: https://github\.com/([\w.-]+/[\w.-]+)$", re.M)
# Earlier checkouts of these transferred projects still use their original GitHub owner.
TRANSFERRED = {"ArchUnitGo", "ArchUnitJava", "ArchUnitNET", "ArchUnitRuby", "ArchUnitRust", "ArchUnitZig"}


def registry():
    return dict(REFERENCE.findall((REDDIT / "products.md").read_text(encoding="utf-8")))


def checkout_names(product, slug):
    names = [slug.split("/")[1], product]
    if product == "ArchUnitPython":
        names.append("ArchUnitPy")
    return list(dict.fromkeys(names))


def matches(path, product, slug):
    if not (path / ".git").exists() or not (path / "README.md").is_file():
        return False
    # Read the stored URL, before any user-specific Git transport rewrites.
    result = subprocess.run(
        ["git", "-C", str(path), "config", "--local", "--get-regexp", r"^remote\.(origin|upstream)\.url$"],
        capture_output=True, text=True, check=False,
    )
    allowed = {slug.lower()}
    if product in TRANSFERRED:
        allowed.add(f"lukasniessen/{product.lower()}")
    for line in result.stdout.splitlines():
        url = line.partition(" ")[2].rstrip("/")
        identity = re.fullmatch(
            r"(?:https?://(?:[^/@]+@)?github\.com/|ssh://git@github\.com(?::\d+)?/|git@github\.com:)"
            r"([\w.-]+/[\w.-]+)", url, re.I,
        )
        if identity and identity[1].lower().removesuffix(".git") in allowed:
            return True
    return False


def discover(product, slug, roots):
    record = LOCAL / product
    candidates = []
    for root in roots:
        candidates.append(root)
        candidates.extend(root / name for name in checkout_names(product, slug))
    if record.is_file():
        candidates.append(Path(record.read_text(encoding="utf-8")))
    if product == "personal-website":
        candidates.append(WORKSPACE)
    candidates.extend(WORKSPACE.parent / name for name in checkout_names(product, slug))
    return next((p.resolve() for p in dict.fromkeys(candidates) if matches(p, product, slug)), None)


def store_path(product, path):
    LOCAL.mkdir(parents=True, exist_ok=True)
    destination = LOCAL / product
    if destination.is_file() and destination.read_text(encoding="utf-8") == str(path):
        return
    fd, temp_name = tempfile.mkstemp(dir=LOCAL)
    temporary = Path(temp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as output:
            output.write(str(path))
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)


def clone(product, slug, root):
    # Passing a checkout itself as --root locates it; new checkouts belong alongside it.
    parent = root.parent if (root / ".git").exists() else root
    ancestor = next((p for p in (parent, *parent.parents) if p.exists()), None)
    if ancestor is None:
        raise ValueError(f"Clone root is unavailable: {parent}")
    inside_repo = subprocess.run(
        ["git", "-C", str(ancestor), "rev-parse", "--show-toplevel"], capture_output=True,
    )
    if inside_repo.returncode == 0:
        raise ValueError(f"Choose a --root outside an existing Git working tree ({parent})")
    parent.mkdir(parents=True, exist_ok=True)
    path = parent / slug.split("/")[1]
    try:
        path.mkdir()
    except FileExistsError:
        raise ValueError(f"Occupied clone destination {path}. Choose another --root or point to the correct checkout.")
    try:
        subprocess.run(["git", "clone", "--", f"https://github.com/{slug}.git", str(path)], check=True)
        if not matches(path, product, slug):
            raise ValueError(f"Clone at {path} has no matching checkout and README.md")
    except BaseException:
        # Git normally cleans up a failed clone. Only discard the empty directory we reserved.
        try:
            path.rmdir()
        except OSError:
            pass
        raise
    return path


def main(argv=None):
    products = registry()
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    setup = sub.add_parser("setup", help="Discover and remember selected products (default: all)")
    setup.add_argument("products", nargs="*", metavar="PRODUCT", help=", ".join(products))
    setup.add_argument("--root", action="append", default=[], type=Path,
                       help="Look in this checkout or its immediate children; repeat for more locations")
    setup.add_argument("--clone-missing", action="store_true", help="Clone missing products into the first root")
    lookup = sub.add_parser("path", help="Print the verified absolute path for one product")
    lookup.add_argument("products", nargs=1, metavar="PRODUCT")
    args = parser.parse_args(argv)
    aliases = {name.casefold(): product for product, slug in products.items() for name in checkout_names(product, slug)}
    selected = []
    for name in args.products or products:
        if name.casefold() not in aliases:
            parser.error(f"Unknown product {name}. Choose from {', '.join(products)}.")
        selected.append(aliases[name.casefold()])
    roots = [p.expanduser().resolve() for p in getattr(args, "root", [])]
    failed = False
    for product in dict.fromkeys(selected):
        slug = products[product]
        try:
            path = discover(product, slug, roots)
            if path is None and getattr(args, "clone_missing", False):
                path = clone(product, slug, roots[0] if roots else WORKSPACE.parent)
            if path is None:
                raise ValueError(f"Missing checkout. Run repos.py setup {product} --root PATH or add --clone-missing.")
            if args.command == "path":
                print(path)
            else:
                store_path(product, path)
                print(f"{product}  {path}")
        except (OSError, ValueError, subprocess.CalledProcessError) as error:
            print(f"{product}: {error}", file=sys.stderr)
            failed = True
    return int(failed)


if __name__ == "__main__":
    sys.exit(main())
