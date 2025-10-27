import sys
import threading
import time

# ANSI colors (256-color orange ~208)
ORANGE = "\033[38;5;208m"
GREEN = "\033[32m"
RED = "\033[31m"
DIM = "\033[2m"
BOLD = "\033[1m"
RESET = "\033[0m"

FRAMES = [
    "⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"
]


class Spinner:
    """Lightweight terminal spinner with Kurama orange aesthetics.

    Usage:
        s = Spinner("Running wiki_search…")
        s.start()
        try:
            ... work ...
            s.stop(success=True)
        except Exception:
            s.stop(success=False)
            raise
    """

    def __init__(self, text: str, icon: str = "🦊 Kurama | "):
        self.text = text
        self.icon = icon
        self._stop = threading.Event()
        self._thread = None
        self._idx = 0
        self._start_time = None

    def _render(self):
        while not self._stop.is_set():
            frame = FRAMES[self._idx % len(FRAMES)]
            self._idx += 1
            line = f"\r{ORANGE}{self.icon}{RESET}{BOLD}{self.text}{RESET} {DIM}{frame}{RESET}"
            sys.stdout.write(line)
            sys.stdout.flush()
            time.sleep(0.08)

    def start(self):
        self._start_time = time.time()
        self._thread = threading.Thread(target=self._render, daemon=True)
        self._thread.start()

    def stop(self, success: bool = True):
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=0.2)
        elapsed = 0.0
        if self._start_time is not None:
            elapsed = time.time() - self._start_time
        status_icon = f"{GREEN}✓{RESET}" if success else f"{RED}✗{RESET}"
        # clear spinner line and print final status
        sys.stdout.write(
            f"\r{ORANGE}{self.icon}{RESET}{BOLD}{self.text}{RESET} {status_icon} {DIM}({elapsed:.1f}s)\n{RESET}"
        )
        sys.stdout.flush()


def run_with_spinner(label: str, fn, *args, **kwargs):
    """Helper to run a callable with spinner and return its result.

    Catches exceptions, stops spinner with failure, and re-raises.
    """
    s = Spinner(f"{label}")
    s.start()
    try:
        res = fn(*args, **kwargs)
        s.stop(success=True)
        return res
    except Exception:
        s.stop(success=False)
        raise
