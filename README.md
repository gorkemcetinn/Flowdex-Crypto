# Flowdex: Crypto

**Flowdex: Crypto**, kripto yatırımcıları için gerçek zamanlı fiyat akışı, favori coin takibi, uyarı sistemi ve analiz özellikleri sunan bir dashboard uygulamasıdır.  
Hem **data engineering** becerilerini geliştirmek isteyenler hem de kripto piyasalarını yakından takip etmek isteyenler için tasarlanmıştır.

---

## ✨ Özellikler

- 📈 **Favori Coin Takibi (Watchlist)**
  - Kullanıcılar seçtikleri coinleri canlı olarak izleyebilir.
  - Sparkline grafikler ve 24 saatlik değişim oranları.

- 🚨 **Uyarılar**
  - Kullanıcı tanımlı kurallar (ör. %2 fiyat artışı 5 dakikada).
  - Anında Telegram/E-mail bildirimi.

- 🏆 **Top Movers**
  - En çok yükselen/düşen coin listeleri (1h / 24h).

- 📊 **Grafikler**
  - 1m / 5m / 15m OHLCV candlestick ve hacim grafikleri.

- 📰 **(V2) Haber Paneli**
  - Haber API’lerinden gelen veriler coin bazlı filtrelenir.
  - Basit duygu analizi ile pozitif/negatif etiketleme.

- 🤖 **(V2) Chatbot**
  - “BTC son 24 saatte ne yaptı?” gibi doğal dil sorularına yanıt.
  - SQL query generation + metrik özetleri.

---

## 🔮 Potansiyel

Flowdex sadece bir fiyat izleme aracı değil:  
- **Data engineering pratiği**: Kafka, Spark, Airflow gibi endüstri standardı araçlarla gerçek zamanlı + batch pipeline.  
- **LLM entegrasyonu**: Doğal dil ile veri ambarından sorgulama ve otomatik raporlama.  
- **Ölçeklenebilir mimari**: İleride hisse senetleri, IoT sensörleri veya farklı veri kaynakları kolayca eklenebilir.  

---

## 🏗️ Mimari

### Akış
1. **Exchange WS** → `ws-collector` → **Kafka (`prices.ticks`)**
2. **Spark Structured Streaming** → OHLCV + metrikler → **PostgreSQL**
3. **Airflow** → batch işler (top movers, backfill, DQ) → **PostgreSQL**
4. **Backend (FastAPI)** → REST/SSE API → **Frontend (Next.js Dashboard)**
5. **Alerts** → Spark trigger / Backend → **Notifier (Telegram/E-mail)**

### Bileşenler
- **Frontend**: Next.js/React  
- **Backend**: FastAPI (REST + SSE/WS)  
- **Data Pipeline**:  
  - Ingestion: Kafka  
  - Processing: Spark Structured Streaming  
  - Orchestration: Airflow  
- **Veritabanı**: PostgreSQL (users, watchlist, alerts, prices_ohlcv, movers, metrics)  

---

## 📂 Klasör Yapısı (öneri)

flowdex-crypto/
│── apps/
│ ├── api/ # FastAPI backend
│ ├── web/ # Next.js frontend
│ └── alert-worker/ # Telegram/Email notifier
│
│── jobs/
│ ├── stream_ohlcv.py # Spark streaming job
│ └── batch_movers.py # Airflow batch job
│
│── airflow/
│ └── dags/ # DAG tanımları
│
│── infra/
│ └── docker-compose.yml
│
│── docs/
│ └── architecture.png # Mimari şema
│
└── README.md


---

## 🚀 Kurulum (Development)

1. Repo’yu klonla:  
   ```bash
   git clone https://github.com/kullanici/flowdex-crypto.git
   cd flowdex-crypto


2. Docker Compose ile servisleri ayağa kaldır:
    ```bash
    docker-compose up -d


3. Servislere erişim:
- Frontend → http://localhost:3000

- Backend API → http://localhost:8000

- Airflow UI → http://localhost:8080


##  🛠️ Tech Stack

Frontend: Next.js, React, Tailwind, Chart.js/Recharts

Backend: FastAPI, SSE/WS

Streaming: Kafka, Spark Structured Streaming

Batch / Orchestration: Airflow

Database: PostgreSQL

Notifications: Telegram Bot API, SMTP (Email)

(V2): LangChain + LLM API (Chatbot), News API

##    📅 Roadmap

 Favori coin izleme + canlı fiyat kartları

 OHLCV streaming job

 Watchlist & Alerts API

 Top Movers batch job

 Telegram/E-mail notifier

 Sembol detay grafikleri

 Haber API entegrasyonu

 LLM destekli chatbot

## 📜 Lisans

MIT