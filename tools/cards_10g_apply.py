"""T10G : cartes transparence / rapport Dassa / maintenance. Usage: cards_10g_apply.py"""
def rd(f): return open(f,encoding='utf8').read()
def wr(f,s): open(f,'w',encoding='utf8').write(s)
def sub(s,o,n):
    assert s.count(o)==1,(o[:70],s.count(o)); return s.replace(o,n)
def edit(f,pairs):
    s=rd('styles/'+f)
    for o,n in pairs: s=sub(s,o,n)
    wr('styles/'+f,s)
A='var(--clr-section-alt)'
edit('transparence-rapports.css',[
('.transparence-chiffres{background-color:var(--clr-white)}','.transparence-chiffres{background-color:%s}'%A),
('grid-template-columns:repeat(5,1fr);gap:1.5rem','grid-template-columns:repeat(5,1fr);gap:1.25rem'),
('.chiffre-card{background:var(--clr-off-white);padding:2rem 1.5rem;border-radius:var(--radius-card);text-align:center;box-shadow:var(--shadow-md)','.chiffre-card{padding:1.5rem;text-align:center'),
('.transparence-form{background-color:var(--clr-off-white)}','.transparence-form{background-color:%s}'%A),
('.transparence-cta{background-color:var(--clr-accent-soft);','.transparence-cta{background-color:%s;'%A),
('grid-template-columns:repeat(3,1fr);gap:2rem;margin-top:3rem','grid-template-columns:repeat(3,1fr);gap:1.25rem;margin-top:3rem'),
('.cta-card{background:var(--clr-white);padding:2rem;border-radius:var(--radius-card);color:var(--clr-secondary);font-weight:600;box-shadow:var(--shadow-md);transition:transform var(--transition-cta)}','.cta-card{padding:1.5rem;color:var(--clr-secondary);font-weight:600}'),
('.cta-card:hover{transform:translateY(-5px)}',''),
('.cta-card,.doc-item{transition:none}','.doc-item{transition:none}'),
('.cta-card:hover{transform:none}',''),
('.form-card{background:var(--clr-white);padding:3rem;border-radius:var(--radius-card);box-shadow:var(--shadow-md)}','.form-card{padding:3rem}'),
('.gov-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:3rem}','.gov-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:3rem}'),
])
edit('rapport-consultations-dassa.css',[
('grid-template-columns:repeat(4,1fr);gap:1.5rem','grid-template-columns:repeat(4,1fr);gap:1.25rem'),
('.rapport-result-card{background:var(--clr-white);border-radius:var(--radius-card);padding:1.5rem;box-shadow:var(--shadow-md);border:1px solid var(--clr-border-card);display:flex','.rapport-result-card{padding:1.5rem;display:flex'),
('.rapport-summary{background-color:var(--clr-white);','.rapport-summary{background-color:%s;'%A),
('.rapport-sheet{background-color:var(--clr-off-white);border-radius:var(--radius-card);padding:2rem;border:1px solid var(--clr-border)','.rapport-sheet{background:var(--clr-white);border:1px solid var(--clr-border-card);border-radius:var(--radius-card);box-shadow:var(--shadow-card);transition:border-color 0.2s ease,box-shadow 0.2s ease;padding:1.5rem'),
])
s=rd('styles/rapport-consultations-dassa.css')
s=s.rstrip('\n')+'\n.rapport-sheet:hover{border-color:var(--clr-border-hover);box-shadow:var(--shadow-hover);transform:none}\n.rapport-results-band{background-color:%s}\n'%A
wr('styles/rapport-consultations-dassa.css',s)
h=rd('pages/rapport-consultations-dassa.html')
h=sub(h,'    <section class="rapport-results container"','    <div class="rapport-results-band">\n    <section class="rapport-results container"')
i=h.index('<section class="rapport-results container"'); j=h.index('</section>',i)+len('</section>')
h=h[:j]+'\n    </div>'+h[j:]
wr('pages/rapport-consultations-dassa.html',h)
edit('maintenance.css',[
('max-width:300px;background:var(--clr-white);border:1px solid var(--clr-border-card);border-radius:var(--radius-md);padding:1rem 1.25rem;display:flex;flex-direction:column;gap:0.875rem;box-shadow:var(--shadow-card)}','max-width:300px;padding:1rem 1.25rem;display:flex;flex-direction:column;gap:0.875rem}'),
])
s=rd('styles/maintenance.css'); s=s.rstrip('\n')+'\n.maintenance{background-color:%s}\n'%A; wr('styles/maintenance.css',s)
