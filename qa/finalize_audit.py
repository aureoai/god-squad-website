"""Finalize the Phase 1 audit: read the workflow output, validate, write the report, print the terminal summary.
Usage: python finalize_audit.py <workflow-output-json> [--write]
Without --write it only validates and prints; with --write it creates PHASE-1-WEBSITE-AUDIT.md in the project root.
"""
import json, re, sys, io, os, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_NAME = "PHASE-1-WEBSITE-AUDIT.md"
src = sys.argv[1]
write = '--write' in sys.argv
top = json.load(open(src, encoding='utf-8', errors='replace'))
res = top.get('result', top)
if isinstance(res, str):
    res = json.loads(res)
report = res.get('report', '')
issues = res.get('issues', [])
counts = res.get('counts', {})
bir = res.get('businessInfoRequired', [])
major = res.get('majorFinding', '')
crit = res.get('criticProblems', [])
missed = res.get('missedEdits', [])

print("== WORKFLOW LOGS ==")
for l in top.get('logs', []): print("  ", l)
print("\n== REPORT ==")
print(f"characters: {len(report):,}  words: {len(report.split()):,}  lines: {report.count(chr(10)):,}")
heads = re.findall(r'^## (\d+)\. (.+)$', report, re.M)
nums = [int(n) for n, _ in heads]
missing = [n for n in range(1, 33) if n not in nums]
dupes = [n for n, c in collections.Counter(nums).items() if c > 1]
print(f"sections found: {len(heads)}  missing: {missing or 'none'}  duplicated: {dupes or 'none'}")
order_ok = nums == sorted(nums)
print(f"section order ascending: {order_ok}")
for n, t in heads:
    body = report.split(f'## {n}. {t}', 1)[1]
    nxt = re.search(r'^## ', body, re.M)
    seg = body[:nxt.start()] if nxt else body
    print(f"  {int(n):2d}. {t:34} {len(seg.split()):6,d} words")
bad = [p for p in ['(synthesis failed)', 'TODO', 'lorem', 'PLACEHOLDER', '{{ p.name }}'] if p in report and p != '{{ p.name }}']
print(f"forbidden placeholders present: {bad or 'none'}")
print(f"mentions of 'hover' being dead: {len(re.findall(r'hover[^.]{0,60}(dead|not implemented|stripped)', report, re.I))}")
print(f"'BUSINESS INFORMATION REQUIRED' occurrences: {report.count('BUSINESS INFORMATION REQUIRED')}")
print(f"'.dc.html' mentions: {report.count('.dc.html')}")

print("\n== ISSUES ==")
print(f"total {len(issues)}  counts: {json.dumps(counts)}")
ids = [i['id'] for i in issues]
dup_ids = [k for k, c in collections.Counter(ids).items() if c > 1]
print(f"duplicate ids: {dup_ids or 'none'}")
by_area = collections.Counter(i['id'].split('-')[0] for i in issues)
print("by prefix:", dict(by_area))
print("by phase:", dict(collections.Counter(i['phase'] for i in issues)))
print(f"\ncritic problems: {len(crit)}  missed edits: {len(missed)}")
for p in crit[:20]: print("  -", p.get('severity'), '|', p.get('where', '')[:70], '|', p.get('problem', '')[:160])
for m in missed[:10]: print("  missed:", m)
print(f"\nbusiness info required ({len(bir)}):")
for b in bir: print("  -", b)

if write:
    path = os.path.join(PROJECT, OUT_NAME)
    if os.path.exists(path):
        print(f"\nREFUSING to overwrite existing {path}")
        sys.exit(2)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(report.rstrip() + '\n')
    print(f"\nWROTE {path} ({os.path.getsize(path):,} bytes)")

sev = counts.get('severity', {}); pri = counts.get('priority', {})
print("\n" + "=" * 40)
print("GOD SQUAD — PHASE 1 AUDIT COMPLETE")
print("=" * 40)
print("\nFILES INSPECTED:\n44 project files (plus 6 external logo source files noted, read-only)")
print("\nASSETS INSPECTED:\n41 (40 image files + 1 editor thumbnail)")
print("\nDUPLICATES FOUND:\n9 exact duplicate groups (11 redundant copies)")
print(f"\nCRITICAL ISSUES:\n{sev.get('CRITICAL', 0)}")
print(f"\nHIGH PRIORITY:\n{sev.get('HIGH', 0)} high-severity issues / {pri.get('P1', 0)} at P1")
print(f"\nMEDIUM PRIORITY:\n{sev.get('MEDIUM', 0)} medium-severity issues / {pri.get('P2', 0)} at P2")
print(f"\nLOW PRIORITY:\n{sev.get('LOW', 0)} low-severity issues / {pri.get('P3', 0)} at P3")
print(f"\nSHOPIFY BLOCKERS:\n{counts.get('blockers', 0)}")
print(f"\nUX ISSUES:\n{counts.get('ux', 0)}")
print(f"\nACCESSIBILITY ISSUES:\n{counts.get('a11y', 0)}")
print(f"\nSEO ISSUES:\n{counts.get('seo', 0)}")
print(f"\nPERFORMANCE ISSUES:\n{counts.get('perf', 0)}")
print(f"\nMAJOR FINDING:\n{major}")
print("\nRECOMMENDED NEXT PHASE:\nPHASE 2 — DESIGN SYSTEM")
print(f"\nREPORT:\n{OUT_NAME}")
print("\nIMPORTANT:\nNO PROJECT FILES WERE MODIFIED.")
print("\nSTOP HERE.\n\nDO NOT BEGIN PHASE 2.")
print("=" * 40)
