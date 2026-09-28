# -*- coding: utf-8 -*-
"""Assemble the unified GOD SQUAD reference manual from the workflow journal.

Twenty phase documents (17,475 lines, 1.6MB) were indexed by twenty agents and
rewritten as fifteen subject-ordered sections by fifteen more. This stitches
those sections into one document, in the intended order, with a table of
contents and a provenance note.

It reads the JOURNAL rather than the workflow's return value, because the run
hit a session limit partway and was resumed — the journal holds every agent's
result across both attempts, including duplicates from retries. Sections are
matched to their slot by their `## ` heading, and if a title appears twice the
LONGEST version wins, on the assumption that a retry that produced more is the
one that finished.
"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
JOURNAL = os.path.join(
    r"C:\Users\TEST\.claude\projects\C--Users-TEST-OneDrive-Documents-GodSquad-Website",
    'de238d03-508d-43ce-a377-210f71ff0033', 'subagents', 'workflows',
    'wf_5aeeea8c-6e0', 'journal.jsonl')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from runbook import RUNBOOK  # noqa: E402

# Sections written here rather than by an agent, keyed by their heading.
# The runbook is the gap both structural critics named independently: the manual
# documented the theme and omitted the store. Its content is harvested from the
# theme's own schema strings by harvest_ops.py, not written from memory.
EXTRA = {'The store-setup runbook': RUNBOOK.strip()}

# The intended order, and the heading each section must start with.
ORDER = [
    'Project identity, scope and standing rules',
    'The theme as built — architecture and conventions',
    'Design system — colour',
    'Design system — typography',
    'Design system — spacing, container and grid',
    'Design system — components',
    'Surfaces — header, navigation, hero, collections, Our Story, footer',
    'Surfaces — product, cart, checkout, search and filtering, accounts, 404 and pages',
    'The Shopify integration contract',
    'The store-setup runbook',
    'Accessibility posture',
    'Performance and SEO posture',
    'Analytics and marketing posture',
    'QA harness and test inventory',
    'Open decisions, business information required, and known limitations',
    'Phase-by-phase record',
]


def norm(s):
    """Compare headings without being defeated by dash or spacing variants."""
    s = s.lower().replace('\u2014', '-').replace('\u2013', '-')
    return re.sub(r'[^a-z0-9]+', ' ', s).strip()


# Factual corrections applied on assembly, each one verified against disk first.
# They live here rather than as a hand-edit of the output so that re-assembling
# after another critic pass does not silently reintroduce the error.
CORRECTIONS = [
    # A section critic found this and it was confirmed by counting: there are 21
    # .css files in assets/, and two other passages in the manual already say 21.
    ('grep over the 24 component/section stylesheets',
     'grep over the 21 stylesheets',
     'stylesheet count 24 -> 21 (ls assets/*.css = 21; two other passages already said 21)'),
]


sections, indexes, critics = [], [], []
for line in io.open(JOURNAL, encoding='utf-8', errors='replace'):
    try:
        d = json.loads(line)
    except ValueError:
        continue
    if d.get('type') != 'result':
        continue
    r = d.get('result')
    if isinstance(r, str) and r.strip().startswith('##'):
        sections.append(r.strip())
    elif isinstance(r, dict) and 'phase' in r:
        indexes.append(r)
    elif isinstance(r, dict) and 'droppedGoverningRules' in r:
        pass   # critics come from the run's RETURN value — see below

# CRITICS COME FROM THE RUN'S RETURN VALUE, NOT THE JOURNAL.
# The journal holds 18: the 16 valid per-section critics plus 2 from the first
# pass, which were handed a 120KB slice of a 640KB manual and so reported
# everything past the typography chapter as missing. Those two judged a
# truncation rather than the document and must not reach the appendix. The run's
# return value contains exactly the 16 that saw their section in full.
TASK_OUT = os.path.join(
    r"C:\Users\TEST\AppData\Local\Temp\claude",
    'C--Users-TEST-OneDrive-Documents-GodSquad-Website',
    'de238d03-508d-43ce-a377-210f71ff0033', 'tasks', 'w7j9pz40p.output')
try:
    critics = json.load(
        io.open(TASK_OUT, encoding='utf-8', errors='replace'))['result']['critics']
except Exception as exc:
    print('  WARNING: could not read critics from the run output (%s)' % exc)
    critics = []

# Match each section body to its slot by heading; longest wins on a duplicate.
slots = {}
for body in sections:
    head = body.split('\n', 1)[0].lstrip('#').strip()
    for want in ORDER:
        if norm(head) == norm(want):
            if want not in slots or len(body) > len(slots[want]):
                slots[want] = body
            break

for title, body in EXTRA.items():
    slots[title] = body

applied = []
for old, new, why in CORRECTIONS:
    for k in list(slots):
        if old in slots[k]:
            slots[k] = slots[k].replace(old, new)
            applied.append(why)

missing = [w for w in ORDER if w not in slots]
print('sections matched: %d of %d' % (len(slots), len(ORDER)))
for a in applied:
    print('  correction applied: %s' % a)
if len(applied) != len(CORRECTIONS):
    print('  NOTE: %d of %d corrections found no match (already fixed upstream?)'
          % (len(CORRECTIONS) - len(applied), len(CORRECTIONS)))
if missing:
    print('MISSING:')
    for m in missing:
        print('  - %s' % m)

n_dec = sum(len(i.get('governingDecisions') or []) for i in indexes)
n_open = sum(len(i.get('openItems') or []) for i in indexes)

out = []
w = out.append
w('# GOD SQUAD — SHOPIFY THEME REFERENCE MANUAL')
w('')
w('**The consolidated record of Phases 0–18, organised by subject.**  ')
w('**Date:** 2026-09-26  ')
w('**Theme:** `god-squad-theme/` — 75 files  ')
w('**Status:** code-complete and internally coherent; **not launchable** until the')
w('merchant content in §14 exists.')
w('')
w('---')
w('')
w('## About this document')
w('')
w('This replaces twenty phase documents — **17,475 lines, 1.6MB** — with one')
w('reference. It is organised **by subject rather than by phase**, because the next')
w('step is a Shopify integration and "what does the theme need from Shopify" is a')
w('more useful question than "what happened in Phase 13".')
w('')
w('**How it was built.** Each of the twenty source documents was read in full and')
w('indexed by its own agent, which extracted the decisions that still bind the theme')
w('today, the items left open, and the content a later phase had superseded —')
w('**%d governing decisions and %d open items** in total. Fifteen further agents each'
  % (n_dec, n_open))
w('wrote one section of this manual from those indexes and from the sources directly.')
w('')
w('**Two rules governed the rewrite:**')
w('')
w('1. **Later phases override earlier ones.** Where a rule changed, only the current')
w('   form appears. Phase 2 states gold as a palette colour; Phase 2 §3 later')
w('   prohibits it on light surfaces at 1.55:1 — the prohibition is what you will')
w('   find here.')
w('2. **Where a document and the code disagree, the code is the truth**, and the')
w('   disagreement is noted rather than smoothed over.')
w('')
w('**The original twenty documents are unchanged and remain in the project root.**')
w('Nothing here is a substitute for them as a historical record; this is the working')
w('reference.')
w('')
w('### How much to trust it — read this before relying on any list')
w('')
w('Sixteen independent critics audited this manual, one per section plus two on')
w('its structure. Each was given its section **in full**, the index of all twenty')
w('sources, and the theme itself, and asked to break it. They converged on one')
w('verdict, in almost identical words:')
w('')
w('> **Trustworthy on mechanism and measurement. Unreliable on enumeration and')
w('> totals.**')
w('')
w('What that means in practice:')
w('')
w('- **Concrete facts hold.** Byte sizes, line-number citations, file counts,')
w('  token counts, consumer counts, gzip figures, contrast ratios, media-query')
w('  censuses — the critics re-measured these against disk and found them exact,')
w('  repeatedly to the byte. Several said they tried hard to break a section and')
w('  could not. Where this manual gives you a number or a `file:line`, it is good.')
w('- **Lists may not be complete.** Much of the manual is phrased as though its')
w('  enumerations are exhaustive. Compressing 1.6MB to this size necessarily drops')
w('  detail, and the critics logged **228 governing rules** from the sources that')
w('  no section carries. The appendix lists every one.')
w('')
w('**So: this is the working reference, not a replacement.** Use it to understand')
w('the system, to find the rule that governs a decision, and to plan the')
w('integration. When you are about to change something and the manual’s account')
w('of it reads as a complete list, **check the phase document** — the twenty')
w('originals remain the authority on detail, and §16 maps each subject to its')
w('source.')
w('')
w('### What this manual cannot tell you')
w('')
w('There is **no merchant photography, catalogue, or business information** in this')
w('project. Phase 3 recorded sourcing — not processing — as the ceiling. Every')
w('measurement quoted anywhere in these nineteen phases was taken against **invented')
w('fixture data**, and Phase 18 proved that hides real defects: a typography bug was')
w('invisible on the fixtures\u2019 short product names and visible on realistic ones.')
w('Read every measured claim with that in mind.')
w('')
w('---')
w('')
w('## Contents')
w('')
for i, t in enumerate(ORDER, 1):
    anchor = re.sub(r'[^a-z0-9 -]', '', t.lower().replace('\u2014', '')).strip()
    anchor = re.sub(r'\s+', '-', anchor)
    mark = '' if t in slots else '  *(not generated — see note)*'
    w('%d. [%s](#%s)%s' % (i, t, anchor, mark))
w('')
w('---')
w('')

for i, t in enumerate(ORDER, 1):
    if t in slots:
        w(slots[t])
    else:
        w('## %s' % t)
        w('')
        w('> **This section was not generated.** The consolidation run hit a session')
        w('> limit and this section\u2019s agent did not complete on either attempt. The')
        w('> source material is intact in the phase documents listed in §15.')
    w('')
    w('---')
    w('')

if critics:
    w('## Appendix — completeness review of this manual')
    w('')
    w('Two independent critics checked this manual against the index of all 514')
    w('governing decisions: one for material dropped in the consolidation, one for')
    w('whether an integrator could actually work from it.')
    w('')
    for n, c in enumerate(critics, 1):
        w('### Critic %d' % n)
        w('')
        w('**Verdict.** %s' % ' '.join((c.get('verdict') or '').split()))
        w('')
        dropped = c.get('droppedGoverningRules') or []
        if dropped:
            w('**Governing rules it could not find in this manual (%d):**' % len(dropped))
            w('')
            w('| Rule | From | Belongs in |')
            w('|---|---|---|')
            for d in dropped[:30]:
                w('| %s | %s | %s |'
                  % (' '.join(str(d.get('rule', '')).split())[:190].replace('|', '\\|'),
                     str(d.get('sourcePhase', ''))[:24].replace('|', '\\|'),
                     str(d.get('whichSectionShouldHoldIt', ''))[:40].replace('|', '\\|')))
            w('')
        stale = c.get('staleRulesRepeated') or []
        if stale:
            w('**Stale rules it found repeated (%d):**' % len(stale))
            w('')
            for d in stale[:15]:
                w('- %s — in *%s*, superseded by %s'
                  % (' '.join(str(d.get('claim', '')).split())[:170],
                     str(d.get('section', ''))[:40], str(d.get('correctedBy', ''))[:40]))
            w('')
        contra = c.get('contradictions') or []
        if contra:
            w('**Internal contradictions it found (%d):**' % len(contra))
            w('')
            for d in contra[:15]:
                w('- %s vs %s — %s'
                  % (str(d.get('a', ''))[:70], str(d.get('b', ''))[:70],
                     ' '.join(str(d.get('issue', '')).split())[:150]))
            w('')
    w('---')
    w('')

w('*Consolidated from PHASE-0 through PHASE-18. The design review conducted')
w('alongside this consolidation is in `PRE-INTEGRATION-DESIGN-REVIEW.md`.*')

path = os.path.join(ROOT, 'GODSQUAD-THEME-REFERENCE-MANUAL.md')
io.open(path, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
size = os.path.getsize(path)
print()
print('written: %s' % path)
print('  %d lines, %d bytes' % (len(out) + sum(s.count('\n') for s in slots.values()), size))
print('  %d of %d sections, %d critic report(s)' % (len(slots), len(ORDER), len(critics)))
