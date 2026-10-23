#!/usr/bin/env python3
"""V182 : relecture exigeante de l'accueil (1/n). Idempotent.
 1. About : image plus haute sur mobile.
 2. Campagnes urgentes : fonds de cartes pleins (fin de l'effet « verre »).
 3. Soutenir : chevrons clignotants indiquant le défilement horizontal des chiffres clés (mobile)."""
import pathlib
root = pathlib.Path(__file__).resolve().parent.parent
p = root / 'index.html'; s = p.read_text(encoding='utf-8')
if 'data-scroll-hint' not in s:
    old = '''      <div class="soutenir__impact-scroller">
        <ul class="soutenir__impact-list" aria-label="Impact de votre soutien">'''
    new = '''      <div class="soutenir__impact-wrap" data-scroll-hint>
      <div class="soutenir__impact-scroller" data-scroll-hint-target>
        <ul class="soutenir__impact-list" aria-label="Impact de votre soutien">'''
    assert old in s
    s = s.replace(old, new)
    old2 = '''          </li>
        </ul>
      </div>

      <div class="soutenir__trust">'''
    new2 = '''          </li>
        </ul>
      </div>
      <span class="soutenir__impact-hint" aria-hidden="true">
        <svg viewBox="0 0 12 22" fill="none"><polyline points="2,3 10,11 2,19"/></svg>
        <svg viewBox="0 0 12 22" fill="none"><polyline points="2,3 10,11 2,19"/></svg>
        <svg viewBox="0 0 12 22" fill="none"><polyline points="2,3 10,11 2,19"/></svg>
      </span>
      </div>

      <div class="soutenir__trust">'''
    assert old2 in s
    s = s.replace(old2, new2)
    tag = '  <script src="scripts/components/hero-mobile.js"></script>\n'
    s = s.replace(tag, tag + '  <script src="scripts/components/scroll-hint.js"></script>\n')
    p.write_text(s, encoding='utf-8')
css = root / 'styles' / 'home.css'; c = css.read_text(encoding='utf-8')
if 'V182' not in c:
    c = c.rstrip('\n') + '''

/* V182 (1/3) About : image plus haute sur mobile */
@media (max-width:767px){.about__visual{height:clamp(300px,64vw,400px)}}
@media (max-width:479px){.about__visual{height:clamp(280px,74vw,330px)}}

/* V182 (2/3) Campagnes urgentes : fonds pleins, sans transparence (fin de l'effet verre) */
.camp-card{background:#162B4C;border:1px solid #2A4872;box-shadow:0 12px 30px rgba(4,10,20,0.32)}
@media (hover:hover){.camp-card:hover{border-color:#3C5F8F}}
.camp-card__progress{background:#0F2039;border-color:#244268}
.camp-chip{background:#1F3A61;border-color:#2F4F7D}
.camp-card__bar-track{background:#2C4872}
.camp-card__cat-overlay{background:#0E1F38}
.camp-card__cat--health{background:#1B3A55;border-color:#2F5C80}
.camp-card__cat--social{background:#44193A;border-color:#6A2A58}
.camp-card__cat--edu{background:#1F3D3A;border-color:#33605A}

/* V182 (3/3) Soutenir : chevrons clignotants = défilement horizontal des chiffres clés */
.soutenir__impact-wrap{position:relative}
.soutenir__impact-hint{position:absolute;top:0;right:0;height:2.1rem;width:4.5rem;display:none;align-items:center;justify-content:flex-end;padding-right:0.15rem;pointer-events:none;background:linear-gradient(to right,rgba(255,255,255,0),#fff 62%)}
.soutenir__impact-hint svg{width:0.8rem;height:1.4rem;margin-left:-0.3rem;stroke:var(--clr-primary);stroke-width:2.4;stroke-linecap:round;stroke-linejoin:round;opacity:0.18;animation:soutenir-chevron 1.5s ease-in-out infinite}
.soutenir__impact-hint svg:nth-child(2){animation-delay:0.2s}
.soutenir__impact-hint svg:nth-child(3){animation-delay:0.4s}
.soutenir__impact-wrap.is-scrollable:not(.is-end) .soutenir__impact-hint{display:flex}
@keyframes soutenir-chevron{0%,100%{opacity:0.18}35%{opacity:1}}
@media (prefers-reduced-motion:reduce){.soutenir__impact-hint svg{animation:none;opacity:0.7}}
'''
    css.write_text(c, encoding='utf-8')
print('ok')
