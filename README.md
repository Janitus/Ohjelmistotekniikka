# Ohjelmistotekniikka Harjoitustyö

RELEASE: https://github.com/Janitus/Ohjelmistotekniikka/releases/tag/viikko7

# Kuvaus

Projekti on pienimuotoinen aarretasohyppely. Pelaajan tehtävänä on päästä kentän loppuun väistellen vaaroja, sekä tarvittaessa edesauttaa asemaansa keräämällä aarteita.

Projekti on suunniteltu pohjaksi kokonaiselle pelille, jota voidaan laajentaa, sekä sisällytän myös ohjeita, kuinka osan tästä työstä voi tehdä.

[![Kuva](https://i.gyazo.com/f50101467b7d175cfa16ed52641fdcf5.png)

# Asennusohje

1. git clone https://github.com/Janitus/Ohjelmistotekniikka

2. cd Aarreluola

3. poetry install - note: jos poetry install ei toimi, poista poetry.lock ja käytä komentoa uudestaan. Riippuvuudet pygame ja pytmx pitäisi asentua nyt! poetry.lock tiedosto löytyy root/Aarreluola kansiosta, joissain systeemeissä tämä tiedosto on näkymätön joudut mahdollisesti etsimään tiedoston että se näkyy!

# Käyttöohje

1. cd Aarreluola

2. poetry run invoke start HUOM! Jos haluat kokeilla omaa kampanjaasi, käytä: poetry run invoke start --campaign=kampanjanimi

3. Pelin pitäisi käynnistyä!


# Dokumentaatio

Työaikakirjaus: https://github.com/Janitus/Ohjelmistotekniikka/blob/main/Aarreluola/dokumentaatio/tyoaikakirjanpito.md

Vaatimusmäärittelyt: https://github.com/Janitus/Ohjelmistotekniikka/blob/main/Aarreluola/dokumentaatio/vaatimusmaarittely.md

Changelog: https://github.com/Janitus/Ohjelmistotekniikka/blob/main/Aarreluola/dokumentaatio/change_log.md

Peliohjeet: https://github.com/Janitus/Ohjelmistotekniikka/blob/main/Aarreluola/dokumentaatio/play_instructions.md

Testausdokumentaatio: https://github.com/Janitus/Ohjelmistotekniikka/blob/main/Aarreluola/dokumentaatio/testaus_dokumentaatio.md

Arkkitehtuurikuvaus: https://github.com/Janitus/Ohjelmistotekniikka/blob/main/Aarreluola/dokumentaatio/arkkitehtuurikuvaus.md

# Luontiohjeet

Kentät: https://github.com/Janitus/Ohjelmistotekniikka/blob/main/Aarreluola/dokumentaatio/level_creation_information.md

Viholliset: https://github.com/Janitus/Ohjelmistotekniikka/blob/main/Aarreluola/dokumentaatio/enemy_creation_information.md

Pickupit: https://github.com/Janitus/Ohjelmistotekniikka/blob/main/Aarreluola/dokumentaatio/pickup_creation_information.md

Kampanjat: https://github.com/Janitus/Ohjelmistotekniikka/blob/main/Aarreluola/dokumentaatio/campaign_creation_information.md



# Testaus

Kokeiltu yliopiston cubbli linuxilla käyttäen VMWarea. Peli toimii odotetusti. Myös testikomennot toimivat odotetusti.

Testikomennot voi suorittaa /Aarreluola sisällä:

- poetry run invoke test

- poetry run invoke coverage-report

- poetry run invoke lint, Huom koodissa on käytetty disable=no-member,c-extension-no-member, sillä nämä herjaavat jokaisesta pygamen ominaisuuksista no-member erroreita, vaikka koodi toimii muuten. Myös player ja characterissa on too-many-instance-attributes, sillä näihin molempiin kuuluu suuri määrä attribuutteja mitä ei voisi vähentää.

# Testitulokset

--- Lint ---

Your code has been rated at 9.91/10 (previous run: 9.90/10, +0.01

--- Coverage ---

Name                        Stmts   Miss Branch BrPart  Cover

TOTAL                         881    264    306     24    68%
