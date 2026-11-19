# Midterm — RGB görüntüsünden sentetik IR üretimi

Bu proje, İHA görüntülerindeki RGB görünümü pix2pix modeliyle sentetik kızılötesi (IR) görünüme dönüştürür. Kullanıcı bir fotoğraf seçer, tahmini üretir ve PNG olarak kaydeder. Hazır uygulamada 512 × 512 giriş boyutuyla çalışan **35. epoch üretici ağırlığı** kullanılır.

## En kolay kullanım — Windows x64

**[Model dahil hazır Windows uygulamasını indir](https://github.com/IHASresearch/efeedemirci/releases/download/midterm-v1.0/RGB_IR_Windows_Epoch35.zip)**

1. Yukarıdaki ZIP'i indirin ve **tamamını** bir klasöre çıkarın. ZIP'in içinden çalıştırmayın.
2. Çıkan `RGB_IR` klasöründe **`RGB_IR.exe` dosyasını açın**. Python, Colab veya GPU kurulumu gerekmez; çıkarım CPU'da yapılır.
3. **Görüntü seç** ile JPG, JPEG, PNG veya BMP dosyanızı seçin.
4. **Sentetik IR üret** düğmesine basın ve sonucu bekleyin.
5. **Sonucu kaydet** ile PNG dosyasını kaydedin.

`_internal` ve `models` klasörleri EXE'nin yanında kalmalıdır. Model ZIP'e dahildir; ayrıca model indirmenize gerek yoktur. İlk açılış ve üretim süresi bilgisayara bağlıdır. Girdi kareye boyutlandırılır; dikdörtgen fotoğrafların en-boy oranı değişebilir.

**Kenarlık kırpma** kutusunu yalnızca orijinal 840 × 712 DroneVehicle görüntülerinde işaretleyin. Kendi fotoğraflarınızda kapalı bırakın.

Hazır EXE Windows x64 için paketlenmiştir. macOS ve Linux, Windows EXE'sini doğrudan çalıştırmaz. Bu sistemler için aşağıdaki Python yolu kullanılabilir; bu sistemlerde uçtan uca test yapılmamıştır. Her işletim sistemi ve donanımda sorunsuz çalışma garantisi verilmez.

## Yalnızca midterm klasörünü veya kaynak ZIP'ini indirdiyseniz

GitHub **Code → Download ZIP** kaynak kodunu ve raporu içerir. Büyük model ve Windows çalışma zamanı GitHub Release'te tutulur. Python kurulumu yapmadan kullanmak için yukarıdaki hazır uygulama bağlantısını açın.

Python ile çalıştırmak isteyenler için, Python 3.12 ve Tkinter kurulu bir sistemde terminali bu `midterm` klasöründe açın:

```powershell
# Windows PowerShell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install torch==2.15.0 --index-url https://download.pytorch.org/whl/cpu
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe model_indir.py
.\.venv\Scripts\python.exe uygulama.py
```

macOS veya Linux için Python 3.12 ve Tkinter bulunan bir ortamda eşdeğer komutlar:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python model_indir.py
.venv/bin/python uygulama.py
```

`model_indir.py` yaklaşık 208 MiB ağırlığı bu reponun Release'inden indirir ve SHA-256 değerini kontrol eder. İnternet yalnızca paketleri/modeli indirmek için gerekir; model hazırlandıktan sonra çıkarım yerelde yapılır.

## Yapılan çalışma

- Veri: DroneVehicle'dan **12.000 farklı RGB–IR çifti**; çok karanlık, orta parlaklık ve aydınlık gruplarından 4.000'er örnek. Bozuk çiftler dışlandı.
- Model: koşullu GAN tabanlı **pix2pix**, U-Net üretici ve PatchGAN ayırt edici.
- Eğitim: NVIDIA L4, batch 64, 512 × 512, 30 + 70 epoch. Ara sonrası G/D ağırlıkları yüklendi; optimizer yeniden başlatıldı.
- Model seçimi: her beş epochta kaydedilen ağırlıklar arasında genel ve çok karanlık doğrulama SSIM değeri en yüksek olan **35. epoch**.

| 512 model | Genel SSIM ↑ | Çok karanlık SSIM ↑ | Genel PSNR ↑ |
|---|---:|---:|---:|
| Epoch 35 — uygulamada kullanılan | 0,4166 | 0,3563 | 14,7003 dB |
| Epoch 100 | 0,4005 | 0,3328 | 14,9208 dB |

Bu sonuçlar aynı **100 doğrulama görüntüsüne** aittir. 512 çıktılar ortak değerlendirme için 256 × 256'ya indirilmiştir. Bağımsız final test sonucu değildir; 35. epoch her sahnede üstün değildir ve PSNR'de 100. epoch daha yüksektir. SSIM, yüzde doğruluk olarak yorumlanamaz.

## Rapor ve dosyalar

**[Proje raporunu aç](rapor/İzzetEfeDemirci_İHATeknolojileri.pdf)**

```text
midterm/
├── README.md
├── uygulama.py              # RGB seçme, tahmin ve PNG kaydetme
├── inference.py             # Model yükleme ve 512 boyutunda çıkarım
├── model_indir.py           # Release'ten doğrulanmış ağırlık indirme
├── requirements.txt
├── SHA256SUMS.txt
├── data/pix2pix_kaynak/     # Kullanılan ağ kodu ve özgün lisansı
└── rapor/                  
```

## Sınırlar ve kaynaklar

Çıktı **sentetik IR tahminidir; gerçek sıcaklık ölçümü değildir**. Model havadan görülen araç/yol sahneleriyle eğitilmiştir. Her RGB dosyasını kabul etmesi, tüm farklı sahnelerde doğru termal içerik ürettiği anlamına gelmez. RGB'de gözlenemeyen ısı bilgisi kesin olarak geri kazanılamaz.

- Pix2pix: https://arxiv.org/abs/1611.07004
- DroneVehicle: https://arxiv.org/abs/2003.02437
- Referans RGB–IR çalışması: https://arxiv.org/abs/2609.02556
- Kullanılan ağ kodu ve lisansı: [pytorch-CycleGAN-and-pix2pix](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix), commit `2a7afba2895d52556dd5dfe07e8555ef657ced6f`. Özgün lisans [data/pix2pix_kaynak/LICENSE](data/pix2pix_kaynak/LICENSE) içindedir.
