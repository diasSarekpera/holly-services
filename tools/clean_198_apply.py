#!/usr/bin/env python3
"""V198 : (1) À propos, section impact : photos sur les 3 petites cartes, voile uni (plus de dégradé), barre 95 % unie.
(2) Site : dégradés DÉCORATIFS remplacés par des couleurs unies (barre de progression du header, liseré équipe,
séparateurs, connecteurs, halos, fonds provisoires, fondu des chevrons). Les voiles sombres sur photos (lisibilité du texte)
sont conservés. Idempotent."""
import pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent

# ---------- (1) section impact ----------
p = root / 'pages' / 'a-propos.html'; s = p.read_text(encoding='utf-8')
if 'stat-item--photo' not in s:
    s = s.replace('class="stat-item stat-item--feature stat-item--rose"', 'class="stat-item stat-item--feature stat-item--photo stat-item--rose"')
    def photo(n, w, h): return f'<img class="stat-item__photo" src="../assets/images/terrain/terrain-{n}.webp" alt="" aria-hidden="true" loading="lazy" decoding="async" width="{w}" height="{h}" />\n            '
    s = s.replace('<li class="stat-item stat-item--blue">\n            ', '<li class="stat-item stat-item--blue stat-item--photo">\n            ' + photo('37', 1080, 810))
    s = s.replace('<li class="stat-item stat-item--green">\n            ', '<li class="stat-item stat-item--green stat-item--photo">\n            ' + photo('31', 810, 608))
    s = s.replace('<li class="stat-item stat-item--wide stat-item--rose">\n            ', '<li class="stat-item stat-item--wide stat-item--photo stat-item--rose">\n            ' + photo('34', 1080, 810))
    assert s.count('stat-item--photo') == 4
    p.write_text(s, encoding='utf-8')
css = root / 'styles' / 'a-propos.css'; c = css.read_text(encoding='utf-8')
old_scrim = '.impact .stat-item--feature::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(to top,#0E1F38 6%,rgba(14,31,56,0.72) 38%,rgba(14,31,56,0.10) 100%)}'
new_scrim = '.impact .stat-item--photo::after{content:"";position:absolute;inset:0;z-index:-1;background:rgba(14,31,56,0.66)}'
c = c.replace(old_scrim, new_scrim)
c = c.replace('background:linear-gradient(90deg,#C2185B,#F08AA8);transition:width', 'background:var(--clr-primary);transition:width')
css.write_text(c, encoding='utf-8')

# ---------- (2) dégradés décoratifs -> unis ----------
SOLID = {
 '.navbar__progress::after': 'var(--clr-primary)',
 '.team-card--featured::before': 'var(--clr-primary)',
 '.media-placeholder': 'var(--clr-surface)',
 '.campagne-photo': 'var(--clr-surface)',
 '.mission-img': 'var(--clr-accent-soft)',
 '.about__divider-line--left': 'rgba(110,139,123,0.55)',
 '.about__divider-line--right': 'rgba(110,139,123,0.55)',
 '.contact__sep': 'rgba(110,139,123,0.42)',
 '.soutenir__sep': 'var(--clr-border-strong)',
 '.mission::before': 'var(--clr-border-strong)',
 '.mission::after': 'var(--clr-border-strong)',
 '.soutenir__right::before': 'var(--clr-accent)',
 '.dons::after': 'none', '.impact::after': 'none', '.cta-contact__cta::after': 'none',
 '.partners::after': 'none', '.partners-certif::after': 'none',
 '.soutenir__impact-hint': 'none',
}
rule = re.compile(r'([^{}]+)\{([^{}]*gradient\([^{}]*)\}')
n = 0
for f in sorted((root / 'styles').glob('*.css')):
    t = f.read_text(encoding='utf-8')
    if '/* V198 ' in t: continue
    found = {}
    for m in rule.finditer(t):
        sel = ' '.join(m.group(1).split()).split('*/')[-1].strip()
        if sel in SOLID: found[sel] = SOLID[sel]
    if found:
        block = '\n/* V198 Dégradés décoratifs -> couleurs unies (propre, institutionnel) */\n' + ''.join(f'{sel}{{background:{v}}}\n' for sel, v in found.items())
        f.write_text(t.rstrip('\n') + '\n' + block, encoding='utf-8'); n += 1
print('feuilles nettoyées :', n)
