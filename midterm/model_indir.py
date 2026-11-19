"""Seçilen epoch 35 ağırlığını indirir ve SHA-256 ile doğrular."""
from pathlib import Path
import hashlib
import urllib.request

URL = 'https://github.com/IHASresearch/efeedemirci/releases/download/midterm-v1.0/35_net_G.pth'
SHA256 = '8d361a48d4df0109ad282f6560519c0ebbf2dfea1557ee1fd67680c11c9b478f'
TARGET = Path(__file__).resolve().parent / 'models/pix2pix_512_epoch35/35_net_G.pth'


def digest(path):
    value = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(8 * 1024 * 1024), b''):
            value.update(block)
    return value.hexdigest()


def main():
    if TARGET.is_file():
        if digest(TARGET) != SHA256:
            raise RuntimeError(f'Mevcut dosyanın SHA-256 değeri yanlış: {TARGET}')
        print('Model zaten hazır:', TARGET)
        return
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    partial = TARGET.with_suffix('.pth.part')
    print('Model indiriliyor: yaklaşık 208 MiB...', flush=True)
    request = urllib.request.Request(URL, headers={'User-Agent': 'RGB-IR-Midterm'})
    size = 0
    with urllib.request.urlopen(request, timeout=60) as response, partial.open('wb') as f:
        for block in iter(lambda: response.read(1024 * 1024), b''):
            f.write(block)
            size += len(block)
            if size % (16 * 1024 * 1024) == 0:
                print(f'{size / 1024**2:.0f} MiB indirildi...', flush=True)
    if digest(partial) != SHA256:
        raise RuntimeError('İndirme doğrulanamadı; uygulama ağırlığı değiştirilmedi. Tekrar deneyin.')
    partial.replace(TARGET)
    print('SHA-256 doğrulandı. Model hazır:', TARGET)


if __name__ == '__main__':
    main()
