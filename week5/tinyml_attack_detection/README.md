# Hafta 5 — TinyML ile Paket Düşürme Tespiti

Bu çalışma, iki kart arasındaki Wi-Fi iletişiminden elde edilen ölçümleri kullanarak normal iletişim ile paket düşürme simülasyonunu sınıflandırır. Küçük bir sinir ağı bilgisayarda eğitilir ve ESP32 üzerinde çalıştırılır.

## Çalışma akışı

1. **Veri gönderimi:** ESP32 veya ESP8266 istemci, ESP32 sunucunun oluşturduğu `UAV_LINK` ağına bağlanır. Normal durumda yaklaşık saniyede 100 UDP paketi gönderir.
2. **Paket düşürme simülasyonu:** İstemci 30 saniye normal, 30 saniye simülasyon döngüsüyle çalışır. Simülasyonda bazı paketleri göndermez ve radyo ayarlarını değiştirir. Paketlerde sıra numarası ve normal/simülasyon etiketi bulunur.
3. **Ölçüm ve kayıt:** Sunucu bir saniyelik aralıklarla alınan ve kaybolan paketleri, paket geliş aralıklarını ve sinyal istatistiklerini hesaplar. `logger.py` seri porttan gelen ölçümleri CSV dosyasına kaydeder.
4. **Model eğitimi:** `train.py`, CSV verisini kullanarak modeli eğitir; normalizasyon değerlerini ve ağırlıkları `detector/model.h` dosyasına yazar.
5. **Kart üzerinde tespit:** `detector`, aynı ölçümleri modele verir. Normal/atak tahminini, model çıkışını ve tahmin süresini seri monitörde gösterir.

## Dosyalar

| Dosya | İşlevi |
|---|---|
| `sender/sender.ino` | ESP32 veya ESP8266 üzerinde paket gönderimini ve paket düşürme simülasyonunu yürütür. |
| `receiver/receiver.ino` | ESP32 üzerinde Wi-Fi ağını oluşturur ve ölçümleri CSV satırları halinde üretir. 500 normal ve 500 simülasyon kaydı hedefler. |
| `logger.py` | Sunucunun seri port çıktısını tarih ve saat içeren bir CSV dosyasına kaydeder. |
| `drop_dataset.csv` | Model eğitiminde kullanılan ölçüm verilerini içerir. |
| `train.py` | Veriyi hazırlar, sinir ağını eğitir ve modeli C dizilerine dönüştürür. |
| `detector/detector.ino` | ESP32 üzerinde ölçüm yapar ve eğitilmiş modelle tahmin üretir. Tahminleri paket etiketleriyle karşılaştırarak sonuçları sayar. |
| `detector/model.h` | Modelin katman ağırlıklarını ve girişleri ölçeklemek için kullanılan değerleri içerir. |

## Modelin kullandığı ölçümler

Model; alınan ve kaybolan paket sayısı, kayıp oranı, en uzun ardışık kayıp, paket geliş aralıklarının ortalaması ve değişkenliği, en büyük geliş aralığı, RSSI değişkenliği, tekrar gönderim oranı ve gözlenen Wi-Fi çerçevesi sayısı olmak üzere **10 özellik** kullanır.

Sinir ağı yapısı **10 giriş → 16 nöron → 8 nöron → 1 çıkış** şeklindedir. Çıkış değeri 0,5'in üzerindeyse atak, diğer durumda normal tahmini üretilir.

Veri toplama için `sender` ve `receiver`; modelle tespit için `sender` ve `detector` birlikte kullanılır. Sunucu ve dedektör ESP32 üzerinde, istemci ise ESP32 veya ESP8266 üzerinde çalışır.
