# -*- coding: utf-8 -*-
"""Apply the Phase 1 review pass to PHASE-1-WEBSITE-AUDIT.md.

Replaces the revised section bodies, merges the revised issue registers, then
regenerates everything derived from the register: the priority matrix, the phase
dependency map, and every count quoted in the executive summary and matrix intro.

Usage: python apply_review.py <review-workflow-output.json> [--write]
"""
import json, re, io, sys, os, collections

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
EV = HERE + '/audit-evidence'
REPORT = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\PHASE-1-WEBSITE-AUDIT.md"

PHASES = ['PHASE 2 — DESIGN SYSTEM', 'PHASE 3 — ASSET PREPARATION', 'PHASE 4 — HEADER & NAVIGATION',
          'PHASE 5 — HERO', 'PHASE 6 — COLLECTIONS & BEST SELLERS', 'PHASE 7 — OUR STORY',
          'PHASE 8 — PRODUCT & SHOPPING UX', 'PHASE 9 — MOBILE UX', 'PHASE 10 — SHOPIFY THEME CONVERSION',
          'PHASE 11 — THEME EDITOR', 'PHASE 12 — PERFORMANCE', 'PHASE 13 — SEO',
          'PHASE 14 — ACCESSIBILITY', 'PHASE 15 — ECOMMERCE QA', 'PHASE 16 — FINAL POLISH']
SEV_ORDER = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
PRI_ORDER = {'P0': 0, 'P1': 1, 'P2': 2, 'P3': 3}
PRI_LABEL = {'P0': 'BLOCKER', 'P1': 'HIGH PRIORITY', 'P2': 'MEDIUM PRIORITY', 'P3': 'POLISH'}

TAG_RE = re.compile(r'<(/?[a-zA-Z][a-zA-Z0-9-]*(?:\s[^<>\n]{0,140})?)>')


def wrap_bare_tags(text):
    out, n = [], 0
    for i, part in enumerate(re.split(r'(```.*?```)', text, flags=re.S)):
        if i % 2:
            out.append(part); continue
        for j, seg in enumerate(re.split(r'(`[^`\n]*`)', part)):
            if j % 2:
                out.append(seg); continue
            seg, k = TAG_RE.subn(r'`<\1>`', seg)
            n += k
            out.append(seg)
    s = ''.join(out)
    s, adj = re.subn(r'>``<', '>` `<', s)
    return s, n, adj


def clean_cell(s):
    return str(s or '').replace('|', '/').replace('\n', ' ').strip()


def phase_of(p):
    t = str(p or '').strip()
    for ph in PHASES:
        if ph.lower() == t.lower():
            return ph
    m = re.search(r'PHASE\s*(\d+)', t, re.I)
    if m:
        i = int(m.group(1)) - 2
        if 0 <= i < len(PHASES):
            return PHASES[i]
    return PHASES[-1]


# ----------------------------------------------------------------- load
src = sys.argv[1]
write = '--write' in sys.argv
top = json.load(open(src, encoding='utf-8', errors='replace'))
res = top.get('result', top)
if isinstance(res, str):
    res = json.loads(res)
clusters = res['results']
rep = open(REPORT, encoding='utf-8').read()
issues = json.load(open(EV + '/workflow-result.json', encoding='utf-8'))['issues']

print("Review pass outcome:")
revised_prefixes, new_sections, changelog = set(), {}, []
for c in clusters:
    if not c.get('revised'):
        print("  %-24s sections %-12s NO CHANGE (review passed clean)" % (c['key'], c['sections']))
        continue
    r = c['revised']
    revised_prefixes.update(c['prefixes'])
    for s in r.get('sections', []):
        new_sections[int(s['number'])] = s
    changelog += ["**%s** — %s" % (c['key'], x) for x in r.get('changeLog', [])]
    print("  %-24s sections %-12s revised: %d section(s), %d issue(s), %d change-log entries"
          % (c['key'], c['sections'], len(r.get('sections', [])), len(r.get('issues', [])), len(r.get('changeLog', []))))

# ----------------------------------------------------------------- merge issues
if revised_prefixes:
    kept = [i for i in issues if i['id'].split('-')[0] not in revised_prefixes]
    incoming = [i for c in clusters if c.get('revised') for i in c['revised'].get('issues', [])]
    before_ids = {i['id'] for i in issues}
    after_ids = {i['id'] for i in kept} | {i['id'] for i in incoming}
    print("\nIssue register: %d -> %d   added: %s   removed: %s"
          % (len(issues), len(kept) + len(incoming),
             sorted(after_ids - before_ids) or 'none', sorted(before_ids - after_ids) or 'none'))
    issues = kept + incoming

for i in issues:
    i['phase'] = phase_of(i.get('phase'))
issues.sort(key=lambda x: (PRI_ORDER.get(x['priority'], 9), SEV_ORDER.get(x['severity'], 9), x['id']))

# ----------------------------------------------------------------- replace sections
print("\nSection replacement:")
for n in sorted(new_sections):
    s = new_sections[n]
    body, _, _ = wrap_bare_tags(s['markdown'].strip())
    pat = re.compile(r'(^## %d\. .+?\n\n)(.*?)(?=^## )' % n, re.S | re.M)
    if not pat.search(rep):
        print("  %-3d *** heading not found ***" % n); continue
    old_words = len(pat.search(rep).group(2).split())
    rep = pat.sub(lambda m: m.group(1) + body + '\n\n', rep, count=1)
    print("  %-3d %-34s %5d -> %5d words" % (n, s['title'][:34], old_words, len(body.split())))

# ----------------------------------------------------------------- regenerate matrix
matrix = ['| ID | AREA | PROBLEM | IMPACT | RECOMMENDATION | SEVERITY | PRIORITY | PHASE |',
          '|---|---|---|---|---|---|---|---|']
for x in issues:
    matrix.append('| %s | %s | %s | %s | %s | %s | %s | %s |' % (
        x['id'], clean_cell(x['area']), clean_cell(x['problem']), clean_cell(x['impact']),
        clean_cell(x['recommendation']), x['severity'], x['priority'], x['phase']))
matrix = '\n'.join(matrix)
pat = re.compile(r'(^## 28\. Priority Matrix\n\n.*?\n)(\| ID \| AREA \|.*?)(?=\n## )', re.S | re.M)
if pat.search(rep):
    rep = pat.sub(lambda m: m.group(1) + matrix + '\n', rep, count=1)
    print("\nPriority matrix regenerated: %d rows" % len(issues))
else:
    print("\n*** matrix block not found ***")

# ----------------------------------------------------------------- regenerate dependency map
dep = []
for ph in PHASES:
    lst = [x for x in issues if x['phase'] == ph]
    dep.append('### %s (%d issues)\n' % (ph, len(lst)) +
               ('\n'.join('- %s [%s/%s] %s' % (x['id'], x['priority'], x['severity'], clean_cell(x['problem']))
                          for x in lst) if lst else '- No issues assigned by this audit.'))
dep = '\n\n'.join(dep)
pat = re.compile(r'(^## 30\. Phase Dependency Map\n\n.*?\n)(### PHASE 2 .*?)(?=\n## )', re.S | re.M)
if pat.search(rep):
    rep = pat.sub(lambda m: m.group(1) + dep + '\n', rep, count=1)
    print("Dependency map regenerated")
else:
    print("*** dependency map block not found ***")

# ----------------------------------------------------------------- refresh counts
sev = collections.Counter(x['severity'] for x in issues)
pri = collections.Counter(x['priority'] for x in issues)
cat = collections.Counter(c for x in issues for c in x.get('categories', []))
blockers = len([x for x in issues if x['priority'] == 'P0' or 'SHOPIFY-BLOCKER' in x.get('categories', [])])
N = len(issues)
counts = dict(total=N, severity=dict(sev), priority=dict(pri), blockers=blockers,
              ux=cat['UX'], a11y=cat['ACCESSIBILITY'], seo=cat['SEO'],
              perf=cat['PERFORMANCE'], mobile=cat['MOBILE'])
print("\nCounts now: %s" % json.dumps(counts))

sev_str = '%d CRITICAL, %d HIGH, %d MEDIUM, %d LOW' % (sev['CRITICAL'], sev['HIGH'], sev['MEDIUM'], sev['LOW'])
pri_str = '%d P0, %d P1, %d P2, %d P3' % (pri['P0'], pri['P1'], pri['P2'], pri['P3'])

subs = [
    (r'\| Issues raised \| \d+ \|', '| Issues raised | %d |' % N),
    (r'\| By severity \| [^|]+\|', '| By severity | %s |' % sev_str),
    (r'\| By priority \| [^|]+\|', '| By priority | %s |' % pri_str),
    (r'\| Shopify blockers \(P0\) \| \d+ \|', '| Shopify blockers (P0) | %d |' % blockers),
    (r'This matrix is the complete work list produced by the audit: \d+ issues',
     'This matrix is the complete work list produced by the audit: %d issues' % N),
    (r'\*\*Counts\.\*\* P0 — BLOCKER: \d+ issues\. P1 — HIGH PRIORITY: \d+ issues\. P2 — MEDIUM PRIORITY: \d+ issues\. P3 — POLISH: \d+ issues\. By severity: [^.]+\. By category: [^.]+\.',
     '**Counts.** P0 — %s: %d issues. P1 — %s: %d issues. P2 — %s: %d issues. P3 — %s: %d issues. By severity: %s. By category: %d UX, %d mobile, %d accessibility, %d SEO, %d performance.'
     % (PRI_LABEL['P0'], pri['P0'], PRI_LABEL['P1'], pri['P1'], PRI_LABEL['P2'], pri['P2'],
        PRI_LABEL['P3'], pri['P3'], sev_str, cat['UX'], cat['MOBILE'], cat['ACCESSIBILITY'], cat['SEO'], cat['PERFORMANCE'])),
]
print("\nCount refresh:")
for pat_s, rep_s in subs:
    rep, n = re.subn(pat_s, lambda m: rep_s, rep, count=1)
    print("   %-46s %s" % (rep_s[:46], 'OK' if n else '-- not found (unchanged)'))

# ----------------------------------------------------------------- revision note
note = ("\n\n## Appendix C. Revision history\n\n"
        "**2026-09-20 — initial issue.** Sections 2-16, 23, 25, 26 and 28 were produced through a draft, "
        "adversarial-review and revision cycle. Sections 17-22, 24, 27 and 29 were issued as first drafts "
        "because their reviewers could not complete. The executive summary, both matrix introductions, the "
        "Phase 2 scope, the final checklist and Appendix A were written by the audit lead.\n\n"
        "**2026-09-21 — review pass.** The nine previously unreviewed sections (%s) were put through the same "
        "hostile-review and revision cycle as the rest of the report. Every claim in them was re-verified against "
        "the evidence base. The issue register, the priority matrix in §28, the dependency map in §30 and all "
        "counts quoted in §1 and §28 were regenerated from the corrected register. Corrections applied:\n\n%s\n"
        % (', '.join('§%d' % n for n in sorted(new_sections)) if new_sections else 'none required',
           '\n'.join('- ' + c for c in changelog) if changelog else '- No corrections were required; the review passed clean.'))
rep = re.sub(r'\n+## Appendix C\. Revision history.*$', '', rep, flags=re.S)
rep = rep.rstrip() + note

# ----------------------------------------------------------------- normalise the whole document
# Runs last: the matrix, the dependency map and the change log are all generated from
# issue and review text that can contain literal HTML tags.
ent = rep.count('&lt;') + rep.count('&gt;') + rep.count('&quot;') + rep.count('&amp;')
rep = (rep.replace('&lt;', '<').replace('&gt;', '>')
          .replace('&quot;', '"').replace('&amp;', '&'))
rep, wrapped, adj = wrap_bare_tags(rep)
print("\nNormalisation: %d entities decoded, %d tags backticked, %d adjacency fixed" % (ent, wrapped, adj))

# ----------------------------------------------------------------- verify
print("\nVerification:")
heads = re.findall(r'^## (?:(\d+)\.|Appendix ([ABC])\.) ', rep, re.M)
nums = [int(h[0]) for h in heads if h[0]]
print("  sections: %d  missing: %s  duplicated: %s" %
      (len(nums), [n for n in range(1, 33) if n not in nums] or 'none',
       [n for n, k in collections.Counter(nums).items() if k > 1] or 'none'))
print("  appendices:", [h[1] for h in heads if h[1]])
print("  placeholders:", rep.count('(synthesis failed)'))
stripped = re.sub(r'`[^`\n]*`', '', re.sub(r'```.*?```', '', rep, flags=re.S))
print("  bare tags outside code:", len(TAG_RE.findall(stripped)))
print("  unbalanced-backtick lines:", sum(1 for l in rep.split('\n') if l.count('`') % 2 and not l.strip().startswith('```')))
ids = {i['id'] for i in issues}
refd = set(re.findall(r'\b([A-Z]{3,6}-\d{2})\b', rep))
unknown = sorted(r for r in refd - ids if not r.startswith(('DEBT-0', 'DEBT-1', 'DUP-', 'FIDELITY', 'RESPONSIVE', 'TECHNICAL')))
print("  unknown IDs referenced:", unknown or 'none')
print("  characters: %s  words: %s" % (format(len(rep), ','), format(len(rep.split()), ',')))

json.dump(counts, open(EV + '/counts-final.json', 'w', encoding='utf-8'), indent=1)
json.dump(issues, open(EV + '/issues-final.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)

if write:
    open(REPORT, 'w', encoding='utf-8', newline='\n').write(rep.rstrip() + '\n')
    print("\nWROTE %s (%s bytes)" % (REPORT, format(os.path.getsize(REPORT), ',')))
else:
    open(EV + '/report-reviewed-preview.md', 'w', encoding='utf-8', newline='\n').write(rep.rstrip() + '\n')
    print("\n(dry run) preview -> audit-evidence/report-reviewed-preview.md")
