Kuvaus projektista:

Peli on "Indiana Jones" tyylinen seikkailuplatformeri, vähän kuin rick dangerous klassikkopeli.

Pelaajan tavoite on käydä erinäisiä kenttiä läpi, joissa päätavoitteena on löytää eräänlaisen aarteen luokse, jonka jälkeen kenttä loppuu.

Kentän loputtua, pelaaja siirtyy kauppavaiheeseen jossa voidaan ostaa lisätarvikkeita ennen seuraavaa kenttää. Tätä varten tarvitaan rahaa, ja rahaa saa kenttiä suorittamalla, sekä sivuaarteita keräämällä.

Kenttiä tulee X lukumäärä, päätavoitetta en vielä tiedä.

Tavaroihin liittyen, pelaaja aloittaa pelin käsiaseella, sekä vähillä määrillä luoteja. Pelaaja kykenee parantamaan asemaansa esimerkiksi ostamalla/löytämällä:

- Lisää elämiä
- Lisää luoteja
- Gadgetteja (Kuten pommit, soihdut, ym)
- Parempia aseita, joissa ovat omat statsinsa.
- Suojia
- Mahdollisesti jotain muutakin.

Kenttien haasteet tulevat muodoissa:

- Viholliset
- Ansat
- Mahdollisia palapelejä
- Mahdollisia muita uhkia

Kenttien luonti tapahtuu "Tiled" Editoria käyttäen, joissa luodaan tiedot kentälle, jotka sitten ladataan itse peliin.

Tavoitteena on myös luoda peliin seuraavia hyödyllisiä ominaisuuksia:

- Tilastot
- Kampanjasysteemi (Kampanjasysteemin tarkoitus on sallia pelaajien luoda omat kampanjat omilla kentillään, sekä ohjeet näiden luomiselle)
- Tallennus/Lataus


TODO lista:

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
    - Luokkakaavio
    - DONE: Sekvenssikaavio
    - DONE: Työaikakirjaus
    - DONE: Peliohjeet
    - DONE: Ohjeistus kenttien ja kampanjoiden luomiselle ym. Mahdollisia video tai kuva-ohjeita tulossa mikäli tarvitaan
- Testit
    - DONE: Pelaajatestit
    - DONE: Pickuptestit
    - DONE: Pylint
    - PROGRESS: Coverage (Ei vielä vaadittu 70%)
    - Vihollistestit
    - Pelitestit
    - Jotain muita testejä


Parannusideoita:

- Viholliset, jotka kykenevät itse ampumaan projektiileja
- Kauppa, mistä ostaa tavaroita.
- Äänet sekä näille systeemi, miten luoda lisää nopeasti jatkossa assets/sounds/in sisälle
- Animaatiot
- Paremmat collisionit
- Muitakin toiminnallisuuksia, kuten pommit ym
- Enemmän zoneja/actioneja (esim. spawn action)
- Main menu
- Tilastonäkymä
- Sotkuiset importit (Mutta näitä nyt ei oikeasti kukaan enään tästä frankensteinista ole korjaamassa)



