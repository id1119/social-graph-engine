# Totalna specifikacija projekta 2 iz Algoritama i struktura podataka

Izvori objedinjeni u ovom dokumentu:

- `specifications/АСП Пројекат 2.pdf`
- `specifications/АСП Пројекат 2.pptx`
- `specifications/Често постављана питања.pdf`

Originalna specifikacija ima poslednju izmenu: **11.06.2026.**

## 1. Tema projekta

Potrebno je implementirati konzolnu aplikaciju koja simulira rad dela drustvene mreze.

Aplikacija treba da:

- ucita korisnike, veze pracenja i blokiranja iz prilozenih fajlova;
- izgradi efikasne strukture podataka za rad nad grafom drustvene mreze;
- podrzi pretragu korisnika;
- izracuna i koristi PageRank;
- podrzi dodavanje novih follow veza;
- evidentira istoriju interakcija;
- za dodatne poene podrzi autocomplete, preporuke, BFS obilazak, "Did you mean", blokiranja, dokumentaciju i efikasan rad nad vecim skupovima podataka.

Interfejs treba da bude **tekstualni meni u konzoli**. Graficki interfejs nije potreban.

## 2. Prilozeni skup podataka

Uz zadatak se dobijaju fajlovi:

- `users.txt`
- `connections.txt`
- `blocked.txt`

Obavezno je koristiti prilozeni skup podataka. Studenti ne treba sami da preuzimaju SNAP dataset niti da sami prave sinteticki skup podataka.

Skup podataka je podeljen u tri velicine:

- `small` - preporucen za razvoj i brzo testiranje;
- `medium` - preporucen za demonstraciju interaktivnog rada;
- `full` - koristi se za proveru performansi algoritama nad velikim brojem podataka.

Aplikacija mora raditi nad sve tri velicine skupa.

Skup podataka je formiran kombinovanjem realne strukture grafa drustvene mreze i realisticnih korisnickih profila. Veze predstavljaju usmereni graf pracenja. Korisnicka imena i opisi profila su pripremljeni tako da omoguce smisleno testiranje pretrage, autocomplete funkcionalnosti i hibridnih preporuka.

## 3. Format ulaznih fajlova

### 3.1 `users.txt`

Format:

```text
id|username|bio
```

Znacenje polja:

- `id` je jedinstveni identifikator korisnika;
- `username` je korisnicko ime;
- `bio` je tekstualni opis profila korisnika.

Biografija se koristi za:

- pretragu po kljucnim recima;
- inverted index;
- racunanje slicnosti korisnika kod hibridnih preporuka.

### 3.2 `connections.txt`

Format:

```text
from_id|to_id
```

Znacenje polja:

- `from_id` je korisnik koji prati;
- `to_id` je korisnik koji je pracen.

Graf je usmeren. Veza `from_id|to_id` znaci da `from_id` prati `to_id`, ali ne znaci da `to_id` prati `from_id`.

### 3.3 `blocked.txt`

Format:

```text
blocker_id|blocked_id
```

Znacenje polja:

- `blocker_id` je korisnik koji je blokirao drugog korisnika;
- `blocked_id` je korisnik koji je blokiran.

Blokiranje nije globalno svojstvo korisnika, vec odnos izmedju dva korisnika.

Blokirane korisnike ne treba brisati iz grafa.

## 4. Inicijalizacija programa i strukture podataka

Pri pokretanju programa treba ucitati sadrzaj fajlova i kreirati strukture podataka za efikasno:

- pretrazivanje;
- rangiranje;
- preporucivanje korisnika;
- obilazak grafa;
- proveru blokiranja;
- prikaz istorije interakcija.

Aplikacija ne treba da ponovo ucitava fajlove i ponovo formira strukture pri svakoj operaciji. Po pokretanju programa pozeljno je formirati sve potrebne strukture za pretragu, rangiranje, preporuke i BFS obilazak.

Iz prezentacije postoji dodatna napomena da je potrebno sve strukture podataka kreirati unapred i serijalizovati, a pri pokretanju programa ih samo ucitavati. Kao preporucen Python modul naveden je `pickle`: https://docs.python.org/3/library/pickle.html

Prakticno tumacenje zahteva:

- program svakako mora umeti da izgradi strukture iz ulaznih fajlova;
- moze se dodati kesiranje/serijalizacija struktura radi brzeg pokretanja;
- ako se koristi kes, treba voditi racuna da odgovara ulaznim fajlovima;
- PageRank i strukture moraju ostati korektni nakon dodavanja korisnika ili follow veze tokom rada programa.

## 5. Osnovni deo projekta - do 10 poena

Za osnovni deo treba implementirati zadatke 1, 2, 3, 4 i 5.

### 5.1 Zadatak 1 - Izgradnja grafa drustvene mreze, 2 poena

Potrebno je kreirati klase:

- `User`
- `SocialGraph`

Za svakog korisnika cuvati:

- jedinstveni identifikator;
- korisnicko ime;
- biografiju.

Veze pracenja treba predstaviti usmerenim grafom.

Potrebno je omoguciti efikasno cuvanje:

- izlaznih veza svakog korisnika, odnosno koga korisnik prati;
- ulaznih veza svakog korisnika, odnosno ko prati korisnika;
- izlaznog stepena svakog korisnika.

Za brzo pronalazenje korisnika treba koristiti hash mape, u Pythonu tipicno `dict`.

Preporucene interne strukture:

- `users_by_id: dict[id, User]`
- `users_by_username_lower: dict[str, User]`
- `following: dict[id, set[id]]`
- `followers: dict[id, set[id]]`
- `out_degree: dict[id, int]`
- strukture za blokiranja, na primer `blocked_by_user` i/ili parovi blokiranja.

Dozvoljeno je koristiti standardne Python strukture podataka kao sto su `dict`, `set`, `list`, `deque` i `heap`.

### 5.2 Zadatak 2 - Rangiranje uticaja korisnika PageRank algoritmom, 3 poena

Potrebno je implementirati iterativni PageRank algoritam nad grafom pracenja.

Zahtevi:

- PageRank se racuna nad usmerenim grafom pracenja;
- damping factor treba da bude `0.85`;
- algoritam se zaustavlja kada se dostigne konvergencija, na primer `epsilon = 1e-6`;
- treba omoguciti prikaz najuticajnijih korisnika;
- za prikaz top rezultata treba koristiti heap.

PageRank ne sme biti zamenjen prostim brojanjem pratilaca. Broj pratilaca moze biti dodatna informacija, ali nije zamena za PageRank. PageRank uzima u obzir i znacaj korisnika koji prave veze.

Intuicija:

- korisnik je uticajniji ako ka njemu vodi vise vaznih veza;
- linkovi/v veze sa bitnih cvorova vrede vise;
- ako cvor `i` ima rang `r_i` i `d_i` izlaznih linkova, svaki izlazni link prenosi `r_i / d_i` uticaja;
- uticaj cvora `j` je suma doprinosa ulaznih linkova.

Formula bez damping faktora iz prezentacije:

```text
r_j = sum over i -> j of r_i / d_i
```

Power iteration iz prezentacije:

```text
set r_j <- 1 / N
repeat:
    r'_j <- sum over i -> j of r_i / d_i
    if |r - r'| <= epsilon:
        stop
    r <- r'
```

U projektu treba koristiti verziju sa damping faktorom i teleportacijom:

```text
PR(j) = (1 - d) / N + d * sum over i -> j of PR(i) / out_degree(i)
```

gde je:

- `d = 0.85`;
- `N` broj korisnika/cvorova;
- `out_degree(i)` broj korisnika koje `i` prati.

Treba voditi racuna o PageRank problemima pomenutim u prezentaciji:

- `spider trap` - grupa/cvor zadrzava rang zbog zatvorene strukture;
- `dead end` - cvor bez izlaznih linkova;
- resenje je teleportacija, odnosno sansa da se poseti bilo koja stranica/cvor.

PageRank se inicijalno racuna nakon ucitavanja grafa.

Nakon dodavanja novog korisnika ili nove follow veze potrebno je ponovo izracunati PageRank.

Dozvoljeno je:

- koristiti prethodno izracunate PageRank vrednosti kao pocetnu tacku za novo racunanje, odnosno `warm start`;
- koristiti kesirane PageRank vrednosti ako su prilozene.

I pored eventualnog kesa, program treba da ume da:

- izracuna PageRank nad grafom;
- ponovo ga izracuna nakon dodavanja novog korisnika ili follow veze.

### 5.3 Zadatak 3 - Pretraga korisnika, 2 poena

Treba omoguciti pretragu korisnika:

- po korisnickom imenu;
- po recima iz biografije.

Pretraga treba da bude case insensitive:

- pretraga po korisnickom imenu;
- pretraga po biografiji;
- autocomplete;
- "Did you mean".

Za biografiju treba izvrsiti jednostavnu obradu teksta, na primer:

- prebacivanje u mala slova;
- uklanjanje nepotrebnih znakova;
- izdvajanje reci.

Biografija je obican tekstualni opis profila. Ne ocekuje se posebna rucno oznacena lista kljucnih reci.

Primer:

```text
Machine learning researcher and Python developer
```

Korisnik sa ovom biografijom treba da bude pronadjen upitima:

- `machine`
- `learning`
- `researcher`
- `python`

Za efikasnu pretragu po recima iz biografije treba formirati inverted index.

Inverted index je struktura koja mapira svaku rec na listu ili skup korisnika cije biografije sadrze tu rec.

Primer:

```text
python -> {5, 17, 42}
```

Pretraga po biografiji treba da pronadje korisnike cije biografije sadrze reci iz upita. Dovoljno je implementirati osnovnu varijantu preko text processing-a i inverted index-a. Dozvoljena je naprednija varijanta, ali nije neophodna.

Rezultate pretrage treba rangirati na osnovu:

- relevantnosti upita;
- PageRank vrednosti korisnika.

Opsti princip rangiranja:

- prvo prikazati relevantnije rezultate;
- ako je relevantnost slicna, korisnici sa vecom PageRank vrednoscu treba da budu prikazani ranije.

Za prikaz top rezultata treba koristiti heap.

Iz prezentacije: pozeljno je oznaciti korisnicki unos u rezultatima pretrage.

Ako je pretraga implementirana iz perspektive konkretnog korisnika, FAQ navodi da blokiranje treba uzeti u obzir i pri pretrazi.

### 5.4 Zadatak 4 - Istorija interakcija i dodavanje novih veza, 2 poena

Treba evidentirati dodavanje novih follow veza.

Za zadatog korisnika treba omoguciti prikaz istorije interakcija:

- korisnika koje je on zapratio;
- korisnika koji su njega zapratili.

Ispise treba prikazati u hronoloskom redosledu.

Za cuvanje istorije mogu se koristiti odgovarajuce strukture podataka, na primer:

- liste dogadjaja;
- redovi;
- vremenski oznaceni zapisi;
- posebne mape po korisniku za outgoing i incoming interakcije.

Kod dodavanja nove follow veze treba:

- proveriti da li oba korisnika postoje;
- proveriti da veza vec ne postoji, ako je to deo odbrane konzistentnosti;
- proveriti blokiranja ako je implementiran zadatak 10;
- dodati vezu u izlazne i ulazne strukture grafa;
- azurirati izlazni stepen;
- evidentirati dogadjaj u istoriji oba relevantna korisnika;
- ponovo izracunati PageRank.

Nije neophodno cuvati izmene nazad u fajlove. Dovoljno je da se izmene, kao sto su dodavanje nove follow veze ili azuriranje PageRank-a, korektno odrzavaju tokom jednog pokretanja programa.

### 5.5 Zadatak 5 - Tekstualni meni, 1 poen

Treba omoguciti korisniku da preko tekstualnog menija bira opcije za:

- pretragu;
- prikaz najuticajnijih korisnika;
- dodavanje nove follow veze;
- prikaz istorije interakcija;
- izlazak iz programa.

Ako su implementirane dodatne funkcionalnosti, meni treba prosiriti opcijama za:

- autocomplete;
- hibridne preporuke;
- BFS obilazak;
- "Did you mean";
- rad sa blokiranim korisnicima ako postoji posebna opcija prikaza;
- eventualno izbor dataset-a ili putanja do fajlova.

## 6. Dodatni deo projekta - do ukupno 25 poena

Ukupan projekat nosi 25 poena.

Dodatni deo obuhvata zadatke 6-12. Rezultate pretrage, autocomplete-a i preporuka treba prikazivati rangirano:

- prvo relevantniji rezultati;
- kod slicne relevantnosti korisnici sa vecom PageRank vrednoscu;
- PageRank predstavlja meru uticaja korisnika u grafu pracenja.

### 6.1 Zadatak 6 - Trie i autocomplete, 3 poena

Treba podrzati efikasnu prefiksnu pretragu korisnickih imena pomocu strukture podataka `trie`.

Trie je prefiksno stablo. Primarno se koristi za autocomplete korisnickih imena.

Kada korisnik odabere autocomplete opciju, treba mu ponuditi nekoliko popularnih zavrsetaka zadatog upita.

Primer:

```text
mar*
```

Moguce ponudjene opcije:

- `marko_ai`
- `maria_dev`
- `marketing_notes`

Konkretni rezultati zavise od postojecih korisnickih imena.

Zahtevi:

- pretraga radi case insensitive;
- rezultati moraju odgovarati zadatom prefiksu;
- rezultati ne treba da budu proizvoljno poredjani;
- rezultate treba sortirati po PageRank vrednosti korisnika;
- prvo prikazati uticajnije korisnike.

Dozvoljeno je koristiti trie i u drugim delovima projekta ako je korisno.

### 6.2 Zadatak 7 - Hibridne preporuke korisnika, 2 poena

Za zadatog korisnika treba predloziti korisnike koje jos ne prati, a koji su relevantni na osnovu:

- grafa pracenja;
- sadrzaja biografija.

Preporuka kombinuje:

- Personalized PageRank iz perspektive zadatog korisnika;
- slicnost biografija.

Kombinovani skor:

```text
alpha * PPR + (1 - alpha) * content_similarity
```

Korisniku treba omoguciti da izabere vrednost parametra `alpha`.

Tumacenje `alpha`:

- ako je `alpha` blize `1`, preporuka se vise oslanja na graf;
- ako je `alpha` blize `0`, preporuka se vise oslanja na sadrzaj biografija.

Preporuke ne smeju da prikazu:

- samog zadatog korisnika;
- korisnike koje zadati korisnik vec prati;
- korisnike koje je zadati korisnik blokirao;
- korisnike koji su blokirali zadatog korisnika.

#### 6.2.1 Personalized PageRank

Personalized PageRank je varijanta PageRank algoritma koja rangira korisnike iz perspektive jednog zadatog korisnika.

Kod obicnog PageRank-a znacaj se racuna globalno za celu mrezu. Kod PPR-a postoji pocetni korisnik i rangiranje treba da pokaze koji su korisnici relevantniji bas za njega.

Intuitivno, PPR je nasumicna setnja kroz graf u kojoj postoji verovatnoca da se setnja vrati nazad na pocetnog korisnika i ponovo krene od njegovog cvora. Zbog toga korisnici koji su blizi pocetnom korisniku ili su vazni u njegovom delu mreze dobijaju veci skor.

PPR ne zamenjuje obican PageRank:

- obican PageRank je potreban za globalno rangiranje uticaja;
- PPR se koristi za personalizovane hibridne preporuke.

#### 6.2.2 Slicnost biografija

Slicnost biografija moze se racunati pomocu:

- Jaccard slicnosti;
- jednostavne Cosine slicnosti;
- neke druge mere slicnosti teksta po izboru studenta.

Student treba da razume i objasni izabranu meru.

Jaccard slicnost:

- svaka biografija se predstavi kao skup reci;
- broj zajednickih reci podeli se brojem razlicitih reci koje se pojavljuju u bar jednoj od dve biografije;
- veca vrednost znaci slicnije biografije.

Formula:

```text
J(A, B) = |A intersection B| / |A union B|
```

Primer:

```text
A = {python, ai, music}
B = {python, data, ai}
A intersection B = {python, ai}
A union B = {python, ai, music, data}
J(A, B) = 2 / 4 = 0.5
```

Cosine slicnost:

- svaka biografija se predstavi kao vektor reci;
- vrednosti u vektoru mogu biti broj pojavljivanja reci;
- alternativno vrednosti mogu biti `0/1`, gde oznacavaju da li se rec pojavljuje;
- slicnost je kosinus ugla izmedju dva vektora.

Formula:

```text
Cosine(A, B) = (A dot B) / (||A|| * ||B||)
```

Nije neophodno koristiti napredne NLP biblioteke.

### 6.3 Zadatak 8 - Obilazak mreze BFS algoritmom, 3 poena

Treba implementirati obilazak grafa pracenja pomocu BFS algoritma.

Za zadatog korisnika treba prikazati:

- prve konekcije;
- druge konekcije;
- trece konekcije;
- dalje konekcije do nivoa koji korisnik zada.

Korisnik moze da zada maksimalni nivo do kog se vrsi pretraga.

Znacenje nivoa:

- nivo 1 - direktne follow veze, odnosno korisnici do kojih se stize jednom follow vezom;
- nivo 2 - korisnici do kojih se stize preko jednog posrednika;
- nivo 3 - korisnici do kojih se stize preko dva posrednika;
- nivo `k` - korisnici udaljeni `k` follow koraka od pocetnog korisnika.

Ako korisnik zada nivo 3, program treba da prikaze prve, druge i trece konekcije.

Treba voditi racuna da se isti korisnik ne obradjuje vise puta.

Preporucena struktura za BFS:

- `deque` za red;
- `visited` skup;
- mapa `level -> list/users` za prikaz po udaljenosti.

### 6.4 Zadatak 9 - "Did you mean", 3 poena

Ako je prilikom unosa korisnickog imena doslo do greske, odnosno ako zadati korisnik ne postoji, treba ponuditi nekoliko slicnih ispravnih mogucnosti.

Zahtevi:

- funkcionalnost radi case insensitive;
- nije potrebno da prvih nekoliko karaktera korisnickog imena bude isto;
- treba ponuditi nekoliko slicnih ispravnih korisnickih imena.

Dozvoljeno je:

- koristiti biblioteku za ovu funkcionalnost;
- samostalno implementirati algoritam.

Moguci pristupi:

- Levenshtein/edit distance;
- difflib iz standardne biblioteke;
- kombinacija prefiksa i distance;
- rangiranje slicnosti uz PageRank kao dodatni kriterijum.

### 6.5 Zadatak 10 - Blokirani korisnici, 2 poena

Treba ucitati podatke iz `blocked.txt` o tome koji korisnik je blokirao kog drugog korisnika.

Blokirane korisnike ne treba potpuno izbaciti iz grafa.

Blokiranje treba uzeti u obzir:

- pri preporukama;
- pri dodavanju novih veza;
- pri pretrazi ako je pretraga implementirana iz perspektive konkretnog korisnika.

Pri preporuci korisnika ne prikazivati:

- korisnike koje je zadati korisnik blokirao;
- korisnike koji su blokirali zadatog korisnika.

Pri dodavanju nove follow veze:

- proveriti da li izmedju ta dva korisnika postoji blokiranje u bilo kom smeru;
- ako blokiranje postoji, zabraniti dodavanje veze;
- prikazati adekvatno obavestenje.

Primer:

- ako je korisnik `A` blokirao korisnika `B`, onda `B` ne treba preporucivati korisniku `A`;
- ako postoji blokiranje izmedju `A` i `B` u bilo kom smeru, ne treba dozvoliti dodavanje nove follow veze izmedju njih.

### 6.6 Zadatak 11 - Kvalitet koda, OOP i dokumentacija, 1 poen

Kod treba da bude:

- jasno organizovan;
- podeljen u klase i funkcije;
- bez nepotrebnog ponavljanja;
- objektno orijentisan tamo gde je to prirodno;
- razumljiv za odbranu i odrzavanje.

Obavezno je priloziti `README.md`.

`README.md` treba da sadrzi:

- kratko objasnjenje projekta;
- nacin pokretanja programa;
- opis potrebnih ulaznih fajlova;
- format podataka;
- spisak implementiranih funkcionalnosti.

Pozeljno je navesti:

- primer korisnika za pretragu;
- primer prefiksa za autocomplete;
- primer korisnika za BFS;
- primer korisnika za preporuke.

### 6.7 Zadatak 12 - Efikasan rad nad prilozenim skupom podataka, 1 poen

Aplikacija treba efikasno da radi nad prilozenim skupom podataka.

Zahtevi:

- ne ucitavati ponovo podatke pri svakoj operaciji;
- ne formirati ponovo sve strukture pri svakoj operaciji;
- po pokretanju programa formirati potrebne strukture za pretragu, rangiranje, preporuke i obilazak;
- vreme od pokretanja do prve operacije ne treba da traje predugo;
- za `medium` skup ocekuje se interaktivan rad;
- za `full` skup potrebno je dokumentovati vreme ucitavanja i vreme izvrsavanja najskupljih operacija.

Najskuplje operacije koje treba meriti/dokumentovati mogu biti:

- ucitavanje fajlova;
- izgradnja grafa;
- izgradnja inverted index-a;
- izgradnja trie strukture;
- inicijalni PageRank;
- PPR za preporuke;
- BFS na vecem nivou;
- top-k pretraga/preporuke ako je znacajno.

## 7. Rangiranje rezultata

Rangiranje je vazan zahtev za vise delova projekta.

Pretraga:

- rangirati po relevantnosti upita;
- kod slicne relevantnosti koristiti PageRank;
- za top rezultate koristiti heap.

Autocomplete:

- naci korisnike sa zadatim prefiksom;
- sortirati po PageRank vrednosti.

Preporuke:

- koristiti kombinovani skor `alpha * PPR + (1 - alpha) * content_similarity`;
- filtrirati vec pracene, samog korisnika i blokirane odnose;
- prikazati top rezultate.

Top rezultati ne moraju biti prikazani u potpunosti. Dovoljno je prikazati, na primer:

- prvih 5;
- prvih 10;
- broj koji korisnik unese.

Za izbor i prikaz top rezultata moze se koristiti heap.

## 8. Algoritmi i strukture koje student treba da razume

Na odbrani student treba da ume da objasni:

- kako je predstavljen graf;
- kako rade izlazne i ulazne veze;
- kako se racuna izlazni stepen;
- kako radi PageRank;
- zasto PageRank nije isto sto i broj pratilaca;
- kako radi PPR;
- kako je napravljen inverted index;
- kako se obradjuje tekst biografije;
- kako se koristi trie;
- kako radi BFS;
- kako se racuna slicnost biografija;
- kako se obradjuju blokirani korisnici;
- kako se dobijaju i rangiraju top rezultati;
- kako se meri efikasnost nad `medium` i `full` skupom.

Tamo gde se eksplicitno trazi implementacija strukture ili algoritma, kao sto su:

- trie;
- PageRank;
- PPR;
- BFS;

student treba da pokaze sopstvenu implementaciju i razumevanje. Standardne Python strukture podataka su dozvoljene, ali ne zamenjuju trazene algoritme.

## 9. Minimalni funkcionalni meni

Minimalni meni za osnovni deo:

```text
1. Pretraga korisnika
2. Prikaz najuticajnijih korisnika
3. Dodavanje nove follow veze
4. Prikaz istorije interakcija
0. Izlaz
```

Prosireni meni za pun projekat:

```text
1. Pretraga korisnika
2. Prikaz najuticajnijih korisnika
3. Dodavanje nove follow veze
4. Prikaz istorije interakcija
5. Autocomplete korisnickih imena
6. Hibridne preporuke korisnika
7. BFS obilazak mreze
8. Did you mean za korisnicko ime
9. Prikaz/provera blokiranja
10. Prikaz statistike performansi
0. Izlaz
```

Tacni nazivi opcija nisu propisani, ali funkcionalnosti moraju biti dostupne.

## 10. Predaja zadatka

Opste informacije:

- zadatak nosi 25 poena;
- obavezno je koristiti prilozeni skup podataka;
- aplikacija mora raditi nad `small`, `medium` i `full` skupom;
- za razvoj se preporucuje `small`;
- za demonstraciju se preporucuje `medium`;
- `full` se koristi za proveru performansi.

Sve fajlove zadatka treba smestiti u folder pod nazivom:

```text
projekat2_sv_XX_YYYY
```

Umesto `XX_YYYY` navodi se broj indeksa, broj upisa i godina upisa.

Primer:

```text
projekat2_sv_02_2025
```

Folder treba ubaciti u zip arhivu i nazvati je isto kao zadatak:

```text
projekat2_sv_XX_YYYY.zip
```

Zip arhivu treba upload-ovati kao assignment na Canvas.

Ako postoji problem sa upload-om, u predvidjenom roku zip se moze poslati na email adresu predmetnog asistenta.

## 11. Kontrolna lista zahteva

Osnovni deo:

- [ ] Ucitavanje `users.txt`
- [ ] Ucitavanje `connections.txt`
- [ ] Klasa `User`
- [ ] Klasa `SocialGraph`
- [ ] Usmeren graf pracenja
- [ ] Izlazne veze
- [ ] Ulazne veze
- [ ] Izlazni stepen
- [ ] Hash mape za brzo pronalazenje korisnika
- [ ] Iterativni PageRank
- [ ] Damping factor `0.85`
- [ ] Konvergencija, na primer `epsilon = 1e-6`
- [ ] Obrada `dead end` cvorova
- [ ] Teleportacija protiv spider trap/dead end problema
- [ ] Prikaz najuticajnijih korisnika
- [ ] Heap za top rezultate
- [ ] Ponovno racunanje PageRank-a nakon nove follow veze
- [ ] Pretraga po korisnickom imenu
- [ ] Pretraga po recima iz biografije
- [ ] Case insensitive pretraga
- [ ] Text processing biografije
- [ ] Inverted index
- [ ] Rangiranje pretrage po relevantnosti i PageRank-u
- [ ] Dodavanje nove follow veze
- [ ] Evidencija istorije zapracivanja
- [ ] Prikaz koga je korisnik zapratio
- [ ] Prikaz ko je korisnika zapratio
- [ ] Hronoloski redosled istorije
- [ ] Tekstualni meni
- [ ] Izlaz iz programa

Dodatni deo:

- [ ] Trie za korisnicka imena
- [ ] Autocomplete po prefiksu
- [ ] Case insensitive autocomplete
- [ ] Autocomplete sortiran po PageRank-u
- [ ] Hibridne preporuke
- [ ] Personalized PageRank
- [ ] Slicnost biografija
- [ ] Izbor `alpha` parametra
- [ ] Formula `alpha * PPR + (1 - alpha) * content_similarity`
- [ ] Filtriranje vec pracenih korisnika u preporukama
- [ ] Filtriranje samog korisnika u preporukama
- [ ] BFS obilazak
- [ ] Prikaz konekcija po nivoima
- [ ] Korisnik zadaje maksimalni BFS nivo
- [ ] `visited` logika da se korisnik ne obradjuje vise puta
- [ ] "Did you mean" za nepostojece korisnicko ime
- [ ] Nekoliko slicnih ispravnih predloga
- [ ] Ucitavanje `blocked.txt`
- [ ] Blokirane korisnike ne brisati iz grafa
- [ ] Ne preporucivati korisnike blokirane u bilo kom relevantnom smeru
- [ ] Zabraniti follow vezu ako postoji blokiranje u bilo kom smeru
- [ ] Jasno organizovan OOP kod
- [ ] Bez nepotrebnog ponavljanja
- [ ] `README.md`
- [ ] Opis pokretanja u README-u
- [ ] Opis ulaznih fajlova u README-u
- [ ] Spisak implementiranih funkcionalnosti u README-u
- [ ] Efikasan rad bez ponovnog ucitavanja pri svakoj operaciji
- [ ] Interaktivan rad za `medium`
- [ ] Dokumentovana vremena za `full`
- [ ] Po potrebi serijalizacija/kesiranje struktura pomocu `pickle`

