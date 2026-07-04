# Projekat 2 - Simulacija drustvene mreze

Projekat implementira konzolnu aplikaciju za rad nad usmerenim grafom drustvene mreze. Korisnici su cvorovi grafa, a follow veze su usmerene grane oblika `from_id -> to_id`, gde `from_id` prati `to_id`.

## Pokretanje

Program se pokrece iz korenskog foldera projekta:

```bash
python3 main.py
```

Ako se ne prosledi argument, program pri pokretanju nudi izbor:

```text
1. small
2. medium
3. full
4. custom path
```

Dataset se moze proslediti i direktno kao argument:

```bash
python3 main.py dataset/small
python3 main.py dataset/medium
python3 main.py dataset/full
```

## Ulazni fajlovi

Svaki dataset folder treba da sadrzi tri fajla:

```text
users.txt
connections.txt
blocked.txt
```

Format `users.txt`:

```text
id|username|bio
```

Format `connections.txt`:

```text
from_id|to_id
```

Format `blocked.txt`:

```text
blocker_id|blocked_id
```

## Implementirane funkcionalnosti

### Graf drustvene mreze

Implementirane su klase `User` i `SocialGraph`.

`SocialGraph` cuva:

- korisnike po ID-u;
- korisnike po username-u;
- izlazne follow veze;
- ulazne follow veze;
- izlazni stepen svakog korisnika;
- blokiranja;
- istoriju novih follow interakcija.

### PageRank

Implementiran je iterativni PageRank algoritam u `PageRankService`.

Karakteristike:

- damping factor je `0.85`;
- konvergencija koristi `epsilon = 1e-6`;
- korisnici bez izlaznih veza se obradjuju kao dangling cvorovi;
- top korisnici se izdvajaju pomocu heap-a.

### Pretraga

Implementirana je pretraga u `SearchService`.

Podrzano je:

- pretraga po username-u;
- pretraga po recima iz biografije;
- case insensitive pretraga;
- obrada teksta regex-om;
- inverted index za bio reci;
- rangiranje po relevantnosti i PageRank-u;
- top rezultati preko heap-a.

### Dodavanje follow veze i istorija

Kroz meni je moguce dodati novu follow vezu.

Pri dodavanju:

- proverava se da korisnici postoje;
- korisnik ne moze pratiti samog sebe;
- ne dodaje se duplikat veze;
- proverava se blokiranje u oba smera;
- azuriraju se izlazne veze, ulazne veze i izlazni stepen;
- evidentira se interakcija;
- PageRank se ponovo racuna.

Istorija prikazuje samo nove follow veze dodate tokom rada programa.

### Blokiranja

Podaci iz `blocked.txt` se ucitavaju u graf.

Blokiranja se koriste:

- pri dodavanju follow veze;
- pri preporukama korisnika.

Ako postoji blokiranje u bilo kom smeru, nova follow veza se ne dozvoljava.

### Trie autocomplete

Autocomplete je implementiran u `AutocompleteService` pomocu Trie strukture.

Podrzano je:

- case insensitive prefiksno pretrazivanje username-a;
- DFS/preorder prikupljanje kandidata iz podstabla prefiksa;
- rangiranje rezultata po PageRank-u;
- top rezultati preko heap-a.

### BFS obilazak mreze

BFS je implementiran u `GraphTraversalService`.

Za zadatog korisnika prikazuju se konekcije po nivoima:

- nivo 1 - direktne follow veze;
- nivo 2 - korisnici dostupni preko jednog posrednika;
- nivo 3 - korisnici dostupni preko dva posrednika.

Koristi se `visited` skup da se korisnik ne obradjuje vise puta.

### Did you mean

`DidYouMeanService` predlaze slicna postojeca korisnicka imena ako je uneto pogresno ime.

Koristi se:

- case insensitive poredjenje;
- `difflib.SequenceMatcher`;
- rangiranje po slicnosti i PageRank-u.

### Hibridne preporuke

Preporuke su implementirane u `RecommendationService`.

Koristi se formula:

```text
alpha * PPR + (1 - alpha) * content_similarity
```

Gde je:

- `PPR` Personalized PageRank iz perspektive zadatog korisnika;
- `content_similarity` Jaccard slicnost biografija;
- `alpha` parametar od `0` do `1`.

Preporuke filtriraju:

- samog korisnika;
- korisnike koje vec prati;
- korisnike koje je blokirao;
- korisnike koji su blokirali njega.

## Meni

Program nudi sledece opcije:

```text
1. Search users
2. Show top PageRank users
3. Add follow relation
4. Show interaction history
5. Autocomplete usernames
6. BFS connections by level
7. Did you mean username
8. Recommend users
0. Exit
```

## Primeri za demonstraciju

Pokretanje na small datasetu:

```bash
python3 main.py dataset/small
```

Primer pretrage:

```text
Search query: guildwars
```

Primer autocomplete-a:

```text
Username prefix: g
```

Primer BFS-a:

```text
Start user id: 1
Max level: 2
```

Primer did you mean:

```text
Username: guimanj
```

Primer preporuka:

```text
User id: 1
Alpha [0-1]: 0.7
How many recommendations to show: 5
```

## Performanse

Velicine dataset-a:

```text
small:  1000 korisnika, 80693 veza, 20 blokiranja
medium: 10000 korisnika, 354503 veza, 200 blokiranja
full:   81306 korisnika, 1768135 veza, 1626 blokiranja
```

Za `medium` se ocekuje interaktivan rad.

Performanse se mogu izmeriti pomocu:

```bash
python3 performance_check.py dataset/small
python3 performance_check.py dataset/medium
python3 performance_check.py dataset/full
```

Izmerena vremena na ovom racunaru:

```text
small:
  load_graph: 0.0461s
  pagerank: 0.1234s
  build_search_index: 0.0066s
  build_trie: 0.0072s
  search_query: 0.0001s
  autocomplete_query: 0.0000s
  bfs_level_2: 0.0000s
  recommendations: 0.1386s

medium:
  load_graph: 0.2276s
  pagerank: 0.9639s
  build_search_index: 0.0559s
  build_trie: 0.0157s
  search_query: 0.0006s
  autocomplete_query: 0.0006s
  bfs_level_2: 0.0012s
  recommendations: 1.3351s

full:
  load_graph: 1.0917s
  pagerank: 12.8591s
  build_search_index: 0.4758s
  build_trie: 1.1951s
  search_query: 0.0086s
  autocomplete_query: 0.0052s
  bfs_level_2: 0.0030s
  recommendations: 17.0853s
```

Najskuplje operacije na `full` skupu su PageRank i PPR preporuke.

## Napomena za odbranu

Za odbranu treba znati objasniti:

- zasto graf cuva i `following` i `followers`;
- zasto PageRank koristi `followers` i `out_degree`;
- sta su damping factor, dangling cvor i teleportacija;
- zasto inverted index ubrzava pretragu;
- kako Trie podrzava autocomplete;
- zasto BFS prikazuje konekcije po nivoima;
- kako radi `Did you mean`;
- razliku izmedju PageRank-a i Personalized PageRank-a;
- kako se racuna Jaccard slicnost;
- kako `alpha` menja preporuke.
