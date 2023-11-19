# Ohjelmistotekniikka Harjoitustyö

RELEASE: https://github.com/Janitus/Ohjelmistotekniikka/releases/tag/viikko3

# Kuvaus

Projekti on pienimuotoinen aarretasohyppely. Pelaajan tehtävänä on päästä kentän loppuun väistellen vaaroja, sekä tarvittaessa edesauttaa asemaansa keräämällä aarteita.

Projekti on suunniteltu pohjaksi kokonaiselle pelille, jota voidaan laajentaa, sekä sisällytän myös ohjeita, kuinka osan tästä työstä voi tehdä.

[![Kuva](https://i.gyazo.com/f50101467b7d175cfa16ed52641fdcf5.png)

# Asennusohje

1. git clone https://github.com/Janitus/Ohjelmistotekniikka

2. cd todoapp

3. poetry install - note: jos poetry install ei toimi, poista poetry.lock ja käytä komentoa uudestaan. Riippuvuudet pygame ja pytmx pitäisi asentua nyt! poetry.lock tiedosto löytyy root/todoapp kansiosta, joissain systeemeissä tämä tiedosto on näkymätön joudut mahdollisesti etsimään tiedoston että se näkyy!

# Käyttöohje

1. cd todoapp

2. poetry run invoke start HUOM! Jos haluat kokeilla omaa kampanjaasi, käytä: poetry run invoke start --campaign=kampanjanimi

3. Pelin pitäisi käynnistyä!


# Dokumentaatio

Työaikakirjaus: https://github.com/Janitus/Ohjelmistotekniikka/blob/main/todoapp/dokumentaatio/tyoaikakirjanpito.md

Vaatimusmäärittelyt: https://github.com/Janitus/Ohjelmistotekniikka/blob/main/todoapp/dokumentaatio/vaatimusmaarittely.md

Changelog: https://github.com/Janitus/Ohjelmistotekniikka/blob/main/todoapp/dokumentaatio/change_log.md

Peliohjeet: https://github.com/Janitus/Ohjelmistotekniikka/blob/main/todoapp/dokumentaatio/play_instructions.md

Sekvenssidiagrammi: https://github.com/Janitus/Ohjelmistotekniikka/blob/main/todoapp/dokumentaatio/sequencediagram.png

# Luontiohjeet

Kentät: https://github.com/Janitus/Ohjelmistotekniikka/blob/main/todoapp/dokumentaatio/level_creation_information.md

Viholliset: https://github.com/Janitus/Ohjelmistotekniikka/blob/main/todoapp/dokumentaatio/enemy_creation_information.md

Pickupit: https://github.com/Janitus/Ohjelmistotekniikka/blob/main/todoapp/dokumentaatio/pickup_creation_information.md

Kampanjat: https://github.com/Janitus/Ohjelmistotekniikka/blob/main/todoapp/dokumentaatio/campaign_creation_information.md



# Testaus

Kokeiltu yliopiston cubbli linuxilla käyttäen VMWarea. Peli toimii odotetusti. Myös testikomennot toimivat odotetusti.

Testikomennot voi suorittaa /todoapp sisällä:

- poetry run invoke test

- poetry run invoke coverage-report

- poetry run invoke lint, Huom koodissa on käytetty disable=no-member,c-extension-no-member, sillä nämä herjaavat jokaisesta pygamen ominaisuuksista no-member erroreita, vaikka koodi toimii muuten.

# Testitulokset

--- Lint ---

Your code has been rated at 9.71/10 (previous run: 9.71/10, +0.00)

--- Coverage ---

Name                        Stmts   Miss Branch BrPart  Cover

TOTAL                         912    261    328     21    70%
