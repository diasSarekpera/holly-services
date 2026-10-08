"""T10D : regles de sections de fond et residus de cartes (hors bloc T10). Usage: cards_10d_find2.py"""
import re,sys
sys.path.insert(0,'tools')
from css_rules import rules
RX={'action.css':r'\.(actions-current|actions-recent)(\s|,|\{|$)|__img[^{]*\{|\.action-(card|tile):hover \.','nos-missions.css':r'\.(besoins|soutenir)(\s|,|\{|$)|\.(card-besoin|card-soutien)','mission-sante.css':r'\.mission-detail__(section|programs|card)(\s|,|\{|:|-|$)'}
for f,rx in RX.items():
    s=open('styles/'+f,encoding='utf8').read(); s=s[:s.find('/* ===== Cartes (T10)')]
    for m,sel,body,a,b in rules(s):
        sl=re.sub(r'\s+',' ',sel.strip())
        if re.search(rx,sl) and re.search(r'background|border|shadow|transform|padding|transition|radius',body):
            print(f[:6],(m or '-')[:18],sl[:50],'|',re.sub(r'\s+',' ',body)[:150])
