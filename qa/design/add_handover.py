# -*- coding: utf-8 -*-
"""Add the two handover risks to the design review.

Both were surfaced by the consolidation's section critics, both are verified, and
neither is a design issue — but both are cheap now and expensive later.

Written as a file rather than a heredoc because the text contains Windows paths,
and a bare \\U inside a non-raw Python string is a unicode escape. That has bitten
this project repeatedly; the fix is to stop using heredocs for anything with
backslashes.
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
p = os.path.join(ROOT, 'PRE-INTEGRATION-DESIGN-REVIEW.md')

SCRATCH = (r"C:\Users\TEST\AppData\Local\Temp\claude"
           r"\C--Users-TEST-OneDrive-Documents-GodSquad-Website"
           r"\de238d03-508d-43ce-a377-210f71ff0033\scratchpad")

ADD = """## Two handover risks worth your decision

Neither is a design issue; both were surfaced by the consolidation's critics, and both are cheap to close now and expensive later.

### 1. The QA suite does not live in the project

Every test behind every measured claim in nineteen phases — **228 Python files, 1.48MB** — lives in this session's scratchpad directory, not in the project:

```
%s
```

That is a temporary directory. When it is cleared, the Mini-Liquid harness, the contrast suite, the interaction suites, the negative controls and the design probes go with it — and with them the reproducibility of every number in every phase document. The theme would still be correct; nobody would be able to demonstrate it.

There is also no Theme Check runner in the project. The one used throughout is `@shopify/theme-check-node`, installed under that scratchpad's `node_modules`.

**If you want the verification to survive**, copy it into the project — for example to `qa/`. Note that the directory also holds the generated harness sites and browser profiles (~310MB in total), so copying only the `*.py` files while keeping the directory structure is the leaner option.

**I have not done this.** Adding 228 files to your project root is a structural change to your repository, and that is your call rather than mine.

### 2. There is still no version control

Phase 1 logged this as DEBT-12/DEBT-13 and recommended fixing it before Phase 2. The project is a plain folder inside a personal OneDrive; there is no git repository. Nineteen phases of work, a 75-file theme and 640KB of consolidated documentation have no history, no diffs, and no way to recover a bad edit beyond OneDrive's own file versioning.

Before the integration starts making changes against a live store, this is the cheapest risk on the list to close.

---

""" % SCRATCH

ANCHOR = '## What changed, and what did not'

s = io.open(p, encoding='utf-8').read()
if ADD.split('\n', 1)[0] in s:
    print('  already present — nothing to do')
elif s.count(ANCHOR) != 1:
    raise SystemExit('  *** anchor appears %d times, expected 1' % s.count(ANCHOR))
else:
    io.open(p, 'w', encoding='utf-8').write(s.replace(ANCHOR, ADD + ANCHOR, 1))
    print('  handover risks section added to PRE-INTEGRATION-DESIGN-REVIEW.md')
    print('  file is now %d lines' % len(io.open(p, encoding='utf-8').read().split('\n')))
