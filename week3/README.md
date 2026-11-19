# Hafta 3 - ESP32 Wi-Fi olcumleri
Server: ESP32. Client: ESP32 veya ESP8266. Ilk once client baglanmalidir; PC/flooder sonra baglanir.
COM5 sunucu seri portu icin varsayimdir; diger kartin portunu ayrica secin.
data_collector.ino bagimsiz genel Wi-Fi dinleyicidir; logger.py ise server/server.ino CSV bicimini bekler.
logger.py varsayilan olarak deney trafigi uretir. Yalniz kayit icin: python logger.py COM5 --manual
Fiziksel test yapilmadi.
