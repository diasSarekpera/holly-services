#!/usr/bin/env python3
"""V186 : À propos, section « Notre impact en chiffres » repensée (direction artistique). Idempotent.
Cartes pleines à liseré coloré, icônes, grande carte photo pour le chiffre phare, barre pour le %, compteur animé."""
import pathlib
root = pathlib.Path(__file__).resolve().parent.parent
p = root / 'pages' / 'a-propos.html'; s = p.read_text(encoding='utf-8')
if 'stat-item__icon' not in s:
    a = s.index('<ul class="stats-banner__list stats-banner__list--impact" role="list">')
    b = s.index('</ul>', a) + len('</ul>')
    ICO = {
     'book':   '<path d="M2 4h6a4 4 0 0 1 4 4v12a3 3 0 0 0-3-3H2z"/><path d="M22 4h-6a4 4 0 0 0-4 4v12a3 3 0 0 1 3-3h7z"/>',
     'school': '<path d="M3 21h18"/><path d="M5 21V9l7-5 7 5v12"/><path d="M9 21v-6h6v6"/>',
     'health': '<rect x="3" y="3" width="18" height="18" rx="4"/><path d="M12 8v8M8 12h8"/>',
     'shield': '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9,12 11,14 15,10"/>',
    }
    def icon(k): return f'<span class="stat-item__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none">{ICO[k]}</svg></span>'
    NEW = f'''<ul class="stats-banner__list stats-banner__list--impact" role="list">
          <li class="stat-item stat-item--feature stat-item--rose">
            <img class="stat-item__photo" src="../assets/images/terrain/terrain-51.webp" alt="" aria-hidden="true" loading="lazy" decoding="async" width="1080" height="810" />
            {icon('book')}
            <span class="stat-item__number" data-count="125000" data-suffix="+">125 000+</span>
            <span class="stat-item__label">Enfants scolarisés</span>
          </li>
          <li class="stat-item stat-item--blue">
            {icon('school')}
            <span class="stat-item__number" data-count="450" data-suffix="+">450+</span>
            <span class="stat-item__label">Écoles soutenues</span>
          </li>
          <li class="stat-item stat-item--green">
            {icon('health')}
            <span class="stat-item__number" data-count="320" data-suffix="+">320+</span>
            <span class="stat-item__label">Centres de santé appuyés</span>
          </li>
          <li class="stat-item stat-item--wide stat-item--rose">
            {icon('shield')}
            <span class="stat-item__number" data-count="95" data-suffix="%">95%</span>
            <span class="stat-item__label">Des fonds sur le terrain</span>
            <span class="stat-item__bar" aria-hidden="true"><span class="stat-item__bar-fill"></span></span>
          </li>
        </ul>'''
    s = s[:a] + NEW + s[b:]
    tag = '  <script src="../scripts/components/back-to-top.js"></script>\n'
    s = s.replace(tag, tag + '  <script src="../scripts/pages/a-propos/count-up.js"></script>\n')
    p.write_text(s, encoding='utf-8')
css = root / 'styles' / 'a-propos.css'; c = css.read_text(encoding='utf-8')
if 'V186' not in c:
    css.write_text(c.rstrip('\n') + '''

/* V186 À propos : « Notre impact en chiffres » : cartes pleines, icônes, carte photo, barre, compteur */
.impact .stats-banner__list--impact{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem;align-items:stretch;justify-content:stretch}
:root body .impact .stats-banner__list--impact .stat-item{--k:#F08AA8;--k-bg:#3A1B3B;--k-bar:#C2185B;position:relative;overflow:hidden;isolation:isolate;display:flex;flex-direction:column;justify-content:flex-end;align-items:flex-start;text-align:left;gap:0.5rem;margin:0;min-width:0;min-height:190px;padding:1.5rem 1.25rem 1.25rem;background:#162B4C;border:1px solid #2A4872;border-radius:var(--radius-card);box-shadow:0 12px 30px rgba(4,10,20,0.32)}
:root body .impact .stats-banner__list--impact .stat-item--blue{--k:#8CB4E0;--k-bg:#1D3A63;--k-bar:#5B9EC9}
:root body .impact .stats-banner__list--impact .stat-item--green{--k:#8CC3AA;--k-bg:#22403A;--k-bar:#6E8B7B}
.impact .stat-item::before{content:"";position:absolute;top:0;left:0;right:0;height:3px;background:var(--k-bar);z-index:2}
.impact .stat-item__icon{width:44px;height:44px;border-radius:var(--radius-card);background:var(--k-bg);display:inline-flex;align-items:center;justify-content:center;flex-shrink:0;margin-bottom:auto;position:relative;z-index:1}
.impact .stat-item__icon svg{width:22px;height:22px;stroke:var(--k);stroke-width:1.75;stroke-linecap:round;stroke-linejoin:round}
:root body .impact .stats-banner__list--impact .stat-item .stat-item__number{font-size:clamp(2.4rem,11vw,3rem);line-height:1;padding:0;margin-top:1rem;color:var(--clr-white);position:relative;z-index:1}
:root body .impact .stats-banner__list--impact .stat-item .stat-item__label{color:#C3CFE1;font-size:var(--fs-xs);letter-spacing:0.08em;line-height:1.45;position:relative;z-index:1}
.impact .stat-item--feature,.impact .stat-item--wide{grid-column:1 / -1}
:root body .impact .stats-banner__list--impact .stat-item--feature{min-height:300px}
:root body .impact .stats-banner__list--impact .stat-item--feature .stat-item__number{font-size:clamp(3.4rem,17vw,4.5rem)}
.impact .stat-item__photo{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center 35%;z-index:-2}
.impact .stat-item--feature::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(to top,#0E1F38 6%,rgba(14,31,56,0.72) 38%,rgba(14,31,56,0.10) 100%)}
.impact .stat-item__bar{display:block;width:100%;height:6px;margin-top:0.5rem;border-radius:999px;background:#2C4872;overflow:hidden;position:relative;z-index:1}
.impact .stat-item__bar-fill{display:block;height:100%;width:95%;border-radius:inherit;background:linear-gradient(90deg,#C2185B,#F08AA8);transition:width 1.4s cubic-bezier(0.22,1,0.36,1)}
.has-countup .impact:not(.is-visible) .stat-item__bar-fill{width:0}
@media (min-width:901px){
  .impact .stats-banner__list--impact{grid-template-columns:1.6fr 1fr 1fr 1fr;gap:1.25rem}
  .impact .stat-item--feature,.impact .stat-item--wide{grid-column:auto}
  :root body .impact .stats-banner__list--impact .stat-item{min-height:320px;padding:1.75rem 1.5rem 1.5rem}
  :root body .impact .stats-banner__list--impact .stat-item:not(.stat-item--wide){padding-bottom:calc(1.5rem + 1.375rem)}
  :root body .impact .stats-banner__list--impact .stat-item .stat-item__number{font-size:clamp(2.6rem,3.6vw,3.25rem)}
  :root body .impact .stats-banner__list--impact .stat-item--feature .stat-item__number{font-size:clamp(3.4rem,5vw,4.5rem)}
}
@media (prefers-reduced-motion:reduce){.impact .stat-item__bar-fill{transition:none}}
''', encoding='utf-8')
print('ok')
