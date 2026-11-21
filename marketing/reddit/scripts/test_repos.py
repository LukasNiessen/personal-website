import contextlib
import io
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import repos


class RepoSetupTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name).resolve()
        self.workspace = self.base / "team" / "website"
        self.workspace.mkdir(parents=True)
        self.mapping = self.workspace / ".local" / "repos"
        patches = [
            patch.object(repos, "WORKSPACE", self.workspace),
            patch.object(repos, "LOCAL", self.mapping),
            patch.dict(os.environ, GIT_CONFIG_GLOBAL=str(self.base / "gitconfig"),
                       GIT_CONFIG_NOSYSTEM="1", GIT_ALLOW_PROTOCOL="file"),
        ]
        for mocked in patches:
            mocked.start()
            self.addCleanup(mocked.stop)

    def checkout(self, path, origin):
        path.mkdir(parents=True)
        subprocess.run(["git", "init", "-q", str(path)], check=True)
        subprocess.run(["git", "-C", str(path), "remote", "add", "origin", origin], check=True)
        (path / "README.md").write_text("demo\n")
        return path

    def invoke(self, *args):
        output, error = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
            status = repos.main(args)
        return status, output.getvalue().strip(), error.getvalue().strip()

    def test_sibling_alias_and_renamed_checkouts(self):
        python = self.checkout(self.workspace.parent / "ArchUnitPy", "git@github.com:LukasNiessen/ArchUnitPython.git")
        self.assertEqual(self.invoke("path", "archunitpython"), (0, str(python), ""))
        self.assertFalse(self.mapping.exists())
        rust = self.checkout(self.base / "renamed rust", "ssh://git@github.com/LukasNiessen/ArchUnitRust.git")
        self.assertEqual(self.invoke("setup", "ArchUnitRust", "--root", str(rust))[0], 0)
        self.assertEqual(self.invoke("path", "ArchUnitRust"), (0, str(rust), ""))
        self.assertEqual(self.invoke("setup", "ArchUnitPy")[0], 0)
        self.assertEqual((self.mapping / "ArchUnitRust").read_text(), str(rust))

        subprocess.run(["git", "-C", str(rust), "remote", "set-url", "origin",
                        "https://github.com/unrelated/ArchUnitRust.git"], check=True)
        self.assertNotEqual(self.invoke("path", "ArchUnitRust")[0], 0)
        subprocess.run(["git", "-C", str(rust), "remote", "add", "upstream",
                        "https://github.com/dragonsec-ai/ArchUnitRust"], check=True)
        self.assertEqual(self.invoke("path", "ArchUnitRust"), (0, str(rust), ""))

    def test_occupied_destination_is_preserved(self):
        occupied = self.checkout(self.base / "repos" / "ArchUnitTS", "https://github.com/unrelated/ArchUnitTS")
        result, _, error = self.invoke("setup", "ArchUnitTS", "--root", str(occupied.parent), "--clone-missing")
        self.assertNotEqual(result, 0)
        self.assertIn("Occupied", error)
        self.assertEqual((occupied / "README.md").read_text(), "demo\n")
        self.assertFalse(self.mapping.exists())

    def test_missing_repo_is_optional_until_selected(self):
        root = self.base / "repos"
        python = self.checkout(root / "ArchUnitPython", "https://github.com/LukasNiessen/ArchUnitPython")
        result, _, error = self.invoke("setup", "ArchUnitTS", "ArchUnitPython", "--root", str(root))
        self.assertNotEqual(result, 0)
        self.assertIn("Missing checkout", error)
        self.assertEqual(self.invoke("path", "ArchUnitPython"), (0, str(python), ""))
        self.assertFalse((root / "ArchUnitTS").exists())

    def test_never_nests_a_clone_in_a_working_tree(self):
        self.checkout(self.base / "existing repository", "https://github.com/example/project")
        nested = self.base / "existing repository" / "new directory"
        result, _, error = self.invoke("setup", "ArchUnitTS", "--root", str(nested), "--clone-missing")
        self.assertNotEqual(result, 0)
        self.assertIn("outside an existing Git", error)
        self.assertFalse(nested.exists())

    def test_unavailable_volume(self):
        with patch.object(Path, "exists", return_value=False):
            with self.assertRaisesRegex(ValueError, "Clone root is unavailable"):
                repos.clone("ArchUnitTS", "LukasNiessen/ArchUnitTS", self.base / "offline volume")

    def test_offline_clone_retry_and_reuse(self):
        # Git can use only file:// transports in this test, even if a mapping is wrong.
        origin = "https://github.com/dragonsec-ai/ArchUnitZig.git"
        seed = self.checkout(self.base / "source repository", origin)
        subprocess.run(["git", "-C", str(seed), "add", "README.md"], check=True)
        subprocess.run(["git", "-C", str(seed), "-c", "user.email=fixture@example.invalid",
                        "-c", "user.name=Fixture", "-c", "commit.gpgsign=false", "commit", "-qm", "Seed"], check=True)
        root = self.base / "my repositories"
        root.mkdir()
        entry = self.checkout(root / "typescript", "https://github.com/LukasNiessen/ArchUnitTS")
        args = ["setup", "ArchUnitZig", "--root", str(entry), "--clone-missing"]
        self.assertNotEqual(self.invoke(*args)[0], 0)
        checkout = root / "ArchUnitZig"
        self.assertFalse(checkout.exists())
        subprocess.run(["git", "config", "--global", f"url.{seed.as_uri()}.insteadOf", origin], check=True)
        self.assertEqual(self.invoke(*args)[0], 0)
        self.assertEqual(self.invoke("path", "ArchUnitZig"), (0, str(checkout), ""))
        (checkout / "README.md").write_text("my uncommitted edits\n")
        self.assertEqual(self.invoke(*args)[0], 0)
        self.assertEqual((checkout / "README.md").read_text(), "my uncommitted edits\n")


if __name__ == "__main__":
    unittest.main()
