# Provenienza e manutenzione dei dati

Le domande sono formulate in italiano per MalWing. Il file `question-bank.js` è compilato dai file di dati con `python scripts/build-bank.py`. La compilazione controlla identificativi, duplicati e risposte. Il generatore usa un seme deterministico per rendere riproducibile l'asset; l'estrazione svolta nel browser resta casuale.

## Geografia

I dati di base su Paesi, capitali e continenti derivano da [mledoze/countries](https://github.com/mledoze/countries), file [dist/countries.csv](https://github.com/mledoze/countries/blob/master/dist/countries.csv), consultato il 7 novembre 2026. Il dataset originale è conservato in `countries-source.csv`; la licenza Open Database License è riportata in `countries-LICENSE`. I dati geografici derivati restano disponibili ai termini ODbL. Il compilatore aggiunge i nomi italiani delle capitali ed esclude dalle domande sulle capitali i casi con sedi multiple, status controverso o trasferimenti in corso. Non usa l'indicatore `unMember` per formulare domande sull'appartenenza all'ONU. Per i continenti transcontinentali vengono esclusi i casi ambigui.

## Riferimenti di controllo

- Elementi e simboli: [IUPAC, Periodic Table of Elements](https://iupac.org/what-we-do/periodic-table-of-elements/).
- Storia italiana: [Treccani, Risorgimento](https://www.treccani.it/enciclopedia/risorgimento_%28Dizionario-di-Storia%29/).
- Attribuzioni artistiche: [Catalogo generale dei Beni Culturali, Camera degli Sposi](https://www.catalogo.beniculturali.it/itinerario/la-campagna-fotografica-alinari-camera-degli-sposi).

I testi sono formulazioni originali, non riproduzioni di voci enciclopediche. I quesiti di calcolo sono prodotti da operazioni verificabili con aritmetica intera o frazioni esatte. Gli altri file raccolgono nozioni stabili di storia, letteratura, lingua, scienze, arte e tecnologia. I riferimenti sono verifiche mirate e non costituiscono una certificazione esterna di ogni singolo quesito.

## Estrazione

La cronologia è locale al browser. All'avvio effettivo vengono consumate le domande estratte; l'anteprima in sala d'attesa non le consuma. Ogni materia esaurisce le domande non ancora utilizzate prima di avviare un nuovo ciclo. Il confine fra cicli non produce duplicati all'interno della stessa sessione. La ricarica della pagina non azzera la cronologia; la cancellazione dei dati del sito la azzera.
