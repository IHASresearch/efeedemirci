# TinyML ile Paket DÃ¼ÅŸÃ¼rme (Drop) AtaÄŸÄ± Tespiti

Ä°ki kart arasÄ±ndaki Wi-Fi baÄŸlantÄ±sÄ±nda paket dÃ¼ÅŸÃ¼rme ataÄŸÄ±nÄ±, ESP32 Ã¼zerinde Ã§alÄ±ÅŸan kÃ¼Ã§Ã¼k bir sinir aÄŸÄ±yla tespit ediyoruz.

## AkÄ±ÅŸ

1. **Veri toplama:** `sender` atak simÃ¼lasyonu yapar, `receiver` aÄŸÄ±n durumunu Ã¶lÃ§er, `logger.py` bunu CSV'ye yazar.
2. **EÄŸitim:** `train.py` bu CSV ile kÃ¼Ã§Ã¼k bir MLP eÄŸitir ve `detector/model.h` dosyasÄ±nÄ± Ã¼retir.
3. **Tespit:** `detector` aynÄ± Ã¶lÃ§Ã¼mleri yapar ve modeli ESP32 Ã¼zerinde Ã§alÄ±ÅŸtÄ±rÄ±r.

## Dosyalar

| Dosya | GÃ¶revi |
|---|---|
| `sender/sender.ino` | Client (ESP32 veya ESP8266, aynÄ± kod). Saniyede 100 UDP paketi yollar. 30 sn normal, 30 sn atak dÃ¶ngÃ¼sÃ¼ yapar. Atakta paketlerin bir kÄ±smÄ±nÄ± gÃ¶ndermez ve TX gÃ¼cÃ¼nÃ¼ dÃ¼ÅŸÃ¼rÃ¼r. Her paket etiketini (0/1) taÅŸÄ±r. |
| `receiver/receiver.ino` | Server (ESP32). AP kurar, paketleri dinler. Her 1 sn iÃ§in kayÄ±p, paket aralÄ±ÄŸÄ±, RSSI, retry gibi deÄŸerleri tek bir CSV satÄ±rÄ± olarak yazar. 500 normal + 500 atak satÄ±rda durur. |
| `logger.py` | Receiver'Ä±n seri port Ã§Ä±ktÄ±sÄ±nÄ± CSV dosyasÄ±na kaydeder. |
| `drop_dataset.csv` | Toplanan veri seti (1000 satÄ±r). |
| `train.py` | MLP eÄŸitir (10 Ã¶zellik â†’ 16 â†’ 8 â†’ 1), test sonucunu yazar, aÄŸÄ±rlÄ±klarÄ± `detector/model.h` dosyasÄ±na C dizisi olarak kaydeder. |
| `detector/detector.ino` | Server'Ä±n tespit sÃ¼rÃ¼mÃ¼. Her pencerede modeli Ã§alÄ±ÅŸtÄ±rÄ±r, tahmini gerÃ§ek etiketle karÅŸÄ±laÅŸtÄ±rÄ±p doÄŸruluÄŸu yazar. |
| `detector/model.h` | `train.py`'nin Ã¼rettiÄŸi model (elle deÄŸiÅŸtirilmez). |

## KullanÄ±m

Python script'lerinde ayarlar dosyanÄ±n Ã¼stÃ¼ndeki **PARAMETRELER** kÄ±smÄ±ndadÄ±r (port, dosya yolu, epoch).

```powershell
# 1) Veri toplama: sender'Ä± ve receiver'Ä± yÃ¼kle, sonra
python logger.py

# 2) EÄŸitim
python train.py

# 3) Tespit: sender'Ä± ve detector'Ä± yÃ¼kle
arduino-cli compile --fqbn esp32:esp32:esp32 detector
arduino-cli upload -p COM9 --fqbn esp32:esp32:esp32 detector
arduino-cli monitor -p COM9 -c baudrate=115200
```

Sender'Ä± ESP8266'ya yÃ¼klemek iÃ§in sadece kart tipini deÄŸiÅŸtirmek yeterli:

```powershell
arduino-cli upload -p COM6 --fqbn esp8266:esp8266:nodemcuv2 sender
```

Receiver ve detector sadece ESP32'de Ã§alÄ±ÅŸÄ±r (ESP32'nin sniffer API'sini kullanÄ±yorlar).

Mevcut veriyle test doÄŸruluÄŸu **%98.5**. Model 321 parametreden oluÅŸur (1.3 KB).

COM5 sunucu/detector icindir. Yeni logger CSV dosyasini train.py icindeki CSV yoluna yazin. Yeni olcumlerle modeli train.py kullanarak yeniden egitebilirsiniz.
