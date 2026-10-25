#!/usr/bin/env python3
"""V201 : listes des missions (nos-missions) : coches classiques remplacées par des lignes à filet fin
et un repère rond rose (point + halo), tracé en CSS. Idempotent."""
import pathlib, re
ROOT = pathlib.Path(__file__).resolve().parent.parent
HTML = ROOT / 'pages/nos-missions.html'
CSS = ROOT / 'styles/nos-missions.css'
BLOCK = '''
/* V201 Listes des missions : lignes à filet fin + repère rond rose (remplace les coches) */
.mission-list{display:block;margin:1.5rem 0 0;padding:0;list-style:none;border-bottom:1px solid var(--clr-border-strong)}
.mission-list li{display:grid;grid-template-columns:1rem 1fr;align-items:start;column-gap:0.875rem;padding:0.75rem 0;border-top:1px solid var(--clr-border-strong);font-size:var(--fs-body);font-weight:500;line-height:1.5;color:var(--clr-secondary)}
.mission-list li::before{content:"";justify-self:center;width:6px;height:6px;margin-top:0.5625rem;border-radius:var(--radius-full);background:var(--clr-primary);box-shadow:0 0 0 5px var(--clr-primary-soft);transition:box-shadow var(--dur-slow) var(--ease-out)}
@media (hover:hover){.mission-list li:hover::before{box-shadow:0 0 0 7px var(--clr-primary-soft)}}
@media (prefers-reduced-motion:reduce){.mission-list li::before{transition:none}}
'''
h = HTML.read_text(encoding='utf-8')
h2 = re.sub(r'(<li>)<i class="ri-check-line" aria-hidden="true"></i> (<span>)', r'\1\2', h)
HTML.write_text(h2, encoding='utf-8')
c = CSS.read_text(encoding='utf-8')
if '/* V201 Listes des missions' in c:
    c = re.sub(r'\n/\* V201 Listes des missions.*?(?=\Z)', BLOCK, c, flags=re.S)
else:
    c = c.rstrip('\n') + '\n' + BLOCK
CSS.write_text(c, encoding='utf-8')
print('coches retirées :', h.count('ri-check-line') - h2.count('ri-check-line'))
