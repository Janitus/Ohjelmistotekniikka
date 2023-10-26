import unittest
from ..maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.kortti = Maksukortti(1000)

    def test_konstruktori_asettaa_saldon_oikein(self):
        self.assertEqual(str(self.kortti), "Kortilla on rahaa 10.00 euroa")


    def test_syo_edullisesti_vahentaa_saldoa_oikein(self):
        self.kortti.syo_edullisesti()

        self.assertEqual(self.kortti.saldo_euroina(), 7.5)

    def test_syo_maukkaasti_vahentaa_saldoa_oikein(self):
        self.kortti.syo_maukkaasti()

        self.assertEqual(self.kortti.saldo_euroina(), 6.0)

    def test_syo_edullisesti_ei_vie_saldoa_negatiiviseksi(self):
        self.kortti.syo_edullisesti()

        self.assertEqual(self.kortti.saldo_euroina(), 7.5)

    def test_syo_edullisesti_ei_vie_saldoa_negatiiviseksi(self):
        self.kortti.syo_maukkaasti()

        self.assertGreaterEqual(self.kortti.saldo_euroina(), 0)

    def test_kortille_voi_ladata_rahaa(self):
        self.kortti.lataa_rahaa(2500)

        self.assertEqual(str(self.kortti), "Kortilla on rahaa 35.00 euroa")

    def test_kortin_saldo_ei_ylita_maksimiarvoa(self):
        self.kortti.lataa_rahaa(20000)

        self.assertEqual(str(self.kortti), "Kortilla on rahaa 150.00 euroa")

    def test_kortin_saldo_ei_muutu_negatiivisella_latauksella(self):
        self.kortti.lataa_rahaa(-100)

        self.assertEqual(self.kortti.saldo, 1000)

    def test_voi_ostaa_edullisen_jos_rahat_riittaa(self):
        kortti = Maksukortti(250)
        kortti.syo_maukkaasti()

        self.assertEqual(kortti.saldo,250)
        kortti.syo_edullisesti()
        self.assertEqual(kortti.saldo,0)

    def test_voi_ostaa_maukkaan_jos_rahat_riittaa(self):
        kortti = Maksukortti(400)
        kortti.syo_maukkaasti()

        self.assertEqual(kortti.saldo,0)
        kortti.syo_edullisesti()
        self.assertEqual(kortti.saldo,0)
