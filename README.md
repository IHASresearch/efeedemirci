# İHA Teknolojileri — Haftalık Çalışmalar

Bu repo; şifreli kablosuz haberleşme, frekans atlama, ağ ölçümleri ve makine öğrenmesi çalışmalarını içerir. Her hafta ayrı bir deney olarak düzenlenmiştir. Ayrıca video üzerinde drone tespiti yapan bir Python uygulaması ve RGB görüntülerden sentetik kızılötesi görüntü üreten midterm projesi bulunur.

## Klasörler

| Klasör | Çalışma | Kullanılan donanım |
|---|---|---|
| `week2` | AES-128 ile şifreli, tek yönlü mesaj iletimi | Arduino Uno/Nano + nRF24L01 |
| `week3` | Wi-Fi bağlantısında paket kaybı ve sinyal ölçümü | ESP32 sunucu + ESP8266/ESP32 istemci |
| `week4` | Frekans atlamalı, şifreli ve çift yönlü haberleşme | Arduino Uno/Nano + nRF24L01 |
| `week5` | Küçük bir sinir ağıyla paket düşürme belirtilerinin tespiti | ESP32 dedektör + ESP8266/ESP32 istemci |
| `drone-tespit` | YOLO modeliyle videodaki drone’ların tespiti | Python çalıştırabilen bilgisayar |
| [`midterm`](midterm/) | Pix2pix ile RGB görüntüsünden sentetik IR üretimi, Windows uygulaması ve proje raporu | Hazır uygulama: Windows x64 CPU |

## Haftalar nasıl çalışır?

### Hafta 2 — Şifreli mesajlaşma

`sender` kartı, oluşturduğu mesajı AES-128 ECB ile şifreleyerek nRF24L01 üzerinden gönderir. `receiver` kartı paketi alır, şifreyi çözer ve mesajı seri monitöre yazar. İki kart sabit kanal 12’de, yani 2412 MHz’de haberleşir.

### Hafta 3 — Ağdan veri toplama

ESP32 sunucu `UAV_LINK` adlı Wi-Fi ağını oluşturur. İstemci bu ağa bağlanarak düzenli UDP paketleri gönderir. Sunucu her saniye paket kaybı, RSSI ve tekrar gönderim gibi ölçümleri özetler; `logger.py` bu çıktıyı CSV dosyasına kaydeder.

`data_collector.ino` ayrı bir genel Wi-Fi dinleyicisidir. Python logger ise `server/server.ino` çıktısıyla kullanılır. İsteğe bağlı `flooder` kodu deney sırasında yoğun trafik oluşturur. Ölçüm istemcisi ağa ilk bağlanan cihaz olmalıdır.

### Hafta 4 — Frekans atlamalı bağlantı

İki kart sekiz kanal arasında beş saniyede bir geçiş yapar. Verici mesajları şifreleyerek gönderir; alıcı vericinin saatine uyum sağlar. Alıcı, alındı onayının içine kendi mesajını ekleyerek ters yönde de veri iletir. Bağlantı kesilirse alıcı yeniden senkronizasyon arar.

### Hafta 5 — TinyML ile tespit

`tinyml_attack_detection` altında veri toplama, eğitim ve kart üzerinde tahmin aşamaları bulunur:

1. `sender`, normal iletişim ve paket düşürme simülasyonu arasında geçiş yapar.
2. `receiver` ölçümleri üretir, `logger.py` CSV dosyasına kaydeder.
3. `train.py`, verilerle küçük bir sinir ağı eğitir ve `detector/model.h` dosyasını oluşturur.
4. `detector`, ölçümleri modele vererek normal/atak tahminini seri monitörde gösterir.

Hazır model `model.h` içindedir. Yeni veri toplandığında `train.py` içindeki CSV yolu güncellenerek yeniden eğitim yapılabilir.

## Drone tespiti

`drone-tespit/drone_tespit.py`, `drone_model.pt` modelini kullanarak `Smarter Drone Swarms.mp4` videosundaki drone’ları tespit eder. Bulunan drone’ların etrafına kutu çizer ve güven değerlerini görüntüler. Ekranın yan panelinde drone bulunup bulunmadığını gösterir; işlenmiş videoyu `drone_sonuc.mp4` olarak kaydeder.


## Midterm — RGB görüntüsünden sentetik IR üretimi

[midterm](midterm/) klasöründe, DroneVehicle'dan seçilen 12.000 farklı eşleştirilmiş RGB–IR görüntüsüyle eğitilmiş pix2pix modelinin masaüstü uygulaması, kaynak kodu ve değiştirilmemiş proje raporu bulunur. 512 × 512 model 100 epocha tamamlanmış; kayıtlı ağırlıklar arasında genel ve çok karanlık doğrulama SSIM değeri daha yüksek olan 35. epoch uygulama için seçilmiştir.

**[Model dahil Windows uygulamasını indir](https://github.com/IHASresearch/efeedemirci/releases/download/midterm-v1.0/RGB_IR_Windows_Epoch35.zip)** → ZIP'i tamamen çıkar → `RGB_IR/RGB_IR.exe` dosyasını aç → RGB seç → sentetik IR üret → PNG kaydet. Python ve GPU kurulumu gerekmez. `_internal` ve `models` klasörleri EXE'nin yanında kalmalıdır.

**Code → Download ZIP yalnızca kaynak kodunu getirir.** Hazır çalıştırılabilir uygulama ve büyük ağırlık dosyası Release'te sunulur. Kaynak koduyla çalıştırma ve diğer işletim sistemlerine ilişkin koşullar [midterm README'sinde](midterm/README.md) açıklanmıştır.

**[Proje raporu](midterm/rapor/İzzetEfeDemirci_İHATeknolojileri.pdf)** · **[Kullanım ve yöntem](midterm/README.md)**

Çıktı sentetik bir IR tahminidir; fiziksel sıcaklık ölçümü değildir. Başarım aynı 100 doğrulama görüntüsü üzerinde ölçülmüştür; bağımsız final test sonucu değildir.
