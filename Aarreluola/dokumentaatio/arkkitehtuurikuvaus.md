# Rakenne

Ohjelma aloittaa pelin lataamalla game.py:ssä tarpeelliset asiat ja tallentaa suurelta osin nämä game_stateen, joka lähetetään aina eteenpäin esim. rendererille, mistä voidaan sekä lukea että kirjoittaa dataa suoraan itse game stateen. Game state sisältää suurimman osan tärkeästä datasta (esim. viholliset, pelaajat, ym.)

Tämän jälkeen jatkamme itse main looppiin, jossa päivitämme pelin tilaa. Game state toimii edelleen pääsääntöisenä varastona tässäkin vaiheessa.

Ohjelma päivittyy 60 kertaa sekunnissa.

# Diagrammi pelin tärkeämmistä ominaisuuksista alusta loppuun

![Sekvenssi](https://github.com/Janitus/Ohjelmistotekniikka/blob/main/Aarreluola/dokumentaatio/sequencediagram.png)


# Käyttöliittymä

Käyttöliittymä on eritelty muusta logiikasta, ja sen tarkoitus on näyttää pelaajalle tätä eniten kiinnostavat arvot. Nämä arvot ovat elämät, ammukset, raha sekä health. UI renderöidään viimeisenä rendererissä.


# Tiedostojen luku

Tiedostoja luetaan aina pelin käynnistyksen ohella, sekä osia tiedostoista luetaan väliajoin myöhemmin (Esim. seuraavaan kenttään päästyä, ladataan uusi kenttä tiedostoista)

Oleellisimmat tiedostot joita luemme, ovat viholliset, pickupit, kentät ja kampanjat. Nämä tulevat muodoissa kuvatiedostot, tekstitiedostot, sekä .tmx tiedostot (Kenttätiedostot.)

Viholliset ja pickupit luemme ohjelman alkuvaiheessa, jotta voimme pitää kopion jokaisesta olemassaolevasta vihollisesta ilman että näitä tietoja tarvitsee lukea pelin aikana. Täten saamme esimerkiksi kenttien lataamisnopeutta paranneltua, sillä kovalevyltä lukeminenhan on hitainta mitä on, joten jätämme sinne vain .tmx tiedostot. Voimme siten .tmx tiedoston perusteella vain katsoa, että mihin mikäkin vihollinen/pickup kuuluu, ja suoraan instantioida ne valmiiksi ladatusta datastamme. Toisaalta, tällä ei hirveästi painoarvoa ole.


# Ohjelman rakenneongelmat

Jos rehellisesti vastataan, niin koko kapistus pitäisi uudelleennimetä frankensteiniksi. Muummoassa circular importteja, global variableja ym. pylintin herjaamia löytyy koodista jonkin verran.

Ohjelman kulkua/koodia myös erityisesti ei ole kovin helppoa seurata, miten missäkin järjestyksessä asiat toimii. Tähän mm. vaikuttaa suhteellisen suuret ja monimutkaiset funktiot.
    Esimerkkinä vihollisia päivittäessä, tarkastamme myös samalla että ovatko vihollinen ja pelaaja kosketuksissa jonka jälkeen vihollinen lyö pelaajaa, ja tästä puolestaan pääsemme characterin puolelle lukemaan damagesta. Tämä taas puolestaan voi merkata pelaajan "kuolleeksi", jolloin seuraavalla päivityksellä loopissa vasta päivitetään pelin tila, ja ladataan kenttä uusiksi / hävitään peli.

Vaikeuksia myös varmasti tuottaa esim. .tmx tiedostojen luku (sekä se, miten sinne tietoa tallennetaan), sillä esimerkiksi tiledin väriarvoja kun luetaan, ovat ne eri formaatissa kuin mitä yleensä ohjelmat käyttävät (ARGB vs RGBA), jonka vuoksi joudutaan sitten tämä konvertoimaan ennen käyttöä. Toki aina jonkinverran tälläisiä on muutenkin (esim. blenderin ja unityn välillä Y ja Z akselit flippaavat), mutta harvemmin näissä manuaalisesti tarvitsee omassa koodissa ratkoa.


# Pieni henkilökohtainen kommentti

Yleisesti olisi myös koodin luettavuutta helpottanut, mikäli olisi tullut enemmän hyödynnettyä erinäisiä design patterneja (esim. jos game_staten passaamisen sijasta olisi luonut singleton patternilla tietovaraston), mutta vajavaisten pythonitaitojen takia tämä olisi näyttäytynyt lisääntyneiden generoitujen koodien määränä. Myös jonkinsortin eventtipohjainen (esim C# tai Javan eventit) olisi voinut helpottaa paljon.