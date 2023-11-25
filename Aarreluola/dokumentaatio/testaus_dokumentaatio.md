# Yksikkötestit

Testeissä keskityimme pääsääntöisesti pelikentältä löytyviin objekteihin (hahmot, pickupit), sekä itse kentän ja tämän sisällön lataamiseen.

Testauskattavuus on noin 70% (Tarkemmat tulokset alla.) Ne missä testikattavuus on pienempi olisivat olleet hyvä myös testata poislukien kuitenkin lighting, sekä jollakin asteikolla renderer.

src\tests\character_test.py .................                            [ 20%]
src\tests\enemy_test.py .......                                          [ 28%]
src\tests\game_test.py .........                                         [ 39%]
src\tests\pickup_test.py ...............                                 [ 57%]
src\tests\player_test.py ...................................             [100%]

============================= 83 passed in 1.23s ==============================
Wrote HTML report to htmlcov\index.html
Name                        Stmts   Miss Branch BrPart  Cover
-------------------------------------------------------------
src\action.py                  25     12      6      0    42%
src\character.py              106      9     34      0    92%
src\enemy.py                   74      2     40      4    95%
src\game.py                   163     74     56      6    48%
src\gamestate.py               15      0      2      0   100%
src\lighting.py                58     15     18      2    72%
src\map.py                    119      9     68      5    90%
src\pickup.py                  83      6     44      3    91%
src\player.py                  75      7     20      1    92%
src\projectile.py              35     26      2      0    24%
src\projectile_manager.py      30     20     16      0    22%
src\renderer.py                47     33     14      0    23%
src\ui\ui.py                   50     35      0      0    30%
src\zone.py                    32     13      8      0    52%
-------------------------------------------------------------
TOTAL                         912    261    328     21    70%



# Manuaaliset käyttäjätestit

Sovellusta on testattu itse pelaamalla sovellusta ja tarkastelemalla tämän tapahtumia (esim. Pystyykö pelaaja hyppimään kun on ilmassa, törmääkö seinään odotetusti)

Myös ohjeita on kokeiltu seurata askel askeleelta (mukaanlukien itse luontiohjeet)


# Laatuongelmia

Sovellus ei testaa tai ohjaa käyttäjää riittävästi esim. luontiohjeiden perusteella luomaan oikeanlaista syötettävää dataa. Tämän vuoksi onkin lähes odotettua, että käyttäjä voisi syöttää esimerkiksi viholliselle max_hp = -5, eikä peli huomioisi sitä lainkaan, sillä validaatiot ovat pienet ja näistä ei myöskään ilmoiteta läheskään aina.

Sovelluksessa on myös ongelmia mm. collisionin kanssa, että miten esimerkiksi luodit menevät monesti vihollisen spriten läpi. Puolustuksekseni sanon, että ovat oikeasti "intentional game mechanics". Pelattavat ne kuitenkin on.