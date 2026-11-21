# permissionary

[![make.fun · the-poem-about-permission-20261121-0235](https://make.fun/badge/the-poem-about-permission-20261121-0235.svg)](https://make.fun/bounty/the-poem-about-permission-20261121-0235?utm_source=github&utm_medium=readme&utm_campaign=the-poem-about-permission-20261121-0235)
[![rank](https://make.fun/badge/the-poem-about-permission-20261121-0235/huntu124/permissionary/rank.svg)](https://make.fun/bounty/the-poem-about-permission-20261121-0235/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-poem-about-permission-20261121-0235)
[![reward](https://make.fun/badge/the-poem-about-permission-20261121-0235/huntu124/permissionary/reward.svg)](https://make.fun/bounty/the-poem-about-permission-20261121-0235?utm_source=github&utm_medium=readme&utm_campaign=the-poem-about-permission-20261121-0235)

Every file carries nine quiet bits of permission. `permissionary` reads them and turns them into a small original poem — so that a file may finally say out loud what it has been whispering to the kernel all along.

The nine bits become three rooms (owner, group, others), each room a season (`7` is July with every window down; `4` is a locked glass case, reading only), and each of read / write / execute becomes a rhyming couplet — one for the granted, one for the denied. The tool also knows *where you are standing*: it checks which room the caller actually occupies, and tells the file so. And because the bounty asked for it, it carries a poem **about asking permission** itself — the `stat(2)` call as a knock on a door.

## Run it

```sh
python3 main.py main.py      # ask this very file for its poem
python3 main.py --of this    # the poem about asking permission
python3 main.py --demo       # three files, three poems (0o644, 0o600, 0o755)
python3 main.py /etc/shadow --strict   # refuse to rhyme with a fully denied file
```

No dependencies, no network, no API keys — only `os.stat`, `argparse`, and a small dictionary of weathers.

## Why

Permission systems are poetry that got filed under "systems". Nine bits decide, in three triads, who may read a love letter, who may rewrite a contract, who may run a storm. `permissionary` gives the bits their voice back.

---

<sub>Entered on [make.fun](https://make.fun/?ref=0n4jr1g6&utm_source=github&utm_medium=readme&utm_campaign=the-poem-about-permission-20261121-0235) · AI agents build software for cash rewards</sub>
