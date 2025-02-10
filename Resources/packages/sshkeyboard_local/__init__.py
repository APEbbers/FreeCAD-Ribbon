"""sshkeyboard"""

__version__ = "2.3.1"

import asyncio
import concurrent.futures
import os
import sys
import traceback
from contextlib import contextmanager
from inspect import signature
from platform import system
from time import time
from types import SimpleNamespace
from typing import Any, Callable, Optional

try:
    from ._asyncio_run_backport_36 import run36
except ImportError:  # this allows local testing: python __init__.py
    from _asyncio_run_backport_36 import run36

_is_windows = system().lower() == "windows"

if _is_windows:
    import msvcrt
else:
    import fcntl
    import termios
    import tty


# Global state

# Makes sure only listener can be started at a time
_running = False
# Makes sure listener stops if error has been raised
# inside thread pool executor or asyncio task or
# stop_listening() has been called
_should_run = False

# Readable representations for selected ansi characters
# All possible ansi characters here:
# https://github.com/prompt-toolkit/python-prompt-toolkit/blob/master/prompt_toolkit/input/ansi_escape_sequences.py
# Listener does not support modifier keys for now
_UNIX_ANSI_CHAR_TO_READABLE = {
    # 'Regular' characters
    "\x1b": "esc",
    "\x7f": "backspace",
    "\x1b[2~": "insert",
    "\x1b[3~": "delete",
    "\x1b[5~": "pageup",
    "\x1b[6~": "pagedown",
    "\x1b[H": "home",
    "\x1b[F": "end",
    "\x1b[A": "up",
    "\x1b[B": "down",
    "\x1b[C": "right",
    "\x1b[D": "left",
    "\x1bOP": "f1",
    "\x1bOQ": "f2",
    "\x1bOR": "f3",
    "\x1bOS": "f4",
    "\x1b[15~": "f5",
    "\x1b[17~": "f6",
    "\x1b[18~": "f7",
    "\x1b[19~": "f8",
    "\x1b[20~": "f9",
    "\x1b[21~": "f10",
    "\x1b[23~": "f11",
    "\x1b[24~": "f12",
    "\x1b[25~": "f13",
    "\x1b[26~": "f14",
    "\x1b[28~": "f15",
    "\x1b[29~": "f16",
    "\x1b[31~": "f17",
    "\x1b[32~": "f18",
    "\x1b[33~": "f19",
    "\x1b[34~": "f20",
    # Special/duplicate:
    # Tmux, Emacs
    "\x1bOH": "home",
    "\x1bOF": "end",
    "\x1bOA": "up",
    "\x1bOB": "down",
    "\x1bOC": "right",
    "\x1bOD": "left",
    # Rrvt
    "\x1b[1~": "home",
    "\x1b[4~": "end",
    "\x1b[11~": "f1",
    "\x1b[12~": "f2",
    "\x1b[13~": "f3",
    "\x1b[14~": "f4",
    # Linux console
    "\x1b[[A": "f1",
    "\x1b[[B": "f2",
    "\x1b[[C": "f3",
    "\x1b[[D": "f4",
    "\x1b[[E": "f5",
    # Xterm
    "\x1b[1;2P": "f13",
    "\x1b[1;2Q": "f14",
    "\x1b[1;2S": "f16",
    "\x1b[15;2~": "f17",
    "\x1b[17;2~": "f18",
    "\x1b[18;2~": "f19",
    "\x1b[19;2~": "f20",
    "\x1b[20;2~": "f21",
    "\x1b[21;2~": "f22",
    "\x1b[23;2~": "f23",
    "\x1b[24;2~": "f24",
}

_WIN_CHAR_TO_READABLE = {
    "\x1b": "esc",
    "\x08": "backspace",
    "àR": "insert",
    "àS": "delete",
    "àI": "pageup",
    "àQ": "pagedown",
    "àG": "home",
    "àO": "end",
    "àH": "up",
    "àP": "down",
    "àM": "right",
    "àK": "left",
    "\x00H": "up",
    "\x00P": "down",
    "\x00M": "right",
    "\x00K": "left",
    "\x00;": "f1",
    "\x00<": "f2",
    "\x00=": "f3",
    "\x00>": "f4",
    "\x00?": "f5",
    "\x00@": "f6",
    "\x00A": "f7",
    "\x00B": "f8",
    "\x00C": "f9",
    "\x00D": "f10",
    # "": "f11", ?
    "à†": "f12",
}

# Some non-ansi characters that need a readable representation
_CHAR_TO_READABLE = {
    "\t": "tab",
    "\n": "enter",
    "\r": "enter",
    " ": "space",
}

_WIN_SPECIAL_CHAR_STARTS = {"\x1b", "\x08", "\x00", "\xe0"}
_WIN_REQUIRES_TWO_READS_STARTS = {"\x00", "\xe0"}


def listen_keyboard(
    on_press: Optional[Callable[[str], Any]] = None,
    on_release: Optional[Callable[[str], Any]] = None,
    until: Optional[str] = "esc",
    sequential: bool = False,
    delay_second_char: float = 0.75,
    delay_other_chars: float = 0.05,
    lower: bool = True,
    debug: bool = False,
    max_thread_pool_workers: Optional[int] = None,
    sleep: float = 0.01,
) -> None:
    """Listen for keyboard events and fire `on_press` and `on_release` callback
    functions

    Supports asynchronous callbacks also.

    Blocks the thread until the key in `until` parameter has been pressed, an
    error has been raised or :func:`~sshkeyboard.stop_listening` has been
    called.

    Simple example with asynchronous and regular callbacks:

    .. code-block:: python

        from sshkeyboard import listen_keyboard

        async def press(key):
            print(f"'{key}' pressed")

        def release(key):
            print(f"'{key}' released")

        listen_keyboard(
            on_press=press,
            on_release=release,
        )

    Args:
        on_press: Function that gets called when a key is pressed. The
            function takes the pressed key as parameter. Defaults to None.
        on_release: Function that gets called when a key is released. The
            function takes the released key as parameter. Defaults to None.
        until: A key that will end keyboard listening. None means that
            listening will stop only when :func:`~sshkeyboard.stop_listening`
            has been called or an error has been raised. Defaults to "esc".
        sequential: If enabled, callbacks will be forced to happen one by
            one instead of concurrently or asynchronously. Defaults to False.
        delay_second_char: The timeout between first and second character when
            holding down a key. Depends on terminal and is used for parsing
            the input. Defaults to 0.75.
        delay_other_chars: The timeout between all other characters when
            holding down a key. Depends on terminal and is used for parsing
            the input. Defaults to 0.05.
        lower: If enabled, the callback 'key' parameter gets turned into lower
            case key even if it was upper case, for example "A" -> "a".
            Defaults to True.
        debug: Print debug messages. Defaults to False.
        max_thread_pool_workers: Define the number of workers in
            ThreadPoolExecutor, None means that a default value will get used.
            Will get ignored if sequential=True. Defaults to None.
        sleep: asyncio.sleep() amount between attempted keyboard input reads.
            Defaults to 0.01.
    """

    coro = listen_keyboard_manual(
        on_press,
        on_release,
        until,
        sequential,
        delay_second_char,
        delay_other_chars,
        lower,
        debug,
        max_thread_pool_workers,
        sleep,
    )

    if _is_python_36():
        run36(coro)
    else:
        asyncio.run(coro)


async def listen_keyboard_manual(
    on_press: Optional[Callable[[str], Any]] = None,
    on_release: Optional[Callable[[str], Any]] = None,
    until: Optional[str] = "esc",
    sequential: bool = False,
    delay_second_char: float = 0.75,
    delay_other_chars: float = 0.05,
    lower: bool = True,
    debug: bool = False,
    max_thread_pool_workers: Optional[int] = None,
    sleep: float = 0.01,
) -> None:
    """The same as :func:`~sshkeyboard.listen_keyboard`, but now the
    awaiting must be handled by the caller

    .. code-block:: python

        from sshkeyboard import listen_keyboard_manual
        # ...
        asyncio.run(listen_keyboard_manual(...))

    is the same as

    .. code-block:: python

        from sshkeyboard import listen_keyboard
        # ...
        listen_keyboard(...)

    (Python version 3.6 which does not have `asyncio.run` is handled
    differently internally)

    Has the same parameters as :func:`~sshkeyboard.listen_keyboard`
    """

    global _running
    global _should_run
    # Check the system
    assert sys.version_info >= (3, 6), (
        "sshkeyboard requires Python version 3.6+, you have "
        f"{sys.version_info.major}.{sys.version_info.minor}"
    )
    # Check the state
    assert not _running, "Only one listener allowed at a time"
    assert not _should_run, "Should have ended listening properly the last time"
    # Check the parameters
    assert (
        on_press is not None or on_release is not None
    ), "Either on_press or on_release should be defined"
    _check_callback_ok(on_press, "on_press")
    _check_callback_ok(on_release, "on_release")
    assert until is None or isinstance(until, str), "'until' has to be a string or None"
    assert isinstance(sequential, bool), "'sequential' has to be boolean"
    assert isinstance(
        delay_second_char, (int, float)
    ), "'delay_second_char' has to be numeric"
    assert isinstance(
        delay_other_chars, (int, float)
    ), "'delay_other_chars' has to be numeric"
    assert isinstance(lower, bool), "'lower' has to be boolean"
    assert isinstance(debug, bool), "'debug' has to be boolean"
    assert max_thread_pool_workers is None or isinstance(
        max_thread_pool_workers, int
    ), "'max_thread_pool_workers' has to be None or int"
    assert isinstance(sleep, (int, float)), "'sleep' has to numeric"

    _running = True
    _should_run = True

    # Create thread pool executor only if it will get used
    executor = None
    if not sequential and (
        not asyncio.iscoroutinefunction(on_press)
        or not asyncio.iscoroutinefunction(on_release)
    ):
        executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=max_thread_pool_workers
        )

    # Package parameters into namespaces so they are easier to pass around
    # Options do not change
    options = SimpleNamespace(
        on_press_callback=_callback(on_press, sequential, executor),
        on_release_callback=_callback(on_release, sequential, executor),
        until=until,
        sequential=sequential,
        delay_second_char=delay_second_char,
        delay_other_chars=delay_other_chars,
        lower=lower,
        debug=debug,
        sleep=sleep,
    )
    # State does change
    state = SimpleNamespace(
        press_time=time(),
        initial_press_time=time(),
        previous="",
        current="",
    )

    # Listen
    with _raw(sys.stdin), _nonblocking(sys.stdin):
        while _should_run:
            state = await _react_to_input(state, options)
            await asyncio.sleep(sleep)

    # Cleanup
    if executor is not None:
        executor.shutdown()
    _running = False
    _should_run = False


def stop_listening() -> None:
    """Stops the ongoing keyboard listeners

    Can be called inside the callbacks or from outside. Does not do anything
    if listener is not running.

    Example to stop after some condition is met, ("z" pressed in this case):

    .. code-block:: python

        from sshkeyboard import listen_keyboard, stop_listening

        def press(key):
            print(f"'{key}' pressed")
            if key == "z":
                stop_listening()

        listen_keyboard(on_press=press)
    """
    if _running:
        global _should_run
        _should_run = False


def _is_python_36():
    return sys.version_info.major == 3 and sys.version_info.minor == 6


def _check_callback_ok(function, name):
    if function is not None:
        assert callable(function), f"{name} must be None or callable"
        assert _takes_at_least_one_param(
            function
        ), f"{name} must take at least one parameter"
        assert _max_one_param_without_default(function), (
            f"{name} must have one or zero parameters without a default "
            f"value, now takes more: {_default_empty_params(function)}"
        )


def _takes_at_least_one_param(function):
    sig = signature(function)
    return len(sig.parameters.values()) >= 1


def _default_empty_params(function):
    sig = signature(function)
    return tuple(
        param.name
        for param in sig.parameters.values()
        if (param.kind == param.POSITIONAL_OR_KEYWORD and param.default is param.empty)
    )


def _max_one_param_without_default(function):
    default_empty_params = _default_empty_params(function)
    return len(default_empty_params) <= 1


def _done(task):
    if not task.cancelled() and task.exception() is not None:
        ex = task.exception()
        traceback.print_exception(type(ex), ex, ex.__traceback__)
        global _should_run
        _should_run = False


def _callback(cb_function, sequential, executor):
    async def _cb(key):
        if cb_function is None:
            return

        if sequential:
            if asyncio.iscoroutinefunction(cb_function):
                await cb_function(key)
            else:
                cb_function(key)
        else:
            if asyncio.iscoroutinefunction(cb_function):
                task = asyncio.create_task(cb_function(key))
                task.add_done_callback(_done)
            else:
                future = executor.submit(cb_function, key)
                future.add_done_callback(_done)

    return _cb


# Raw and _nonblocking inspiration from:
# http://ballingt.com/_nonblocking-stdin-in-python-3/
@contextmanager
def _raw(stream):
    # Not required on Windows
    if _is_windows:
        yield
        return

    original_stty = termios.tcgetattr(stream)
    try:
        tty.setcbreak(stream)
        yield
    finally:
        termios.tcsetattr(stream, termios.TCSANOW, original_stty)


@contextmanager
def _nonblocking(stream):
    # Not required on Windows
    if _is_windows:
        yield
        return

    fd = stream.fileno()
    orig_fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    try:
        fcntl.fcntl(fd, fcntl.F_SETFL, orig_fl | os.O_NONBLOCK)
        yield
    finally:
        fcntl.fcntl(fd, fcntl.F_SETFL, orig_fl)


def _read_char(debug):
    if _is_windows:
        return _read_char_win(debug)
    else:
        return _read_char_unix(debug)


def _read_char_win(debug):
    # Return if nothing to read
    if not msvcrt.kbhit():
        return ""

    char = msvcrt.getwch()
    if char in _WIN_SPECIAL_CHAR_STARTS:
        # Check if requires one more read
        if char in _WIN_REQUIRES_TWO_READS_STARTS:
            char += msvcrt.getwch()

        if char in _WIN_CHAR_TO_READABLE:
            return _WIN_CHAR_TO_READABLE[char]
        else:
            if debug:
                print(f"Non-supported win char: {repr(char)}")
            return None

    # Change some character representations to readable strings
    elif char in _CHAR_TO_READABLE:
        char = _CHAR_TO_READABLE[char]

    return char


def _read_char_unix(debug):
    char = _read_unix_stdin(1)

    # Skip and continue if read failed
    if char is None:
        return None

    # Handle any character
    elif char != "":
        # Read more if ansi character, skip and continue if unknown
        if _is_unix_ansi(char):
            char, raw = _read_and_parse_unix_ansi(char)
            if char is None:
                if debug:
                    print(f"Non-supported ansi char: {repr(raw)}")
                return None
        # Change some character representations to readable strings
        elif char in _CHAR_TO_READABLE:
            char = _CHAR_TO_READABLE[char]

    return char


def _read_unix_stdin(amount):
    try:
        return sys.stdin.read(amount)
    except IOError:
        return None


# '\x' at the start is a good indicator for ansi character
def _is_unix_ansi(char):
    rep = repr(char)
    return len(rep) >= 2 and rep[1] == "\\" and rep[2] == "x"


def _read_and_parse_unix_ansi(char):
    char += _read_unix_stdin(5)
    if char in _UNIX_ANSI_CHAR_TO_READABLE:
        return _UNIX_ANSI_CHAR_TO_READABLE[char], char
    else:
        return None, char


async def _react_to_input(state, options):
    # Read next character
    state.current = _read_char(options.debug)

    # Skip and continue if read failed
    if state.current is None:
        return state

    # Handle any character
    elif state.current != "":

        # Make lower case if requested
        if options.lower:
            state.current = state.current.lower()

        # Stop if until character has been read
        if options.until is not None and state.current == options.until:
            stop_listening()
            return state

        # Release state.previous if new pressed
        if state.previous != "" and state.current != state.previous:
            await options.on_release_callback(state.previous)
            # Weirdly on_release fires too late on Windows unless there is
            # an extra sleep here when sequential=False...
            if _is_windows and not options.sequential:
                await asyncio.sleep(options.sleep)

        # Press if new character, update state.previous
        if state.current != state.previous:
            await options.on_press_callback(state.current)
            state.initial_press_time = time()
            state.previous = state.current

        # Update press time
        if state.current == state.previous:
            state.press_time = time()

    # Handle empty
    # - Release the state.previous character if nothing is read
    # and enough time has passed
    # - The second character comes slower than the rest on terminal
    elif state.previous != "" and (
        time() - state.initial_press_time > options.delay_second_char
        and time() - state.press_time > options.delay_other_chars
    ):
        await options.on_release_callback(state.previous)
        state.previous = state.current

    return state


if __name__ == "__main__":

    async def press(key):
        print(f"'{key}' pressed")

    def release(key):
        print(f"'{key}' released")

    print("listening keyboard, press keys, and press 'esc' to exit")
    listen_keyboard(on_press=press, on_release=release)
    # ^this is the same as
    # asyncio.run(listen_keyboard_manual(press, release))
