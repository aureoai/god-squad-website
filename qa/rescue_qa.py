# -*- coding: utf-8 -*-
"""Copy the QA suite out of the temp directory and into the project.

Every test behind every measured claim in nineteen phases lives in a Windows
temp folder that Windows will eventually delete. The theme would survive that;
the ability to demonstrate anything about it would not.

WHAT IS COPIED
  Every .py file, plus package.json and package-lock.json.

WHAT IS NOT, AND WHY IT DOES NOT MATTER
  site/        generated fixture pages — check-all.py rebuilds them from the
               theme on every run, and a stale copy would be worse than none
  edge-*/      browser profile directories, worthless once copied
  node_modules 19MB of vendored dependencies. The lockfile pins them exactly,
               so `npm install` restores Theme Check in one command
  *.html       saved DOM dumps from probe runs
  __pycache__  compiled bytecode

THE PATHS ARE REWRITTEN, NOT JUST COPIED

  The suite hardcodes the project location in about forty places:

      PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
      THEME = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'god-squad-theme')
  Those work only while the project sits at exactly that path. The copy computes
  both from its own position on disk instead, so qa/ keeps working if the
  project is moved, renamed, or handed to someone else.

  One reference also has to change meaning: four scripts read PROJECT/images to
  copy six placeholder pictures into the fixtures, and that folder is now
  brand-assets/images. Missing it would break the harness build in a way that
  surfaces later as unrelated-looking test failures.
"""
import io
import os
import re
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QA = os.path.join(ROOT, 'qa')

SKIP_DIRS = {'node_modules', '__pycache__', 'site'}
SKIP_PREFIX = ('edge-',)
KEEP_NON_PY = {'package.json', 'package-lock.json'}

# depth of a file inside qa/ -> the expression that reaches the project root
ROOT_EXPR = {
    0: "os.path.dirname(os.path.dirname(os.path.abspath(__file__)))",
    1: "os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))",
}

PROJECT_LINE = re.compile(
    r'^(?P<ind>\s*)(?P<name>PROJECT|ROOT)\s*=\s*r?"[^"]*GodSquad Website"\s*$', re.M)
THEME_LINE = re.compile(
    r'^(?P<ind>\s*)(?P<name>THEME)\s*=\s*r?"[^"]*god-squad-theme"\s*$', re.M)
THEME_ENV = re.compile(
    r"^(?P<ind>\s*)THEME\s*=\s*os\.environ\.get\('GS_THEME'\)\s*or\s*\\?\s*$", re.M)


def rewrite(text, depth):
    """Point PROJECT / THEME at the real project, computed from __file__."""
    expr = ROOT_EXPR[depth]
    n = 0

    def proj(m):
        nonlocal n
        n += 1
        return '%s%s = %s' % (m.group('ind'), m.group('name'), expr)

    def theme(m):
        nonlocal n
        n += 1
        return "%sTHEME = os.path.join(%s, 'god-squad-theme')" % (m.group('ind'), expr)

    text = PROJECT_LINE.sub(proj, text)
    text = THEME_LINE.sub(theme, text)
    # `THEME = os.environ.get('GS_THEME') or \` + a continued literal on the next line
    text = re.sub(
        r"THEME\s*=\s*os\.environ\.get\('GS_THEME'\)\s*or\s*\\\s*\n\s*r?\"[^\"]*god-squad-theme\"",
        "THEME = os.environ.get('GS_THEME') or os.path.join(%s, 'god-squad-theme')" % expr,
        text)
    # images/ moved under brand-assets/
    text2 = text.replace("PROJECT, 'brand-assets', 'images'", "PROJECT, 'brand-assets', 'images'")
    if text2 != text:
        n += 1
        text = text2
    return text, n


if __name__ == '__main__':
    if not os.path.isdir(QA):
        os.makedirs(QA)

    copied = rewritten = 0
    for dirpath, dirnames, filenames in os.walk(HERE):
        dirnames[:] = [d for d in dirnames
                       if d not in SKIP_DIRS and not d.startswith(SKIP_PREFIX)]
        rel = os.path.relpath(dirpath, HERE)
        if rel == '.':
            rel = ''
        depth = 0 if rel == '' else 1
        for f in sorted(filenames):
            if not (f.endswith('.py') or f in KEEP_NON_PY):
                continue
            src = os.path.join(dirpath, f)
            dst_dir = os.path.join(QA, rel) if rel else QA
            if not os.path.isdir(dst_dir):
                os.makedirs(dst_dir)
            dst = os.path.join(dst_dir, f)
            if f.endswith('.py'):
                text = io.open(src, encoding='utf-8', errors='replace').read()
                new, n = rewrite(text, depth)
                io.open(dst, 'w', encoding='utf-8').write(new)
                if n:
                    rewritten += 1
            else:
                shutil.copy2(src, dst)
            copied += 1

    print('copied %d file(s) into qa/, %d with paths rewritten' % (copied, rewritten))

    size = sum(os.path.getsize(os.path.join(r, f))
               for r, _d, fs in os.walk(QA) for f in fs)
    print('qa/ is now %d files, %.1f MB'
          % (sum(len(fs) for _r, _d, fs in os.walk(QA)), size / 1048576.0))

    print()
    print('Checking no absolute project path survived:')
    left = []
    for r, _d, fs in os.walk(QA):
        for f in fs:
            if not f.endswith('.py'):
                continue
            t = io.open(os.path.join(r, f), encoding='utf-8', errors='replace').read()
            for m in re.finditer(r'r?"[^"]*GodSquad Website[^"]*"', t):
                left.append((os.path.relpath(os.path.join(r, f), QA), m.group(0)[:70]))
    if not left:
        print('  none — qa/ is portable.')
    else:
        print('  %d absolute reference(s) remain:' % len(left))
        for f, s in left[:25]:
            print('    %-34s %s' % (f, s))
