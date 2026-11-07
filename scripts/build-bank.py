"""Compile the local, reviewed Italian question sources into a browser asset.
Country facts: mledoze/countries, ODbL. See data/SOURCES.md.
This script is an offline build step; no question generation service is required.
"""
from pathlib import Path
from fractions import Fraction
import csv, hashlib, json, random, re, unicodedata
ROOT=Path(__file__).resolve().parents[1]
rng=random.Random(5698001)

def rows(file):
    return [line.rsplit('|',1) for line in (ROOT/'data'/file).read_text().splitlines() if line.strip()]

def norm(text):
    return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFD',text.lower()).encode('ascii','ignore').decode())

def qa(question,answer,topic):
    return {'question':question,'answer':str(answer),'topic':topic}

def facts(file,topic):
    return [qa(q,a,topic) for q,a in rows(file)]

history=[]
dates=rows('history-dates.txt')
for event,year in dates:
    history.append(qa(f'In quale anno avvenne questo evento: «{event}»?',year,'date'))
history+=facts('history-facts.txt','personaggi e istituzioni')
pairs=[(a,b) for i,a in enumerate(dates) for b in dates[i+1:] if abs(int(a[1])-int(b[1]))>=10]
rng.shuffle(pairs)
for a,b in pairs[:375-len(history)]:
    left,right=(a,b) if rng.random()<.5 else (b,a)
    answer=min((a,b),key=lambda item:int(item[1]))[0]
    history.append(qa(f'Quale evento avvenne prima: «{left[0]}» oppure «{right[0]}»?',answer,'cronologia'))

culture1=[]
for name,symbol in rows('elements.txt'):
    culture1.append(qa(f'Qual è il simbolo chimico dell’elemento {name.lower()}?',symbol,'chimica'))
for title,author in rows('literature.txt'):
    culture1.append(qa(f'Chi è l’autore dell’opera «{title}»?',author,'letteratura'))
culture1+=facts('science.txt','scienze')

math=[]
for i in range(1,26):
    pct=(i%8+1)*5;base=40+20*i
    math.append(qa(f'Quanto vale il {pct}% di {base}?',base*pct//100,'calcolo'))
    a,b=i+3,i+7
    math.append(qa(f'Quanto misura, in centimetri, il perimetro di un rettangolo con lati di {a} e {b} centimetri?',2*(a+b),'calcolo'))
    base,height=2*(i+3),i+5
    math.append(qa(f'Quanto vale, in centimetri quadrati, l’area di un triangolo con base {base} cm e altezza {height} cm?',base*height//2,'calcolo'))
    n=i+11
    math.append(qa(f'Quanto vale {n} elevato al quadrato?',n*n,'calcolo'))
    minutes=(i%5+1)*10
    math.append(qa(f'A quanti minuti corrispondono {i} ore e {minutes} minuti?',i*60+minutes,'calcolo'))
    denominator=i+3;numerator1=i+1;numerator2=i+2
    result=Fraction(numerator1+numerator2,denominator)
    math.append(qa(f'Qual è il risultato, ridotto ai minimi termini, di {numerator1}/{denominator} + {numerator2}/{denominator}?',str(result),'calcolo'))
    first=i*3;step=i%7+2
    terms=', '.join(str(first+step*j) for j in range(4))
    math.append(qa(f'Qual è il numero successivo nella progressione aritmetica {terms}, mantenendo la stessa differenza?',first+step*4,'calcolo'))
    terms=[i+4,i+10,i+16]
    math.append(qa(f'Qual è la media aritmetica dei numeri {terms[0]}, {terms[1]} e {terms[2]}?',sum(terms)//3,'calcolo'))
culture2=math+facts('language.txt','italiano')+facts('technology.txt','tecnologia')+facts('arts.txt','arte e musica')

countries=[x for x in csv.DictReader((ROOT/'data/countries-source.csv').open()) if x['unMember']=='1']
excluded=set('VAT ISR LKA NRU SWZ ZAF BOL BEN CIV MYS NLD IDN GNQ YEM SDN BDI TZA KIR PLW'.split())
capital_it={
'Yerevan':'Erevan','Brussels':'Bruxelles','Bern':'Berna','Beijing':'Pechino','Havana':'L’Avana','Prague':'Praga','Berlin':'Berlino','Djibouti':'Gibuti','Copenhagen':'Copenaghen','Algiers':'Algeri','Cairo':'Il Cairo','Addis Ababa':'Addis Abeba','Paris':'Parigi','London':'Londra','Athens':'Atene','Guatemala City':'Città del Guatemala','New Delhi':'Nuova Delhi','Dublin':'Dublino','Tehran':'Teheran','Rome':'Roma','South Tarawa':'Tarawa Sud','Kuwait City':'Madinat al-Kuwait','Luxembourg':'Lussemburgo','Mexico City':'Città del Messico','Valletta':'La Valletta','Ulan Bator':'Ulan Bator','Muscat':'Mascate','Panama City':'Città di Panama','Warsaw':'Varsavia','Lisbon':'Lisbona','Bucharest':'Bucarest','Moscow':'Mosca','Riyadh':'Riad','City of San Marino':'San Marino','Mogadishu':'Mogadiscio','Belgrade':'Belgrado','Ljubljana':'Lubiana','Stockholm':'Stoccolma','Damascus':'Damasco','Tunis':'Tunisi','Kyiv':'Kiev','Washington D.C.':'Washington','Vatican City':'Città del Vaticano','Seoul':'Seul'}
country_it={'OMN':'Oman','SSD':'Sudan del Sud','SWZ':'Eswatini','COD':'Repubblica Democratica del Congo','COG':'Repubblica del Congo','MMR':'Myanmar','THA':'Thailandia','ZAF':'Sudafrica'}
geography=[]
for c in countries:
    if c['cca3'] in excluded: continue
    assert c['capital'] and ',' not in c['capital'],c['cca3']
    name=country_it.get(c['cca3'],c['translations.ita.common'])
    capital=capital_it.get(c['capital'],c['capital'])
    geography.append(qa(f'Qual è la capitale del Paese indicato: {name}?',capital,'capitali'))
assert len(geography)==175,len(geography)
transcontinental=set('RUS TUR KAZ AZE GEO ARM CYP EGY IDN VAT'.split())
regions={'Africa':'Africa','Europe':'Europa','Asia':'Asia','Oceania':'Oceania','Americas':'America'}
region_pool=[c for c in countries if c['cca3'] not in transcontinental]
rng.shuffle(region_pool)
for c in region_pool[:150]:
    name=country_it.get(c['cca3'],c['translations.ita.common'])
    geography.append(qa(f'In quale continente si trova principalmente il territorio di questo Paese: {name}?',regions[c['region']],'continenti'))
geography+=facts('geography-facts.txt','geografia fisica e Italia')

categories=[history,culture1,culture2,geography]
all_norms=set();compiled=[]
for s,category in enumerate(categories):
    assert len(category)==375,(s,len(category))
    out=[]
    for row in category:
        q,a,topic=row['question'],row['answer'].strip(),row['topic']
        canonical=norm(q)
        assert canonical not in all_norms,('duplicate question',q)
        all_norms.add(canonical)
        assert a and '?' in q
        if re.fullmatch(r'\d+',a):
            n=int(a);wrong=[str(n+1),str(n+7)]
        elif re.fullmatch(r'\d+/\d+',a):
            f=Fraction(a);wrong=[str(f+1),str(f+2)]
        elif topic=='cronologia':
            other=[event for event,year in dates if ('«'+event+'»') in q and norm(event)!=norm(a)];assert len(other)==1;wrong=other*2
        else:
            wrong=list(dict.fromkeys(x['answer'] for x in category if x['topic']==topic and norm(x['answer'])!=norm(a)))
        assert len(wrong)>=2,(q,wrong)
        rng.shuffle(wrong)
        a_sentence=a if a.endswith(('.',':','!','?')) else a+'.'
        low=a[0].lower()+a[1:] if a.startswith(('Il ','La ','Lo ','Gli ','Le ','Un ','Una ','L’','L\'')) else a
        alternative=(f'Il simbolo è {a}.' if topic=='chimica' else f'L’autore è {a}.' if topic=='letteratura' else f'La capitale è {a}.' if topic=='capitali' else f'È {low}.')
        out.append({'id':'s'+str(s+1)+'-'+hashlib.sha256(canonical.encode()).hexdigest()[:12],'topic':topic,'q':[q,a_sentence,(f'Nel {a}.' if topic=='date' else a),(f'L’evento risale al {a}.' if topic=='date' else alternative),wrong[0]+'.',wrong[1]+'.']})
    compiled.append(out)
asset='/* Italian question bank. Sources and licensing: data/SOURCES.md. */\nwindow.MALWING_BANK='+json.dumps(compiled,ensure_ascii=False,separators=(',',':'))+';\n'
(ROOT/'question-bank.js').write_text(asset)
print('Validated category sizes:',[len(x) for x in compiled])
print('Distinct question IDs:',len({x['id'] for c in compiled for x in c}))
