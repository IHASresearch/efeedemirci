from pathlib import Path
import threading
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from PIL import Image, ImageOps, ImageTk
from inference import load_model, predict

ROOT = Path(sys.executable).resolve().parent if getattr(sys, 'frozen', False) else Path(__file__).resolve().parent
MODEL = ROOT / 'models' / 'pix2pix_512_epoch35' / '35_net_G.pth'


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('İHA RGB → Sentetik IR')
        self.geometry('820x560')
        self.source = self.result = self.model = None
        self.status = tk.StringVar(value='Başlamak için bir RGB görüntüsü seçin.')
        ttk.Label(self, text='RGB görüntüsünden sentetik termal görüntü', font=('Segoe UI', 16, 'bold')).pack(pady=15)
        ttk.Label(self, text='Sonuç tahminidir; gerçek sıcaklık ölçümü değildir.').pack()
        ttk.Label(self, text='Seçilen model: 512 × 512 | epoch 35').pack()
        controls = ttk.Frame(self)
        controls.pack(pady=15)
        self.choose_button = ttk.Button(controls, text='Görüntü seç', command=self.choose)
        self.choose_button.pack(side='left', padx=5)
        self.crop_border = tk.BooleanVar(value=False)
        ttk.Checkbutton(self, text='Orijinal DroneVehicle görüntüsü: 100 piksel kenarlığı kırp (840 × 712)', variable=self.crop_border).pack()
        self.generate = ttk.Button(controls, text='Sentetik IR üret', command=self.start)
        self.generate.pack(side='left', padx=5)
        self.save_button = ttk.Button(controls, text='Sonucu kaydet', command=self.save, state='disabled')
        self.save_button.pack(side='left', padx=5)
        pictures = ttk.Frame(self)
        pictures.pack(pady=8)
        self.panels = []
        for title in ('RGB girdi', 'Sentetik IR'):
            panel = ttk.Frame(pictures)
            panel.pack(side='left', padx=20)
            ttk.Label(panel, text=title, font=('Segoe UI', 11, 'bold')).pack()
            label = ttk.Label(panel)
            label.pack(pady=8)
            self.panels.append(label)
        ttk.Label(self, textvariable=self.status, wraplength=760).pack(pady=12)

    def show_image(self, index, image):
        preview = ImageOps.contain(image.convert('RGB'), (320, 320))
        photo = ImageTk.PhotoImage(preview)
        self.panels[index].configure(image=photo)
        self.panels[index].image = photo

    def choose(self):
        path = filedialog.askopenfilename(filetypes=[('Görüntüler', '*.jpg *.jpeg *.png *.bmp'), ('Tüm dosyalar', '*.*')])
        if not path:
            return
        try:
            with Image.open(path) as image:
                self.source = ImageOps.exif_transpose(image).convert('RGB').copy()
            self.result = None
            self.panels[1].configure(image='')
            self.save_button.configure(state='disabled')
            self.show_image(0, self.source)
            self.status.set('Görüntü seçildi. Sentetik IR üret düğmesine basın.')
        except Exception as error:
            messagebox.showerror('Görüntü açılamadı', str(error))

    def install_model(self):
        if str(self.generate['state']) == 'disabled':
            return
        path = filedialog.askopenfilename(title='Drive’dan indirdiğiniz son 100_net_G.pth dosyasını seçin', filetypes=[('Model ağırlığı', '*.pth')])
        if not path:
            return
        try:
            import shutil
            checked = load_model(path)
            MODEL.parent.mkdir(parents=True, exist_ok=True)
            if Path(path).resolve() != MODEL.resolve():
                temp = MODEL.with_suffix('.pth.tmp')
                shutil.copyfile(path, temp)
                temp.replace(MODEL)
            self.model = checked
            self.status.set('Model yüklendi. RGB görüntüsü seçerek çalıştırabilirsiniz.')
        except Exception as error:
            messagebox.showerror('Model yüklenemedi', str(error))

    def start(self):
        if self.source is None:
            messagebox.showinfo('Görüntü gerekli', 'Önce bir RGB görüntüsü seçin.')
            return
        if not MODEL.is_file():
            messagebox.showerror('Model bulunamadı', f'Eğitilmiş model bu konumda olmalı:\n{MODEL}')
            return
        if self.crop_border.get() and self.source.size != (840, 712):
            messagebox.showerror('Boyut uygun değil', 'Kenarlık kırpma yalnızca 840 × 712 orijinal DroneVehicle görüntüleri içindir.')
            return
        self.generate.configure(state='disabled')
        self.choose_button.configure(state='disabled')
        self.save_button.configure(state='disabled')
        self.status.set('Model çalışıyor. İlk çalıştırma biraz sürebilir...')
        source = self.source.copy()
        if self.crop_border.get():
            source = source.crop((100, 100, 740, 612))

        def work():
            try:
                if self.model is None:
                    self.model = load_model(MODEL)
                result = predict(self.model, source)
                self.after(0, lambda: self.complete(result))
            except Exception as error:
                self.after(0, lambda msg=str(error): self.failed(msg))

        threading.Thread(target=work, daemon=True).start()

    def complete(self, result):
        self.result = result
        self.show_image(1, result)
        self.generate.configure(state='normal')
        self.choose_button.configure(state='normal')
        self.save_button.configure(state='normal')
        self.status.set('Sentetik görüntü üretildi. Sonucu kaydedebilirsiniz.')

    def failed(self, error):
        self.generate.configure(state='normal')
        self.choose_button.configure(state='normal')
        self.status.set('Görüntü üretilemedi.')
        messagebox.showerror('İşlem başarısız', error)

    def save(self):
        path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('PNG görüntüsü', '*.png')])
        if path:
            try:
                self.result.save(path)
                self.status.set('Görüntü kaydedildi: ' + path)
            except OSError as error:
                messagebox.showerror('Kaydedilemedi', str(error))


if __name__ == '__main__':
    Application().mainloop()
