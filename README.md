# Ohjelmistotekniikka Harjoitustyö

# Kuvaus

Projekti on pienimuotoinen aarretasohyppely. Pelaajan tehtävänä on päästä kentän loppuun väistellen vaaroja, sekä tarvittaessa edesauttaa asemaansa keräämällä aarteita.

Projekti on suunniteltu pohjaksi kokonaiselle pelille, jota voidaan laajentaa, sekä sisällytän myös ohjeita, kuinka osan tästä työstä voi tehdä.

# Asennusohje

1. git clone https://github.com/Janitus/Ohjelmistotekniikka

2. cd todoapp

3. poetry install - note: jos poetry install ei toimi, poista poetry.lock ja käytä komentoa uudestaan. Riippuvuudet pygame ja pytmx pitäisi asentua nyt! poetry.lock tiedosto löytyy root/todoapp kansiosta, joissain systeemeissä tämä tiedosto on näkymätön joudut mahdollisesti etsimään tiedoston että se näkyy!

# Käyttöohje

1. poetry run python src/game.py

2. Pelin pitäisi käynnistyä!


# Dokumentaatio

Työaikakirjaus: https://github.com/Janitus/Ohjelmistotekniikka/blob/main/todoapp/dokumentaatio/tyoaikakirjanpito.md

Vaatimusmäärittelyt: https://github.com/Janitus/Ohjelmistotekniikka/blob/main/todoapp/dokumentaatio/vaatimusmaarittely.md

Ohjeet kenttäeditoinnille: https://github.com/Janitus/Ohjelmistotekniikka/blob/main/todoapp/dokumentaatio/level_creation_information.md

Ohjeet pelaajalle: https://github.com/Janitus/Ohjelmistotekniikka/blob/main/todoapp/dokumentaatio/play_instructions.md

Ohjeet pickuppien luonnille: https://github.com/Janitus/Ohjelmistotekniikka/blob/main/todoapp/dokumentaatio/pickup_creation_information.md


# Testaus

Kokeiltu yliopiston cubbli linuxilla käyttäen VMWarea. Peli toimii odotetusti. Myös testikomennot toimivat odotetusti.

Testikomennot voi suorittaa /todoapp sisällä:

1. poetry run coverage run --branch -m pytest src

2. poetry run coverage report