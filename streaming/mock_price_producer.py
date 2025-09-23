#!/usr/bin/env python
"""Produce synthetic price ticks to Kafka for Phase 2 development."""
from __future__ import annotations

import argparse
import json
import os
import random
import signal
import sys
import time
from datetime import datetime, timezone
from typing import Dict

from kafka import KafkaProducer


DEFAULT_SYMBOLS: Dict[str, dict[str, float]] = {
    "BTC": {"price": 65500.0, "volatility": 0.6},
    "ETH": {"price": 3400.0, "volatility": 0.9},
    "SOL": {"price": 150.0, "volatility": 1.2},
    "AVAX": {"price": 38.0, "volatility": 1.4},
}


def build_producer(brokers: str) -> KafkaProducer:
    return KafkaProducer(
        bootstrap_servers=brokers,
        value_serializer=lambda payload: json.dumps(payload).encode("utf-8"),
    )


def next_tick(symbol: str, state: dict[str, float]) -> dict[str, object]:
    base = state.setdefault(symbol, DEFAULT_SYMBOLS[symbol]["price"])
    volatility = DEFAULT_SYMBOLS[symbol]["volatility"]
    drift = random.gauss(0, volatility)
    price = max(0.01, round(base * (1 + drift / 100), 2))
    state[symbol] = price
    volume = round(abs(random.gauss(2.5, 1.2)), 4)
    return {
        "symbol": symbol,
        "price": price,
        "volume": volume,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": "flowdex-demo",
    }


def run_producer(args: argparse.Namespace) -> None:
    symbols = [symbol.upper() for symbol in args.symbols]
    for symbol in symbols:
        if symbol not in DEFAULT_SYMBOLS:
            raise SystemExit(f"Unsupported symbol '{symbol}'. Choose from {sorted(DEFAULT_SYMBOLS)}")

    producer = build_producer(args.brokers)
    state: dict[str, float] = {}

    running = True

    def handle_signal(signum: int, _frame: object) -> None:  # pragma: no cover - signal handler
        nonlocal running
        running = False
        print(f"Received signal {signum}, flushing producer…", file=sys.stderr)

    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, handle_signal)

    try:
        while running:
            for symbol in symbols:
                event = next_tick(symbol, state)
                producer.send(args.topic, event)
                if args.verbose:
                    print(f"→ {event}")
            producer.flush()
            time.sleep(args.interval)
    finally:
        producer.flush()
        producer.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--brokers",
        default=os.getenv("KAFKA_BROKERS", "localhost:9092"),
        help="Bootstrap brokers for Kafka (default: %(default)s)",
    )
    parser.add_argument(
        "--topic",
        default=os.getenv("KAFKA_TOPIC", "prices.ticks"),
        help="Kafka topic for tick events",
    )
    parser.add_argument(
        "--symbols",
        nargs="+",
        default=list(DEFAULT_SYMBOLS.keys()),
        help="Symbols to simulate (default: %(default)s)",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=float(os.getenv("PRODUCER_INTERVAL", 1.0)),
        help="Seconds between batches (default: %(default)s)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print payloads as they are produced",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_producer(args)


if __name__ == "__main__":  # pragma: no cover - script entrypoint
    main()
