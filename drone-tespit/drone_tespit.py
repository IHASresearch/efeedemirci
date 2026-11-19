from pathlib import Path

import cv2
import numpy as np
from ultralytics import YOLO


KLASOR = Path(__file__).resolve().parent
VIDEO = KLASOR / "Smarter Drone Swarms.mp4"
MODEL = KLASOR / "drone_model.pt"
CIKTI = KLASOR / "drone_sonuc.mp4"
GUVEN = 0.20


def main():
    model = YOLO(str(MODEL))
    video = cv2.VideoCapture(str(VIDEO))
    if not video.isOpened():
        raise RuntimeError(f"Video acilamadi: {VIDEO}")

    genislik = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    yukseklik = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS) or 25
    panel = 300
    kayit = cv2.VideoWriter(str(CIKTI), cv2.VideoWriter_fourcc(*"mp4v"), fps, (genislik + panel, yukseklik))
    if not kayit.isOpened():
        video.release()
        raise RuntimeError(f"Cikti videosu olusturulamadi: {CIKTI}")

    try:
        while True:
            ok, kare = video.read()
            if not ok:
                break
            # Modelin iki sinifi da drone turudur: quadcopter ve fixed-wing.
            sonuc = model.predict(kare, conf=GUVEN, agnostic_nms=True, verbose=False)[0]
            for kutu in sonuc.boxes:
                x1, y1, x2, y2 = map(int, kutu.xyxy[0].tolist())
                guven = float(kutu.conf[0])
                cv2.rectangle(kare, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(kare, f"Drone {guven:.2f}", (x1, max(30, y1 - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            goruntu = np.zeros ( (yukseklik, genislik + panel, 3), dtype=np.uint8)
            goruntu[:, :genislik] = kare
            yazi = "Drone" if len(sonuc.boxes) else "Drone yok"
            cv2.putText(goruntu, yazi, (genislik + 20, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            kayit.write(goruntu)
            ekran = cv2.resize(goruntu, (1110, int(yukseklik * 1110 / (genislik + panel))))
            cv2.imshow("Drone tespiti - cikis: Q", ekran)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        video.release()
        kayit.release()
        cv2.destroyAllWindows()
    print(f"Sonuc kaydedildi: {CIKTI}")


if __name__ == "__main__":
    main()
