import sys,glob,re
sys.path.insert(0,'tools')
from css_rules import rules
BLOCK=r"""/* ===== Boutons (T9) : socle .btn =====
   Variantes : .btn--primary · .btn--ghost (fond clair) · .btn--ghost-light (fond sombre) · .btn--block · tailles .btn--sm / .btn--lg. .btn--submit = .btn--primary de formulaire. Sous 480 px le retour à la ligne est toléré (libellés longs, aucun débordement horizontal). Bloc identique dans toutes les feuilles ; états focus/survol détaillés = T9C. */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:var(--sp-2);box-sizing:border-box;min-height:44px;padding:var(--sp-3) var(--sp-6);font-family:var(--font-body);font-size:var(--fs-base-sm);font-weight:600;line-height:1.2;letter-spacing:0.03em;white-space:nowrap;text-decoration:none;border-radius:var(--radius-sm);border:1.5px solid transparent;cursor:pointer;transition:background var(--transition-cta),border-color var(--transition-cta),color var(--transition-cta),transform var(--transition-cta),box-shadow var(--transition-cta)}
.btn svg{width:1em;height:1em;stroke:currentColor;fill:none;stroke-width:1.75;stroke-linecap:round;stroke-linejoin:round;flex-shrink:0;transition:transform 0.22s ease}
.btn i{font-size:1em;line-height:1;flex-shrink:0}
.btn:hover svg:last-child{transform:translateX(3px)}
.btn:focus-visible{outline:2px solid var(--clr-primary);outline-offset:3px}
.btn--sm{min-height:36px;padding:var(--sp-2) var(--sp-4);font-size:var(--fs-sm)}
.btn--lg{min-height:52px;padding:var(--sp-4) var(--sp-8);font-size:var(--fs-body)}
.btn--block{display:flex;width:100%}
@media(max-width:767px){.btn--sm{min-height:44px;padding:var(--sp-3) var(--sp-6);font-size:var(--fs-base-sm)}}
@media(max-width:479px){.btn{max-width:100%;white-space:normal;text-align:center}}
.btn--primary{background:var(--clr-primary);color:var(--clr-white);border-color:var(--clr-primary);box-shadow:0 2px 8px var(--clr-primary-overlay)}
.btn--primary:hover{background:var(--clr-primary-dark);border-color:var(--clr-primary-dark);box-shadow:0 4px 14px rgba(194,24,91,0.18)}
.btn--ghost{background:transparent;color:var(--clr-text);border-color:var(--clr-border-btn)}
.btn--ghost:hover{background:var(--clr-surface)}
.btn--ghost-light{background:transparent;color:var(--on-dark-text);border-color:var(--on-dark-border)}
.btn--ghost-light:hover{background:rgba(255,255,255,0.08)}
"""
def run(write):
    log=[]
    for f in sorted(glob.glob('styles/*.css')):
        if f.endswith('hero-photo.css'): continue
        s=open(f,encoding='utf8').read();rs=rules(s)
        idx=[i for i,r in enumerate(rs) if r[1].split(':')[0].split(' ')[0] in('.btn','.btn--primary','.btn--ghost') and not r[0]]
        assert idx==list(range(idx[0],idx[-1]+1)) and len(idx)==8,f
        a,b=rs[idx[0]][3],rs[idx[-1]][4]
        cuts=[(a,b,BLOCK.rstrip('\n'))]
        if f.endswith('home.css'):
            for r in rs:
                if r[1] in('.btn--ghost-light','.btn--ghost-light svg','.btn--ghost-light:hover','.btn--submit','.btn--submit svg') and not r[0]:
                    cuts.append((r[3],r[4],''))
        for x,y,t in sorted(cuts,reverse=True):
            s=s[:x]+t+s[y:]
        if write: open(f,'w',encoding='utf8').write(s)
        log.append((f,len(cuts)))
    return log
if __name__=='__main__':
    print(run(True))
