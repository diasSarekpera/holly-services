"""T11D : mise en page formulaires Temoignage / Transparence / Actualites (feuilles locales, avant le bloc Cartes T10). Usage: forms_11d_apply.py"""
M='/* ===== Cartes (T10)'
BLK={
'styles/actualites.css':'''/* T11D : filtres, recherche, newsletter */
.actualites-filter{display:inline-flex;align-items:center;min-height:44px}
.actualites-nl__interests{display:flex;flex-wrap:wrap;gap:0 var(--rhythm-block);min-width:0;margin:0 0 var(--rhythm-block);padding:0;border:0}
.actualites-nl__interests label,.actualites-nl__consent label{min-height:44px}
.actualites-nl__form .btn[type="submit"]{justify-content:center}
@media (max-width:767px){.actualites-nl__form .btn[type="submit"]{width:100%}.actualites-toolbar__filters{gap:0.5rem}}
''',
'styles/partager-temoignage.css':'''/* T11D : formulaire Temoignage */
@media (max-width:767px){.temoignage-form__submit{width:100%;justify-content:center}}
''',
'styles/transparence-rapports.css':'''/* T11D : demande de rapport + recherche documents */
.docs-toolbar__search{min-height:44px}
@media (max-width:767px){.docs-toolbar__search{width:100%}.transparence-form__form .btn[type="submit"]{width:100%;justify-content:center}}
'''}
for f,b in BLK.items():
    s=open(f,encoding='utf8').read()
    assert 'T11D' not in s; i=s.find(M); assert i>0
    open(f,'w',encoding='utf8').write(s[:i]+b+'\n'+s[i:])
