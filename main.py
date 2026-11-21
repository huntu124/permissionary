#!/usr/bin/env python3.13
"""permissionary - a machine that asks your files for a poem.

Every file carries nine quiet bits of permission. This tool reads them
and turns them into a small original poem, so that a file may finally
say out loud what it has been whispering to the kernel all along.

Usage:
    python3 main.py <path>            # ask that file for its poem
    python3 main.py --of this         # a poem about asking permission
    python3 main.py --demo            # three files, three poems
    python3 main.py <path> --strict   # refuse to rhyme with deny
"""

from __future__ import annotations

import argparse
import os
import stat
import sys
from datetime import datetime

# ---------------------------------------------------------------- phrases

TRIPLET_ORDER = ("reader", "writer", "executor")

VOICE_BY_ROLE = {
    "owner": "The owner speaks first, and mostly says yes.",
    "group": "The group echoes, softer, a chorus in the middle room.",
    "others": "And the world, at the end of the corridor, waits.",
}

ROOM_BY_ROLE = {
    "owner": "You stand in the first room. The file knows your name.",
    "group": "You stand in the second room. The file knows your people.",
    "others": "You stand in the last room. The file knows only your knocking.",
}

SEASON_BY_DIGIT = {
    7: "July, everything open, every window down.",
    6: "Late autumn: read and write, but the door is shut.",
    5: "A museum day: you may look, never touch.",
    4: "A locked glass case. Reading only. Bring your own light.",
    3: "A stairwell: you may pass and act, but the ledger is closed.",
    2: "A ghost writer: change it, but you may never read it.",
    1: "A machine room: run it, but do not ask what is inside.",
    0: "A sealed envelope addressed to no one.",
}

RHYME = {
    ("read", "y"): ("The reading comes as freely as the rain,", "though no one asked it, and none can explain."),
    ("write", "y"): ("The writing lives, a pen that never dries,", "and every line is gossip in disguise."),
    ("exec", "y"): ("And running is a kind of gentle thunder,", "one keystroke wide, and the whole night splits asunder."),
    ("read", "n"): ("The reading waits outside a frosted pane,", "the words are warm, the window keeps the strain."),
    ("write", "n"): ("The writing is a letter never sent,", "kept, unsigned, for someone else's intent."),
    ("exec", "n"): ("The running stays a thunder still asleep,", "a storm behind a wall too proud to peep."),
}

CLOSERS = {
    "y": "So it says yes, and says it in a poem, which is the politest yes there is.",
    "n": "So it says no, and says it in a poem, which is the kindest no there is.",
}

ASKING_POEM = """A Poem About Asking Permission

Before I touch the sleeping byte,
I knock. The knock is stat(2).
The file, if it is feeling right,
will answer: owner, group, and you.

To ask is small. To ask is rare
in rooms where root does as it will.
Yet even chmod has a prayer:
a mode, a meaning, and a will.

I read the nine bits like a psalm,
three triads, each a different room.
I do not force. I do not disarm.
I only rhyme with what may bloom.

Permission is a poem, too:
it measures what we dare to do.
"""


# ---------------------------------------------------------------- core

def triplet_bits(mode: int, who: str) -> int:
    shift = {"owner": 6, "group": 3, "others": 0}[who]
    return (mode >> shift) & 7


def who_am_i_for(path: str, mode: int) -> str:
    """Which of the three rooms the caller is actually standing in."""
    try:
        uid, gid = os.geteuid(), os.getegid()
        st = os.stat(path)
        if uid == st.st_uid:
            return "owner"
        if gid == st.st_gid:
            return "group"
        return "others"
    except (OSError, AttributeError):
        return "owner"


def couplet(kind: str, allowed: bool) -> tuple[str, str]:
    return RHYME[(kind, "y" if allowed else "n")]


def compose(path: str, mode: int) -> str:
    role = who_am_i_for(path, mode)
    lines: list[str] = []
    lines.append(f"A poem of {os.path.basename(path) or 'the nameless one'}")
    lines.append(f"(as {datetime.now():%Y-%m-%d}, mode {oct(mode)[2:].zfill(4)})")
    lines.append("")
    for who in ("owner", "group", "others"):
        bits = triplet_bits(mode, who)
        lines.append(f"[{who} = {bits}] {SEASON_BY_DIGIT[bits]}")
        lines.append(VOICE_BY_ROLE[who])
    lines.append("")
    lines.append(ROOM_BY_ROLE[role])
    lines.append("")
    allowed_map = {
        "read": bool(mode & 0o444),
        "write": bool(mode & 0o222),
        "exec": bool(mode & 0o111),
    }
    for kind, allowed in allowed_map.items():
        a, b = couplet(kind, allowed)
        lines.append(a)
        lines.append(b)
    lines.append("")
    lines.append(CLOSERS["y" if allowed_map["read"] else "n"])
    return "\n".join(lines)


# ---------------------------------------------------------------- cli

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="permissionary", description="Turn file permissions into poems.")
    p.add_argument("path", nargs="?", help="the file to ask")
    p.add_argument("--of", dest="of_", action="store_true", help="the poem about asking permission")
    p.add_argument("--demo", action="store_true", help="three files, three poems")
    p.add_argument("--strict", action="store_true", help="refuse to rhyme with deny")
    args = p.parse_args(argv)

    if args.of_:
        print(ASKING_POEM)
        return 0

    if args.demo:
        import tempfile
        names = ("diary.txt", "secret.key", "run_me.sh")
        modes = (0o644, 0o600, 0o755)
        for name, m in zip(names, modes):
            fp = os.path.join(tempfile.gettempdir(), name)
            with open(fp, "w") as fh:
                fh.write("placeholder\n")
            os.chmod(fp, m)
            print(compose(fp, os.stat(fp).st_mode))
            print("\n" + "-" * 46 + "\n")
            os.remove(fp)
        return 0

    if not args.path:
        p.print_help()
        return 0
    if not os.path.exists(args.path):
        print(f"permissionary: no such file: {args.path}", file=sys.stderr)
        return 1
    mode = stat.S_IMODE(os.stat(args.path).st_mode)
    if args.strict and not (mode & 0o444):
        print("permissionary: strict mode will not rhyme with a fully denied file.", file=sys.stderr)
        return 2
    print(compose(args.path, mode))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
