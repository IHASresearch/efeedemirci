# IHASresearch haftalik calismalar
Kaynak: https://github.com/IHASresearch/tolgahan.keles
week2: Uno/Nano + nRF24, AES-128 ECB, kanal 12, tek yon.
week3: ESP32 server + ESP8266/ESP32 client, Wi-Fi/UDP olcum.
week4: Uno/Nano + nRF24, AES-128 ECB, 8 kanal, 5 saniye/kanal, ACK payload ile cift yon.
week5/tinyml_attack_detection: ESP32 receiver/detector + ESP8266/ESP32 sender.
midterm bilerek bos. drone-tespit mevcut haliyle korunur.

## Uno / klasik Nano baglantisi (iki tarafta ayni)
nRF24 CE=D7, CSN=D8, SCK=D13, MOSI=D11, MISO=D12, VCC=3.3V, GND=GND.
Uno/Nano SPI master icin D10 cikis olarak ayarlanir. nRF24 VCC'ye 5V vermeyin.
Kutuphaneler: RF24 (TMRh20), Crypto (Rhys Weatherley). ESP32 mbedtls bagimliligi AVR kodlarindan cikarildi.
Seri monitor 115200 baud. COM5 bir kart icin secilir; iki kart ayni anda ayni COM portunu kullanmaz.
Uno kart secimi: arduino:avr:uno. Klasik Nano: arduino:avr:nano (eski bootloader gerekebilir).
Her sender/receiver ayri karta yuklenir; haftalar ayri deneylerdir.

## Sinirlar
ECB ve sabit ornek anahtarlar egitim amaclidir. Oturum numarasi guvenli rastgelelik saglamaz.
Hafta 4 log yuzdeleri AVR icin tam sayiya yuvarlanir. Mikro-saniye zaman damgasi millis ile 1 ms cozunurlukte uretilir.
Hafta 5 modeli kaynak deneyden alinmistir; kendi olcumlerinizle yeniden egitim gerekir.
ESP32 kart paketi bu bilgisayarda bulunmadigi icin ESP32 derlemesi/donanım testi yapilmadi.
