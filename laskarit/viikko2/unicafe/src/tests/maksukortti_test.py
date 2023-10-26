import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_saldo_on_oikein(self):
        self.assertEqual(self.maksukortti.saldo,1000)

    def test_saldo_kasvaa_oikein(self):
        self.maksukortti.lataa_rahaa(1000)
        self.assertEqual(self.maksukortti.saldo,2000)

    def test_rahan_ottaminen_toimii(self):
        self.maksukortti.ota_rahaa(500)
        self.assertEqual(self.maksukortti.saldo,500)

        self.assertFalse(self.maksukortti.ota_rahaa(1000))
        self.assertTrue(self.maksukortti.ota_rahaa(200))

    def test_saldo_euroina_on_oikein(self):
        eurot_senteiksi = self.maksukortti.saldo_euroina() * 100
        self.assertAlmostEqual(self.maksukortti.saldo,eurot_senteiksi)
        
    def test_tostring_nayttaa_oikealta(self):
        self.assertEqual(str(self.maksukortti),"Kortilla on rahaa 10.00 euroa")