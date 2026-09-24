import os
import sys
from pathlib import Path


class TerminalUI:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    GREEN = "\033[92m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    WHITE = "\033[97m"

    def __init__(self, enabled=None):
        if enabled is None:
            enabled = sys.stdout.isatty() and not os.environ.get("NO_COLOR")
        self.enabled = bool(enabled)

    def _paint(self, text, *codes):
        if not self.enabled:
            return str(text)
        return "".join(codes) + str(text) + self.RESET

    def accent(self, text):
        return self._paint(text, self.BOLD, self.YELLOW)

    def heading(self, text):
        return self._paint(text, self.BOLD, self.WHITE)

    def success(self, text):
        return self._paint(text, self.GREEN)

    def info(self, text):
        return self._paint(text, self.CYAN)

    def warning(self, text):
        return self._paint(text, self.YELLOW)

    def error(self, text):
        return self._paint(text, self.RED)

    def dim(self, text):
        return self._paint(text, self.DIM)

    def rule(self, width=54):
        print(self.dim("─" * width))

    def header(self, version):
        print(f"{self.accent('Mifa')} {self.dim('v' + version)}")

    def banner(self, version):
        print()
        print(self.info("               .----------------------."))
        print(self.info("            .-'                        '-."))
        print(self.info("          .'") + self.accent("            M I F A") + self.info("           '."))
        print(self.info("         /                                  \\"))
        print(self.info("        |") + self.warning("               (  )") + self.info("                 |"))
        print(self.info("        |") + self.warning("              ( /\\ )") + self.info("                |"))
        print(self.info("        |") + self.warning("               \\__/") + self.info("                 |"))
        print(self.info("        |                                    |"))
        print(self.info("        |") + self.heading("    Windows Security Framework") + self.info("      |"))
        print(self.info("        |") + self.dim(f"               v{version}") + self.info("               |"))
        print(self.info("         \\                                  /"))
        print(self.info("          '.                              .'"))
        print(self.info("            '-.________________________.-'"))
        print()

def read_version(root):
    path = Path(root) / "VERSION"
    if not path.is_file():
        return "unknown"
    return path.read_text(encoding="utf-8").strip()
