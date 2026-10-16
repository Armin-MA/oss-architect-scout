"""CLI presentation controller and application entrypoint for OSS Architect Scout."""
from __future__ import annotations

import argparse
import sys
from typing import List, Optional, TextIO

from src.config.settings import Settings
from src.core.container import Container


def create_parser() -> argparse.ArgumentParser:
    """Construct command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="oss-architect-scout",
        description="Autonomous Scout evaluating OSS repositories against host architecture.",
    )
    parser.add_argument(
        "-q",
        "--query",
        type=str,
        required=True,
        help="Search query to discover candidate repositories on GitHub",
    )
    parser.add_argument(
        "-p",
        "--path",
        dest="project_path",
        type=str,
        default=".",
        help="Path to host project directory (default: current directory)",
    )
    parser.add_argument(
        "--allow-copyleft",
        action="store_true",
        default=False,
        help="Permit copyleft viral licenses (e.g. GPL, AGPL) with warnings instead of hard veto",
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["scout", "history"],
        default="scout",
        help="Execution mode: 'scout' (default) or 'history'",
    )
    return parser


class CLIController:
    """Presentation controller coordinating CLI input, orchestrator execution, and output."""

    def __init__(
        self,
        container: Optional[Container] = None,
        stdout: Optional[TextIO] = None,
        stderr: Optional[TextIO] = None,
    ) -> None:
        """Initialize controller with optional container and output streams.

        Args:
            container: IoC Container instance. Defaults to a new Container().
            stdout: Output stream for reports (defaults to sys.stdout).
            stderr: Error stream for error messages (defaults to sys.stderr).
        """
        self.container = container
        self.stdout: TextIO = stdout if stdout is not None else sys.stdout
        self.stderr: TextIO = stderr if stderr is not None else sys.stderr

    def run(self, argv: Optional[List[str]] = None) -> int:
        """Parse CLI arguments, execute workflow, and print output.

        Args:
            argv: Optional list of argument strings. Defaults to sys.argv[1:].

        Returns:
            Exit code integer (0 on success, non-zero on failure).
        """
        parser = create_parser()
        try:
            parsed = parser.parse_args(argv if argv is not None else sys.argv[1:])
        except SystemExit as exc:
            # Propagate exit code from argparse (e.g. --help or syntax error)
            return int(exc.code) if isinstance(exc.code, int) else 2

        if not parsed.query or not parsed.query.strip():
            self.stderr.write("Error: --query argument cannot be empty.\n")
            return 1

        active_container = self.container if self.container is not None else Container()

        try:
            if parsed.mode == "history":
                return self._handle_history(active_container)

            return self._handle_scout(
                container=active_container,
                query=parsed.query.strip(),
                project_path=parsed.project_path,
                allow_copyleft=parsed.allow_copyleft,
            )
        except Exception as exc:
            self.stderr.write(f"Scout execution failed: {exc}\n")
            return 1

    def _handle_scout(
        self,
        container: Container,
        query: str,
        project_path: str,
        allow_copyleft: bool,
    ) -> int:
        """Execute scout workflow and print markdown report to stdout."""
        orchestrator = container.create_orchestrator()
        result = orchestrator.scout(
            query=query,
            project_path=project_path,
            allow_copyleft=allow_copyleft,
        )

        report = result.report if hasattr(result, "report") else str(result[0])
        try:
            self.stdout.write(report + "\n")
        except UnicodeEncodeError:
            clean_text = report.encode(getattr(self.stdout, "encoding", "ascii") or "ascii", errors="replace").decode(getattr(self.stdout, "encoding", "ascii") or "ascii")
            self.stdout.write(clean_text + "\n")
        return 0

    def _handle_history(self, container: Container) -> int:
        """Fetch past evaluation history and print summary."""
        records = container.repository.get_evaluation_history(limit=10)
        if not records:
            self.stdout.write("No previous evaluation history found.\n")
            return 0

        self.stdout.write("# Past Evaluation History\n\n")
        for rec in records:
            repo_name = getattr(rec, "repo_full_name", "unknown")
            score = getattr(rec, "final_score", 0.0)
            self.stdout.write(f"- {repo_name}: Score {score:.1f}\n")
        return 0


def main(argv: Optional[List[str]] = None) -> int:
    """CLI application entrypoint returning process exit code."""
    controller = CLIController()
    return controller.run(argv)


if __name__ == "__main__":
    sys.exit(main())
