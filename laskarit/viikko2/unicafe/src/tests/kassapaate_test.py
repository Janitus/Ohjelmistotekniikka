import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.maksukortti = Maksukortti(1000)

    def test_saldo_oikein_ennen_myyntia(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)

    def test_luvut_oikein_edullisen_myytya_kateisella(self):
        vaihtoraha = self.kassapaate.syo_edullisesti_kateisella(300)

        self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)
        self.assertEqual(vaihtoraha, 60)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_luvut_oikein_maukkaan_myytya_kateisella(self):
        vaihtoraha = self.kassapaate.syo_maukkaasti_kateisella(500)

        self.assertEqual(self.kassapaate.kassassa_rahaa, 100400)
        self.assertEqual(vaihtoraha, 100)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_kateisraha_ei_riita_edulliseen(self):
        vaihtoraha = self.kassapaate.syo_edullisesti_kateisella(200)

        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(vaihtoraha, 200)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_kateisraha_ei_riita_maukkaaseen(self):
        vaihtoraha = self.kassapaate.syo_maukkaasti_kateisella(200)

        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(vaihtoraha, 200)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_korttimaksu_edulliseen_onnistuu(self):
        self.assertTrue(self.kassapaate.syo_edullisesti_kortilla(self.maksukortti))
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_korttimaksu_maukkaaseen_onnistuu(self):
        self.assertTrue(self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti))
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_korttimaksu_edulliseen_ei_riita_rahat(self):
        kortti = Maksukortti(100)
        self.assertFalse(self.kassapaate.syo_edullisesti_kortilla(kortti))
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_korttimaksu_maukkaaseen_ei_riita_rahat(self):
        kortti = Maksukortti(100)
        self.assertFalse(self.kassapaate.syo_maukkaasti_kortilla(kortti))
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_lataa_rahaa_kassasta_positiivinen(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 500)
        self.assertEqual(self.maksukortti.saldo,1500)
        self.assertEqual(self.kassapaate.kassassa_rahaa,100500) # En ole varma onko tehtävässä virhe? Nythän voidaan dupettaa rahaa loputtomiin. Tulee eräs kummelit-sketsi mieleen.

    def test_lataa_rahaa_kassasta_negatiivinen(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, -500)
        self.assertEqual(self.maksukortti.saldo,1000)
        self.assertEqual(self.kassapaate.kassassa_rahaa,100000)

