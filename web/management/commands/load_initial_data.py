from django.core.management.base import BaseCommand
from web.models import City, District, Vet

class Command(BaseCommand):
    help = "Gerçek şehir, ilçe ve veteriner verilerini yükler"

    def handle(self, *args, **kwargs):
        veri = {
            "İstanbul": {
                "Kadıköy": [
                    ("VetKadıköy Veteriner Polikliniği", "Caferağa Mahallesi Halisefendi Sok. No:9/A Kadıköy - İstanbul", "02163303592"),
                    ("Feneryolu Veteriner Polikliniği", "Feneryolu Mahallesi Kadıköy - İstanbul", "05362001930")
                ],
                "Üsküdar": [
                    ("VetArt Veteriner Kliniği", "İcadiye Mah. Cumhuriyet Cad. No:57 Üsküdar - İstanbul", "02165530112"),
                    ("Vetmedica Veteriner Kliniği", "Aziz Mahmut Hüdayi Mah. Halk Cad. No:80/B Üsküdar - İstanbul", "05550946652")
                ],
                "Beşiktaş": [
                    ("Heka Veteriner Kliniği", "Türkali Mah. Mısırlıbahçe Sok. No:70-A Beşiktaş - İstanbul", "05012417258"),
                    ("Petsmart Veteriner Kliniği", "Dikilitaş Mah. Asude Sok. No:17/A Beşiktaş - İstanbul", "02122599290")
                ],
            },
            "Ankara": {
                "Çankaya": [
                    ("Çankaya Vet Merkezi", "Üsküp Cad. No:26/B Çankaya - Ankara", "03124664555"),
                    ("Pet Care Center", "Alacatlı Mah. 3315 Sok. No:18 Çankaya - Ankara", "05364032273")
                ],
                "Keçiören": [
                    ("Keçiören Vet Kliniği", "Kuşcağız Mah. Sanatoryum Cad. 249/A Keçiören - Ankara", "03129997932"),
                    ("Lions Vet Kliniği", "Etlik Mah. Etlik Cad. 137/B Keçiören - Ankara", "03123262244")
                ],
                "Yenimahalle": [
                    ("Yenimahalle Vet Kliniği", "Ragıp Tüzün Cad. 75/A Yenimahalle - Ankara", "03123436070"),
                    ("Anka Vet Kliniği", "Kentkoop Mah. 1859. Sok. No:17/B Yenimahalle - Ankara", "03123542652")
                ],
            },
            "İzmir": {
                "Konak": [
                    ("Mira Vet Kliniği", "Mithat Paşa Cad. 99/1 Sok. No:1 Konak - İzmir", "02322442802"),
                    ("PattePasteur Vet", "Güzelyalı Mah. 54. Sok. No:5/D Konak - İzmir", "05551970627")
                ],
                "Bornova": [
                    ("Doğa Vet Polikliniği", "Kazım Dirik Mah. 220 Sok. No:7 Bornova - İzmir", "02325202575"),
                    ("Mascote Vet Kliniği", "Kazımdirik Mah. 185. Sok. No:54/A Bornova - İzmir", "05436777919")
                ],
                "Karşıyaka": [
                    ("Pekin Vet Kliniği", "Bahariye Mah. Zübeyde Hanım Cad. No:84/A Karşıyaka - İzmir", "02323729993"),
                    ("VetCity", "Goncalar Mah. Girne Cad. No:44 Karşıyaka - İzmir", "02323652525")
                ],
            }
        }

        for sehir_adi, ilceler in veri.items():
            city, _ = City.objects.get_or_create(name=sehir_adi)
            for ilce_adi, vet_listesi in ilceler.items():
                district, _ = District.objects.get_or_create(name=ilce_adi, city=city)
                for vet_adi, adres, telefon in vet_listesi:
                    Vet.objects.get_or_create(
                        name=vet_adi,
                        address=adres,
                        phone=telefon,
                        city=city,
                        district=district
                    )

        self.stdout.write(self.style.SUCCESS("✅ Gerçek veteriner verileri başarıyla yüklendi!"))
