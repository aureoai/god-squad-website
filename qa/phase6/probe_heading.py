import re, sys
sys.path.insert(0, '.')
import build as B

e = B.make_engine(False)
hero_html = B.render_section(e, 'sections/hero.liquid', 'hero', B.wrap(B.HERO_SETTINGS))

def fc(overrides):
    m = dict(B.SECTION_DEFAULTS)
    m.update(overrides)
    return B.render_section(e, 'sections/featured-collection.liquid', 'x', B.wrap(m))

col = B.collection('the-faithful', [B.P_TEE, B.P_HOODIE, B.P_CAP])

for label, ov in [
    ('heading PRESENT', {'collection': col}),
    ('heading BLANK  ', {'collection': col, 'heading': ''}),
    ('heading SPACES ', {'collection': col, 'heading': '   '}),
]:
    page = hero_html + fc(ov)
    levels = re.findall(r'<h([1-6])[ >]', page)
    print(label, '-> outline:', ' '.join('h'+l for l in levels))
