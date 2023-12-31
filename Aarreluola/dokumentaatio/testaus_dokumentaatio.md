# Yksikkötestit

Testeissä keskityimme pääsääntöisesti pelikentältä löytyviin objekteihin (hahmot, pickupit), sekä itse kentän ja tämän sisällön lataamiseen.

Testauskattavuus on noin 68% (Tarkemmat tulokset alla.) Ne missä testikattavuus on pienempi olisivat olleet hyvä myös testata poislukien kuitenkin lighting.

![Coverage](https://i.gyazo.com/98ecf39d5f9a6ae64fb9324a2cffa33b.png)


# Manuaaliset käyttäjätestit

Sovellusta on testattu itse pelaamalla sovellusta ja tarkastelemalla tämän tapahtumia (esim. Pystyykö pelaaja hyppimään kun on ilmassa, törmääkö seinään odotetusti)

Myös ohjeita on kokeiltu seurata askel askeleelta (mukaanlukien itse luontiohjeet)


# Laatuongelmia

Sovellus ei testaa tai ohjaa käyttäjää riittävästi esim. luontiohjeiden perusteella luomaan oikeanlaista syötettävää dataa. Tämän vuoksi onkin lähes odotettua, että käyttäjä voisi syöttää esimerkiksi viholliselle max_hp = -5, eikä peli huomioisi sitä lainkaan, sillä validaatiot ovat pienet ja näistä ei myöskään ilmoiteta läheskään aina.

Sovelluksessa on myös ongelmia mm. collisionin kanssa, että miten esimerkiksi luodit menevät monesti vihollisen spriten läpi. Puolustuksekseni sanon, että ovat oikeasti "intentional game mechanics". Pelattavat ne kuitenkin on.
