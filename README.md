# İHA Teknolojileri — Haftalık Çalışmalar

Bu repo; şifreli kablosuz haberleşme, frekans atlama, ağ ölçümleri ve makine öğrenmesi çalışmalarını içerir. Her hafta ayrı bir deney olarak düzenlenmiştir. Ayrıca video üzerinde drone tespiti yapan bir Python uygulaması bulunur.

## Klasörler

| Klasör | Çalışma | Kullanılan donanım |
|---|---|---|
| `week2` | AES-128 ile şifreli, tek yönlü mesaj iletimi | Arduino Uno/Nano + nRF24L01 |
| `week3` | Wi-Fi bağlantısında paket kaybı ve sinyal ölçümü | ESP32 sunucu + ESP8266/ESP32 istemci |
| `week4` | Frekans atlamalı, şifreli ve çift yönlü haberleşme | Arduino Uno/Nano + nRF24L01 |
| `week5` | Küçük bir sinir ağıyla paket düşürme belirtilerinin tespiti | ESP32 dedektör + ESP8266/ESP32 istemci |
| `drone-tespit` | YOLO modeliyle videodaki drone’ların tespiti | Python çalıştırabilen bilgisayar |

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

Hazır model `model.h` içindedir. Yeni veri toplandığında `train.py` içindeki CSV yolu güncellenerek yeniden eğitim yapılabilir. Modelin tahmini, ölçülen bağlantı bozulmalarına dayanır; paket kaybının nedenini tek başına kanıtlamaz.

## Arduino bağlantısı ve kullanım

Uno ve klasik Nano için her iki nRF24L01 modülü de aynı şekilde bağlanır:

| nRF24L01 | Uno / Nano |
|---|---|
| VCC | 3.3V |
| GND | GND |
| CE | D7 |
| CSN | D8 |
| SCK | D13 |
| MOSI | D11 |
| MISO | D12 |

**nRF24L01 beslemesine 5V verilmemelidir.** Arduino IDE’de `RF24` ve `Crypto` kütüphaneleri kurulmalıdır. Wi-Fi haftaları için kullanılan karta uygun ESP32 veya ESP8266 kart paketi gerekir.

İlgili haftanın `sender.ino` ve `receiver.ino` dosyalarını ayrı kartlara yükleyin. Seri monitörü **115200 baud** ile açın. Portu kartın bağlı olduğu bağlantıya göre seçin; COM5 kullanılan örnek porttur. İki kart aynı anda bağlıysa portları farklı olacaktır.

## Drone tespiti

Gerekli Python paketleri:

```powershell
pip install ultralytics opencv-python numpy
```

Repo kökünden çalıştırma:

```powershell
python drone-tespit/drone_tespit.py
```

Uygulama `drone_model.pt` modelini kullanarak `Smarter Drone Swarms.mp4` videosunu işler. Tespitleri ekranda gösterir ve sonucu aynı klasöre `drone_sonuc.mp4` olarak kaydeder. Çıkmak için **Q** tuşuna basılır. Video ve güven eşiği scriptin başından değiştirilebilir.

TinyML veri toplama ve eğitimi için ayrıca `pyserial`, `numpy`, `pandas` ve `scikit-learn` paketleri kullanılır. Seri port ayarı logger dosyasından yapılır.

## Doğrulama durumu

Hafta 2 ve hafta 4 alıcı/verici kodları Uno hedefi için derlenmiştir. ESP32 kodlarının derlemesi ve kartlar arası fiziksel testler henüz tamamlanmamıştır. Şifreleme örneklerinde kullanılan sabit anahtarlar ve ECB modu eğitim amaçlıdır.
