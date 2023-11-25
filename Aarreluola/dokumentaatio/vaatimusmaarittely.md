Kuvaus projektista:

Peli on "Indiana Jones" tyylinen seikkailuplatformeri, vähän kuin rick dangerous klassikkopeli.

Pelaajan tavoite on käydä erinäisiä kenttiä läpi, joissa päätavoitteena on löytää eräänlaisen aarteen luokse, jonka jälkeen kenttä loppuu.

Kentän loputtua, pelaaja siirtyy kauppavaiheeseen jossa voidaan ostaa lisätarvikkeita ennen seuraavaa kenttää. Tätä varten tarvitaan rahaa, ja rahaa saa kenttiä suorittamalla, sekä sivuaarteita keräämällä.

Kenttiä tulee X lukumäärä, päätavoitetta en vielä tiedä.

Tavaroihin liittyen, pelaaja aloittaa pelin käsiaseella, sekä vähillä määrillä luoteja. Pelaaja kykenee parantamaan asemaansa esimerkiksi ostamalla/löytämällä:

- Lisää elämiä
- Lisää luoteja
- Parempia aseita, joissa ovat omat statsinsa.
- Suojia
- Mahdollisesti jotain muutakin.

Kenttien haasteet tulevat muodoissa:

- Viholliset
- Ansat

Kenttien luonti tapahtuu "Tiled" Editoria käyttäen, joissa luodaan tiedot kentälle, jotka sitten ladataan itse peliin. Kentillä muodostetaan suurempia kampanjoita, joita voi myös käyttäjä luoda.


TODO lista:

- Invoketoiminnot
    - DONE: Start (Sekä lisäargumentti jolla vaihtaa kampanja)
    - DONE: Lint
    - DONE: Coverage
    - DONE: Test
- Tiedostojärjestelmä
    - DONE: Kykenee ottamaan tiledillä luodut tiedot ja muuntamaan sen datan pelille soveltuvaksi
    - DONE: Kykenee lukemaan käyttäjien luomat viholliset
    - DONE: Kykenee lukemaan käyttäjien luomat pickupit
    - DONE: Kykenee pyörittämään käyttäjien luomat kampanjat (jotka sisältävät kentät ja näihin luodut viholliset/pickupit)
- Pelilogiikka
    - DONE: Kameran liikkuvuus
    - DONE: Hahmojen liikkuminen (Kävely, kiipeily, hyppiminen, painovoima)
    - DONE: Pelaajien toiminnot (Ampuminen, ym)
    - DONE: Vihollisten tekoäly (Vihollisella perus tekoäly, osaa kävellä, vältellä putouksia ja kääntää suuntaa)
    - DONE: Tapahtumat (Esim. jos pelaaja menee alueelle, avataan vaikka ovi)
    - DONE: Kenttien välinen tila, missä ladataan uudet kentät
    - DONE: Hyppiminen
    - DONE: Collisionit
    - DONE: Tikkaat
    - DONE: Valot
    - DONE: Projektiilit
    - DONE: Damage & Heal systeemi
    - DONE: Tavaroiden ostojärjestelmä
- Lisää dokumentaatiota.
    - DONE: Sekvenssikaavio
    - DONE: Työaikakirjaus
    - DONE: Peliohjeet
    - DONE: Ohjeistus kenttien ja kampanjoiden luomiselle ym. Mahdollisia video tai kuva-ohjeita tulossa mikäli tarvitaan
- Testit
    - DONE: Pylint (Ongelmia toki löytyy vielä)
    - DONE: Coverage (70%)



Parannusideoita:

- Viholliset, jotka kykenevät itse ampumaan projektiileja
- Äänet sekä näille systeemi, miten luoda lisää nopeasti jatkossa assets/sounds/in sisälle
- Animaatiot
- Paremmat collisionit
- Muitakin toiminnallisuuksia, kuten pommit ym
- Enemmän zoneja/actioneja (esim. spawn action)
- Main menu
- Tilastonäkymä, sekä itse tilastot
- Sotkuiset importit (Mutta näitä nyt ei oikeasti kukaan enään tästä frankensteinista ole korjaamassa)
- Projektiileille omat templatet (samanlain kuin vihollisille ja pickupeille luotu, jotta saisi paremmin luotua lisää)
- Varmaan noin 50% koodista on silkkaa pahuutta, jonka voisi lakaista maton alle. Luudalle tarvetta.