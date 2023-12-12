# Projektin kuvaus

Peli on "Indiana Jones" tyylinen seikkailuplatformeri, vähän kuin rick dangerous klassikkopeli.

Pelaajan tavoite on käydä erinäisiä kenttiä läpi, joissa päätavoitteena on löytää eräänlaisen aarteen luokse, jonka jälkeen kenttä loppuu.

Kentän loputtua, pelaaja siirtyy kauppavaiheeseen jossa voidaan ostaa lisätarvikkeita ennen seuraavaa kenttää. Tätä varten tarvitaan rahaa, ja rahaa saa aarteita keräämällä.

Pelin voittaa suorittamalla kaikki kampanjaan (Lista kenttiä) kuuluvat kentät.

# Laajennettavuus

Projekti toteutetaan siten, että sitä olisi mahdollisimman helppo laajentaa.

Tiedostot vihollisiin, pickuppeihin, sekä kenttiin ovat muokattavissa ilman ohjelmointitaitoja, ja näille löytyy ohjeet kuinka toteuttaa, sekä käyttäjän kannalta voi myös tarkastella itse tiedostoja ottaakseen mallia.

Viholliset ja pickupit onnistuvat puhtaasti teksti ja kuvatiedostoilla, kenttien luonti kuitenkin tarvitsee "Tiled" Editorin, sillä tiedostot ovat .tmx formaattia.

# Vaaditusmäärittely

Kaikki allaolevat toiminnallisuudet ovat jo toteutettu.

- Invoketoiminnot (Poetry run invoke [Komento])
    - Start (Sekä lisäargumentti jolla vaihtaa kampanja)
    - Lint
    - Coverage-Report
    - Test

- Tiedostojärjestelmä
    - Lukee tiledillä luodut tiedot peliin
    - Lukee käyttäjien luomat viholliset
    - Lukee käyttäjien luomat pickupit
    - Lukee käyttäjien luomat kentät (Sekä kampanjat)
    - Kirjaa ja lukee käyttäjän pelikerrat kampanjoittain säilyttäen saavutetut pisteet.

- Pelilogiikka
    - Kameran liikkuvuus
    - Hahmojen liikkuminen (Kävely, kiipeily, hyppiminen, painovoima)
    - Pelaajien toiminnot (Ampuminen, ym)
    - Vihollisten tekoäly (Vihollisella perus tekoäly, osaa kävellä, vältellä putouksia ja kääntää suuntaa)
    - Tapahtumat (Esim. jos pelaaja menee alueelle, avataan vaikka ovi)
    - Kenttien välinen tila, missä ladataan uudet kentät
    - Hyppiminen
    - Collisionit
    - Tikkaat
    - Valot
    - Projektiilit
    - Damage & Heal systeemi
    - Tavaroiden ostojärjestelmä

- Lisää dokumentaatiota.
    - Arkkitehtuurikuvaus (Sekä yksi sekvenssikaavio tälle)
    - Testausdokumentaatio
    - Työaikakirjaus
    - Peliohjeet
    - Ohjeistus sisällön luomiselle (Kampanjat, kentät, viholliset ja pickupit)

- Testit
    - Pylint (Ongelmia toki löytyy vielä)
    - Coverage (70%)

# Parannusideoita

- Viholliset, joilta löytyvät kyky ampua itse projektiileja
- Äänet sekä näille systeemi, miten luoda lisää nopeasti jatkossa assets/sounds/ sisälle
- Animaatiot
- Paremmat collisionit
- Main menu
- Projektiileille omat templatet (samanlain kuin vihollisille ja pickupeille luotu, jotta saisi paremmin luotua lisää)
- Yleisesti enemmän toiminnallisuutta ja sisältöä (Esim. pommit.) Osa näistä voitaisiin toteuttaa nykyisillä systeemeillä, esim ansa-alue joka iskee pelaajaan.
