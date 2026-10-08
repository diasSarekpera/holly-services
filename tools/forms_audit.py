"""T11A : audit CSS des champs (hors bloc T11) -> section « Audit CSS (T11A) » de docs/FORMULAIRES.md. Usage: forms_audit.py"""
import re,glob,sys
sys.path.insert(0,'tools')
from css_rules import rules
CL=['form-input','form-select','form-textarea','form-control','benevolat-input','contact-form__input','contact-form__textarea','actualites-nl__input','article-nl__input','search-input','footer__nl-input','erreur404-search input','candidature-layout input','actualites-toolbar__search input']
P=['min-height','height','font-size','padding','border','border-radius','background']
def val(b,k):
    m=re.search(r'(?:^|;)\s*'+k+r'\s*:\s*([^;]+)',b); return m.group(1).strip()[:34] if m else '-'
rows=[]
for c in CL:
    seen={}
    for f in sorted(glob.glob('styles/*.css')):
        s=open(f,encoding='utf8').read(); i=s.find('/* ===== Formulaires (T11)')
        if i>=0: s=s[:i]
        for m,sel,body,a,b in rules(s):
            if m: continue
            if re.search(r'(^|[\s,])\.?'+re.escape(c).replace('\\ ',' ')+r'(?![\w-])(?!:|\[)',sel) and not re.search(r'::?(placeholder|focus|hover|autofill|-webkit|-moz)|__(?!input|textarea)',sel.replace(c,'')) and re.search(r'border|padding|height|font-size',body):
                seen.setdefault((val(body,'min-height') if val(body,'height')=='-' else val(body,'height'),val(body,'font-size'),val(body,'padding'),val(body,'border') if val(body,'border')!='-' else val(body,'border-color'),val(body,'border-radius'),val(body,'background')),[]).append(f[7:-4][:12])
    for k,v in seen.items(): rows.append((c,sorted(set(v)),k))
L=['## Audit CSS (T11A)','','Script : `tools/forms_audit.py` (règles hors @media, hors bloc T11) ; bloc posé par `tools/forms_t11.py apply|hash|measure` (hash `%s`, 21 feuilles).'%open('/tmp/h11').read().strip(),'',
'| Champ | Feuille(s) | Haut. | Police | Padding | Bordure | Rayon | Fond |','|---|---|---|---|---|---|---|---|']
for c,fs,k in rows: L.append('| `%s` | %s | %s |'%(c.replace('|','/'),','.join(fs[:2])+('+' if len(fs)>2 else ''),' | '.join(x.replace('|','/') for x in k)))
L+=['','Constats : 14 familles de champs, 5 hauteurs (40/44/48/56 px ou auto), polices 13,3 / 14 / 15 / 16 px, bordures `--clr-border-strong` / `--clr-field-border` / `--clr-secondary-soft`, rayons `--radius-badge` ou `--radius-sm`, placeholders 0,5 d’opacité (a-propos, home) ; champs de `.candidature-layout` et `.erreur404-search` stylés par descendance.',
'Une règle partagée existante force `border-color:var(--clr-field-border) !important` sur tous les champs (3,65:1, WCAG 1.4.11, DESIGN-TOKENS l.41/132) : le bloc T11 l’adopte au lieu de `rgba(16,35,63,0.25)` (≈1,6:1).','Hors socle : cases, radios, fichier, pot de miel `_gotcha`, `footer__nl-input` (fond marine), `actualites-toolbar__search` (conteneur bordé).']
doc=open('docs/FORMULAIRES.md',encoding='utf8').read(); i=doc.find('## Audit CSS (T11A)')
if i>=0: doc=doc[:i].rstrip('\n')+'\n'
open('docs/FORMULAIRES.md','w',encoding='utf8').write(doc.rstrip('\n')+'\n\n'+'\n'.join(L)+'\n')
print(len(L),'lignes')
