"""Answer-kind matching for Italian questions; no unrelated random distractors."""
import re,unicodedata

def key(s):
    s=unicodedata.normalize('NFD',str(s).lower())
    return re.sub(r'[^a-z0-9]','',s)

POOLS={
'political_system':['Monarchia','Democrazia','Oligarchia','Repubblica','Assolutismo','Totalitarismo','Apartheid','Autoritarismo'],
'economic_doctrine':['Mercantilismo','Liberismo','Protezionismo','Fisiocrazia'],
'cultural_period':['Medioevo','Umanesimo','Rinascimento','Illuminismo','Ellenismo','Età moderna'],
'person':['Giuseppe Garibaldi','Giuseppe Mazzini','Augusto','Giulio Cesare','Carlo Magno','Napoleone Bonaparte','George Washington','Luigi Einaudi','Nelson Mandela','Alessandro Magno'],
'author':['Dante Alighieri','Giovanni Boccaccio','Alessandro Manzoni','Giacomo Leopardi','Italo Calvino','Luigi Pirandello','William Shakespeare','Jane Austen'],
'artist':['Leonardo da Vinci','Michelangelo Buonarroti','Raffaello Sanzio','Caravaggio','Sandro Botticelli','Pablo Picasso','Claude Monet','Gian Lorenzo Bernini'],
'composer':['Giuseppe Verdi','Giacomo Puccini','Antonio Vivaldi','Wolfgang Amadeus Mozart','Ludwig van Beethoven','Gioachino Rossini','Georges Bizet'],
'scientist':['Isaac Newton','Albert Einstein','Charles Darwin','Gregor Mendel','Galileo Galilei','Carlo Linneo','Marie Curie','Louis Pasteur'],
'dynasty':['I Medici','Gli Sforza','I Borbone','I Savoia','Gli Asburgo','I Carolingi'],
'city':['Roma','Milano','Torino','Napoli','Parigi','Londra','Madrid','Vienna','Berlino','Atene'],
'continent':['Europa','Africa','Asia','America','Oceania','Antartide'],
'river':['Tevere','Arno','Po','Senna','Tamigi','Danubio','Nilo','Tago','Vistola','Moldava'],
'mountain_range':['Alpi','Appennini','Pirenei','Ande','Himalaya','Urali'],
'mountain':['Everest','K2','Kilimangiaro','Aconcagua','Monte Fuji','Monte Bianco'],
'volcano':['Etna','Vesuvio','Stromboli','Krakatoa','Mauna Loa'],
'sea':['Mar Tirreno','Mare Adriatico','Mar Ionio','Mar Ligure','Mar Nero','Mar Baltico'],
'ocean':['Oceano Atlantico','Oceano Pacifico','Oceano Indiano','Oceano Artico','Oceano Antartico'],
'strait':['Stretto di Gibilterra','Stretto di Bering','Stretto di Messina','Stretto di Magellano'],
'canal':['Canale di Suez','Canale di Panama','Canale di Corinto','Canale di Kiel'],
'desert':['Sahara','Gobi','Atacama','Kalahari','Deserto del Namib'],
'forest':['Foresta amazzonica','Foresta del bacino del Congo','Foresta di Bialowieza'],
'island':['Sicilia','Sardegna','Corsica','Madagascar','Creta','Cipro','Islanda'],
'geo_line':['Equatore','Meridiano di Greenwich','Tropico del Cancro','Tropico del Capricorno','Circolo polare artico'],
'coordinate':['Latitudine','Longitudine','Altitudine'],
'planet':['Mercurio','Venere','Terra','Marte','Giove','Saturno','Urano','Nettuno'],
'star':['Sole','Sirio','Vega','Stella Polare','Betelgeuse'],
'galaxy':['Via Lattea','Galassia di Andromeda','Grande Nube di Magellano'],
'moon':['Luna','Europa','Titano','Ganimede','Callisto'],
'celestial_object':['Asteroide','Cometa','Meteorite','Pianeta','Satellite naturale','Stella'],
'astronomy_concept':['Orbita','Rotazione','Rivoluzione','Eclissi solare','Eclissi lunare','Costellazioni','Buco nero','Teoria del Big Bang'],
'organ':['Cuore','Polmoni','Fegato','Pancreas','Reni','Vescica','Cistifellea','Intestino tenue','Stomaco','Cervello'],
'body_structure':['Osso frontale','Femore','Vene','Arterie','Capillari','Alveoli','Diaframma','Retina','Iride','Coclea','Timpano','Nefrone','Cervelletto','Sinapsi','Mielina','Ventricolo sinistro','Arteria polmonare','Scheletro'],
'cell_structure':['Mitocondrio','Cloroplasto','Membrana plasmatica','Nucleo','Ribosoma','Vacuolo'],
'bio_cell':['Globuli rossi','Globuli bianchi','Piastrine','Neuroni','Coni','Bastoncelli'],
'molecule':['DNA','RNA','Desossiribosio','Ribosio','Uracile','Timina','Guanina','Adenina','Citosina','Clorofilla','Emoglobina','Insulina','Glucagone','Enzimi','Proteine','Chitina'],
'gas':['Ossigeno','Azoto','Anidride carbonica','Elio','Argon','Idrogeno'],
'plant_tissue':['Xilema','Floema','Epidermide','Meristema'],
'bio_process':['Mitosi','Meiosi','Fotosintesi','Traspirazione','Metamorfosi','Impollinazione','Germinazione','Riproduzione sessuata','Selezione naturale'],
'biology_kind':['Autotrofo','Eterotrofo','Erbivoro','Onnivoro','Carnivoro','Invertebrato','Vertebrato','Decompositori'],
'animal_group':['Mammiferi','Anfibi','Rettili','Uccelli','Pesci','Echinodermi','Molluschi','Artropodi'],
'ecology_concept':['Popolazione','Comunità biologica','Ecosistema','Biodiversità','Mutualismo','Parassitismo','Predazione','Competizione'],
'discipline':['Biologia','Botanica','Zoologia','Micologia','Ecologia','Fisica','Chimica','Geologia','Astronomia'],
'unit':['Newton','Joule','Watt','Pascal','Hertz','Coulomb','Volt','Ohm','Ampere','Kelvin','Anno luce','Metro','Secondo'],
'physical_quantity':['Densità','Velocità media','Accelerazione','Pressione','Potenza','Forza','Energia','Massa','Volume'],
'physical_concept':['Attrito','Inerzia','Terzo principio della dinamica','Rifrazione','Riflessione','Dispersione','Lente convessa','Eco','Ultrasuoni','Energia cinetica','Energia potenziale gravitazionale'],
'phase_change':['Fusione','Solidificazione','Condensazione','Sublimazione','Brinamento','Evaporazione'],
'particle':['Elettrone','Protone','Neutrone','Fotone'],
'chemistry_concept':['Elemento chimico','Composto','Isotopi','Ione','Legame covalente','Legame ionico','Solvente','Soluto','Miscuglio'],
'separation_process':['Distillazione','Filtrazione','Decantazione','Centrifugazione','Cristallizzazione'],
'word_plural':['Case','Libri','Uomini','Uova','Temi','Dita','Archi','Banche','Province','Ciliegie'],
'verb_form':['Essere','Avere','Andare','Scrivere','Vedere','Preso','Letto','Aperto','Chiuso','Detto','Fatto','Scelto','Risposto','Essendo','Avendo'],
'grammar_mood':['Indicativo','Congiuntivo','Condizionale','Imperativo','Infinito','Participio','Gerundio'],
'grammar_tense':['Presente','Imperfetto','Passato prossimo','Passato remoto','Trapassato prossimo','Trapassato remoto','Futuro semplice','Futuro anteriore'],
'part_of_speech':['Nome','Pronome','Aggettivo','Avverbio','Congiunzione','Preposizione','Articolo determinativo','Verbo','Interiezione'],
'punctuation':['Punto interrogativo','Punto esclamativo','Punto fermo','Virgola','Punto e virgola','Due punti'],
'hardware':['CPU','GPU','RAM','Tastiera','Scanner','Stampante','Monitor','Mouse','Microfono','SSD','Router','Disco rigido'],
'acronym':['URL','HTTPS','HTTP','DNS','LAN','WAN','OTP','IP','USB','TCP'],
'file_format':['TXT','PDF','DOCX','XLSX','CSV','JSON','PNG','JPEG','ZIP','MP3'],
'language':['HTML','CSS','JavaScript','SQL','Python','Java','C++'],
'license':['Licenza libera','Licenza proprietaria','Licenza freeware','Licenza shareware'],
'it_concept':['Sistema operativo','Browser','Motore di ricerca','Wi-Fi','Bluetooth','Backup','Cifratura','Phishing','Malware','Ransomware','Firewall','Password','Autenticazione a due fattori','Patch','Bit','Sistema binario','Database','Debugging','Algoritmo','Bug','Diritto d’autore','Cloud computing'],
'instrument':['Violino','Chitarra','Pianoforte','Trombone','Flauto','Clarinetto','Tromba','Violoncello'],
'note_value':['Semibreve','Minima','Semiminima','Croma','Semicroma'],
'history_concept':['Feudalesimo','Rinascimento','Umanesimo','Illuminismo','Assolutismo','Mercantilismo','Restaurazione','Risorgimento','Imperialismo','Colonialismo','Nazionalismo','Totalitarismo','Democrazia','Oligarchia','Monarchia','Guerra fredda','Decolonizzazione'],
'religion':['Cristianesimo','Islam','Ebraismo','Buddismo','Induismo'],
'religious_order':['Benedettini','Francescani','Domenicani','Gesuiti'],
'historical_group':['Patrizi','Plebe','Iloti','Servi della gleba','Proletariato','Terzo stato','Amanuensi'],
'historical_institution':['Senato','Consoli','Censore','Pretore','Tribunato della plebe','Gerusia','Stati generali','Corporazioni','Sindacato','Monastero'],
}
POOLS.update({
'bio_fluid':['Plasma','Sangue','Linfa','Liquido cerebrospinale'],
'sense':['Olfatto','Gusto','Vista','Udito','Tatto'],
'body_covering':['Esoscheletro','Cuticola','Epidermide','Endoscheletro'],
'optical_instrument':['Microscopio','Telescopio','Binocolo','Lente d’ingrandimento'],
'infinitive':['Essere','Avere','Andare','Scrivere','Vedere','Leggere','Prendere'],
'participle':['Preso','Letto','Aperto','Chiuso','Detto','Fatto','Scelto','Risposto'],
'gerund':['Essendo','Avendo','Andando','Scrivendo','Vedendo','Leggendo'],
'human_language':['Latino','Greco','Aramaico','Sanscrito','Egizio','Accadico'],
'military_unit':['Legione','Coorte','Centuria','Manipolo'],
'latin_motto':['Ora et labora','Carpe diem','E pluribus unum'],
'historical_place':['Polis','Agorà','Acropoli','Limes','Scriptorium'],
})
LOOKUP={key(a):t for t,values in POOLS.items() for a in values}
PEOPLE=r'generale|condottiero|faraone|faraona|regina|legislatore|imperatore|storico|uomo politico|re |schiavo|filosofo|papa|sovrano|sovrana|viaggiatore|donna|sultano|figlia|monarca|zar |riformatore|teologo|navigatore|esploratore|conquistatore|rivoluzionario|giornalista|comandante|ammiraglio|diplomatico|patriota|statista|presidente|infermiera|filantropo|suffragetta|dirigente|leader|dittatore|attivista|cancelliere|sindacalista|politico|magistrato|astronauta|cosmonauta'

def answer_type(row):
    q,a,t=row['question'],row['answer'],row['topic'];low=q.lower()
    if t=='date':return 'year'
    if t=='cronologia':return 'event'
    if t=='chimica':return 'chemical_symbol'
    if t=='letteratura':return 'author'
    if t=='capitali' or 'capoluogo' in low:return 'city'
    if t=='continenti':return 'continent'
    if t=='calcolo':return 'fraction' if '/' in a else 'number'
    if re.fullmatch(r'\d+',a):return 'number'
    if t=='personaggi e istituzioni':
        if low.startswith('chi ') or re.match('quale ('+PEOPLE+')',low):return 'person'
        if 'dinastia' in low or 'famiglia governò' in low:return 'dynasty'
        if any(x in low for x in ['sistema politico','forma di governo','dottrina politica','regime di segregazione','forma di dittatura']):return 'political_system'
        if 'dottrina economica' in low:return 'economic_doctrine'
        if any(x in low for x in ['movimento culturale','stagione culturale','periodo successivo']):return 'cultural_period'
        return LOOKUP.get(key(a),'history_concept')
    if t=='italiano':
        if low.startswith('nella frase'):return 'sentence_fragment'
        if 'plurale' in low:return 'word_plural'
        if 'infinito' in low:return 'infinitive'
        if 'participio passato' in low:return 'participle'
        if 'gerundio presente' in low:return 'gerund'
        if 'modo verbale' in low:return 'grammar_mood'
        if "tempo dell'indicativo" in low:return 'grammar_tense'
        if 'segno di punteggiatura' in low:return 'punctuation'
        return 'part_of_speech'
    if t=='arte e musica':
        if low.startswith('chi compose'):return 'composer'
        if low.startswith('chi '):return 'artist'
        return LOOKUP.get(key(a),'instrument')
    if t=='geografia fisica e Italia':
        for term,kind in [('fiume','river'),('catena montuosa','mountain_range'),('monte','mountain'),('vetta','mountain'),('vulcano','volcano'),('mare','sea'),('oceano','ocean'),('stretto','strait'),('canale','canal'),('deserto','desert'),('foresta','forest'),('isola','island'),('continente','continent'),('linea immaginaria','geo_line'),('meridiano','geo_line')]:
            if term in low:return kind
        return LOOKUP.get(key(a),'coordinate')
    if t=='tecnologia':
        if 'estensione' in low or low.startswith('quale formato'):return 'file_format'
        if 'sigla' in low:return 'acronym'
        if 'licenza' in low:return 'license'
        if 'linguaggio' in low:return 'language'
        return LOOKUP.get(key(a),'it_concept')
    if t=='scienze':
        if re.match(r'quale (naturalista|monaco|scienziato)',low):return 'scientist'
        return LOOKUP.get(key(a),'body_structure')
    raise ValueError('Unclassified question: '+q)

def distractors(row,all_rows,rng):
    q,a=row['question'],row['answer'];kind=answer_type(row)
    if kind in ('year','number'):
        n=int(a);return [str(n+1),str(n+7)]
    if kind=='fraction':
        from fractions import Fraction
        n=Fraction(a);return [str(n+1),str(n+2)]
    if kind=='event':
        other=[x for x in re.findall('«(.*?)»',q) if key(x)!=key(a)];assert len(other)==1
        return other*2
    if kind=='word_plural':
        noun=re.search(r'plurale di (\w+)',q,re.I).group(1)
        stem=noun[:-1]
        options=[noun,stem+'i',stem+'e',stem+'hi',stem+'he',stem+'ii',stem+'ie']
        options=list({key(x):x for x in options if key(x)!=key(a)}.values())
        return options[:2]
    if kind=='sentence_fragment':
        sentence=re.search('«(.*?)»',q).group(1)
        words=sentence.split();options=words+[' '.join(words[i:i+2]) for i in range(len(words)-1)]
    else:
        options=[r['answer'] for r in all_rows if answer_type(r)==kind]+POOLS.get(kind,[])
    # Names, codes and forms remain inside the requested semantic category.
    # Exclude alternate spellings of the official answer, rather than marking them wrong.
    aliases=[{'newton','isaacnewton'},{'darwin','charlesdarwin'},{'latino','lingualatina'},{'greco','linguagreca'},{'michelangelo','michelangelobuonarroti'},{'o','ossigeno'},{'articolodeterminativo','articolo'}]
    blocked={key(a)}
    for group in aliases:
        if key(a) in group:blocked|=group
    unique={key(x):x for x in options if key(x) not in blocked and x.strip()}
    assert len(unique)>=2,(kind,q,a)
    options=list(unique.values());rng.shuffle(options);return options[:2]
