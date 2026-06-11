# 🐹 hamster-game-api

Python event-driven API for Hamster Game — Task 1 & 2.

## Proje Yapısı

```
hamster-game-api/
├── app/
│   ├── main.py        # FastAPI — webhook alır, DB'ye kaydeder
│   └── database.py    # Neon bağlantısı + tablo oluşturma
├── worker/
│   ├── worker.py      # Pending olayları okuyup işler (event loop)
│   ├── dispatcher.py  # event_type → handler yönlendirmesi
│   └── handlers.py    # Her olay tipi için ayrı fonksiyon
├── requirements.txt
└── .env               # DATABASE_URL buraya
```

## Kurulum

```bash
pip install -r requirements.txt
cp .env.example .env
# .env dosyasına Neon connection string'ini ekle
```

## Çalıştırma

**Task 1 — API'yi başlat:**
```bash
uvicorn app.main:app --reload
```

**Task 2 — Worker'ı başlat (ayrı terminalde):**
```bash
python -m worker.worker
```

## Event Gönderme (test)

```bash
curl -X POST http://localhost:8000/events \
  -H "Content-Type: application/json" \
  -d '{"event_type": "tap", "user_id": "user_123", "payload": {"tap_power": 5}}'
```

## Desteklenen Event Tipleri

| event_type     | Açıklama                     |
|----------------|------------------------------|
| `tap`          | Kullanıcı hamsteri tıkladı   |
| `boost_used`   | Boost aktivasyonu            |
| `level_up`     | Yeni seviye                  |
| `score_update` | Skor güncelleme              |

Yeni event tipi eklemek için sadece `worker/handlers.py`'a fonksiyon,
`worker/dispatcher.py`'daki `HANDLER_REGISTRY`'e bir satır ekle.

## n8n ile Karşılaştırma

| n8n                  | Bu Proje                        |
|----------------------|---------------------------------|
| Webhook node         | `POST /events` endpoint         |
| Switch/Router node   | `dispatcher.py`                 |
| Her işlem node'u     | `handlers.py` içindeki fonksiyon |
| Execution log        | `events` tablosundaki `status`  |
