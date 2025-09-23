#!/usr/bin/env bash
set -euo pipefail

# Ortam değişkenleri (.env'den okunabilir)
BROKER=${KAFKA_BROKERS:-localhost:9092}
TOPIC=${KAFKA_TOPIC:-prices.ticks}
PARTITIONS=${PARTITIONS:-6}
REPLICATION=${REPLICATION:-1}

echo "Creating topic: $TOPIC (partitions=$PARTITIONS, rf=$REPLICATION) on $BROKER"

# Kafka container'ını bul (bitnami/kafka imajını esas alıyoruz)
CID=$(docker ps --filter "ancestor=bitnami/kafka:3.7" -q | head -n 1)
if [ -z "$CID" ]; then
  echo "Kafka container bulunamadı. docker ps ile kontrol edin."
  exit 1
fi

docker exec -i "$CID" kafka-topics.sh \
  --create \
  --if-not-exists \
  --topic "$TOPIC" \
  --bootstrap-server kafka:9092 \
  --partitions "$PARTITIONS" \
  --replication-factor "$REPLICATION"

echo "Done."
