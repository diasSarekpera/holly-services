#!/usr/bin/env python3
"""V180 : menu mobile = panneau latéral qui glisse depuis la droite (au lieu du plein écran qui descend du haut).
Fond assombri derrière (body.nav-mobile-open::after) ; fermeture au clic extérieur déjà gérée par hero-mobile.js.
Idempotent."""
import pathlib
root = pathlib.Path(__file__).resolve().parent.parent
CSS = '''
/* Menu mobile en panneau latéral, depuis la droite (V180) */
.mobile-menu{inset:0 0 0 auto;width:min(88vw,420px);transform:translateX(100%);border-left:1px solid rgba(255,255,255,0.08);box-shadow:-28px 0 70px rgba(5,12,24,0.5)}
.mobile-menu.is-open{transform:translateX(0)}
@media (prefers-reduced-motion:reduce){.mobile-menu,.mobile-menu.is-open{transform:none}}
@media (max-width:1023px){
  body::after{content:"";position:fixed;inset:0;z-index:calc(var(--z-menu) - 1);background:rgba(8,16,30,0.58);opacity:0;visibility:hidden;pointer-events:none;transition:opacity 0.35s ease,visibility 0s linear 0.35s}
  body.nav-mobile-open::after{opacity:1;visibility:visible;pointer-events:auto;transition:opacity 0.35s ease,visibility 0s linear 0s}
}
'''
c = h = 0
for p in root.glob('styles/*.css'):
    s = p.read_text(encoding='utf-8')
    if '.mobile-menu{position:fixed' in s and 'V180' not in s:
        p.write_text(s.rstrip('\n') + '\n' + CSS, encoding='utf-8'); c += 1
for p in list(root.glob('*.html')) + list(root.glob('pages/*.html')):
    s = p.read_text(encoding='utf-8'); t = s.replace('<!-- Menu mobile plein écran -->', '<!-- Menu mobile : panneau latéral (droite) -->')
    if t != s: p.write_text(t, encoding='utf-8'); h += 1
print(f'CSS : {c} | HTML (commentaire) : {h}')
