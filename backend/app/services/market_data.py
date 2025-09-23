"""Static market data helpers for Phase 1 development."""
from __future__ import annotations

import asyncio
import copy
import random
from typing import Any, AsyncIterator, Iterable, Sequence


_BASE_FIELDS = (
    "symbol",
    "name",
    "price",
    "percent_change_24h",
    "percent_change_7d",
    "volume_24h",
    "market_cap",
    "sparkline",
)
_DETAIL_FIELDS = _BASE_FIELDS + ("high_24h", "low_24h", "description")
_MOVE_FIELDS = (
    "symbol",
    "name",
    "price",
    "percent_change_24h",
    "volume_24h",
)

_MARKET_DATA: dict[str, dict[str, Any]] = {
    "BTC": {
        "symbol": "BTC",
        "name": "Bitcoin",
        "price": 65842.28,
        "percent_change_24h": 1.84,
        "percent_change_7d": 5.12,
        "volume_24h": 32800000000,
        "market_cap": 1295000000000,
        "sparkline": [
            64120.23,
            64350.44,
            64410.88,
            64620.01,
            64950.72,
            65320.04,
            65210.98,
            65400.22,
            65680.11,
            65510.33,
            65780.42,
            65842.28,
        ],
        "high_24h": 66010.56,
        "low_24h": 64220.14,
        "description": (
            "Bitcoin is the original decentralized digital currency powering the "
            "crypto ecosystem."
        ),
    },
    "ETH": {
        "symbol": "ETH",
        "name": "Ethereum",
        "price": 3432.87,
        "percent_change_24h": 2.41,
        "percent_change_7d": 4.67,
        "volume_24h": 17200000000,
        "market_cap": 412000000000,
        "sparkline": [
            3285.12,
            3304.18,
            3318.44,
            3340.56,
            3365.22,
            3398.0,
            3387.76,
            3404.91,
            3426.33,
            3412.58,
            3428.21,
            3432.87,
        ],
        "high_24h": 3448.32,
        "low_24h": 3278.45,
        "description": (
            "Ethereum enables programmable smart contracts and powers a wide range "
            "of decentralized applications."
        ),
    },
    "SOL": {
        "symbol": "SOL",
        "name": "Solana",
        "price": 152.35,
        "percent_change_24h": 3.58,
        "percent_change_7d": 8.91,
        "volume_24h": 2650000000,
        "market_cap": 68000000000,
        "sparkline": [
            141.22,
            142.85,
            144.31,
            146.42,
            148.94,
            150.88,
            149.72,
            151.03,
            152.91,
            151.64,
            152.17,
            152.35,
        ],
        "high_24h": 153.18,
        "low_24h": 140.55,
        "description": (
            "Solana is a high-performance blockchain focused on throughput for "
            "DeFi, NFTs, and web3 applications."
        ),
    },
    "XRP": {
        "symbol": "XRP",
        "name": "XRP",
        "price": 0.57,
        "percent_change_24h": -1.27,
        "percent_change_7d": 0.84,
        "volume_24h": 940000000,
        "market_cap": 30500000000,
        "sparkline": [
            0.59,
            0.588,
            0.584,
            0.579,
            0.575,
            0.571,
            0.569,
            0.568,
            0.567,
            0.566,
            0.568,
            0.57,
        ],
        "high_24h": 0.61,
        "low_24h": 0.55,
        "description": (
            "XRP powers the Ripple network for fast, low-cost cross-border "
            "payments and settlements."
        ),
    },
    "DOGE": {
        "symbol": "DOGE",
        "name": "Dogecoin",
        "price": 0.15,
        "percent_change_24h": -0.82,
        "percent_change_7d": 2.91,
        "volume_24h": 820000000,
        "market_cap": 21000000000,
        "sparkline": [
            0.152,
            0.154,
            0.153,
            0.151,
            0.149,
            0.148,
            0.147,
            0.148,
            0.149,
            0.148,
            0.149,
            0.15,
        ],
        "high_24h": 0.158,
        "low_24h": 0.145,
        "description": (
            "Dogecoin began as a meme but now supports tipping, payments, and "
            "community-driven experiments."
        ),
    },
    "ADA": {
        "symbol": "ADA",
        "name": "Cardano",
        "price": 0.52,
        "percent_change_24h": 0.74,
        "percent_change_7d": -1.45,
        "volume_24h": 540000000,
        "market_cap": 18200000000,
        "sparkline": [
            0.508,
            0.509,
            0.511,
            0.514,
            0.518,
            0.521,
            0.519,
            0.517,
            0.515,
            0.516,
            0.519,
            0.52,
        ],
        "high_24h": 0.53,
        "low_24h": 0.5,
        "description": (
            "Cardano is a proof-of-stake blockchain built on peer-reviewed "
            "research for secure smart contracts."
        ),
    },
    "AVAX": {
        "symbol": "AVAX",
        "name": "Avalanche",
        "price": 38.44,
        "percent_change_24h": 4.12,
        "percent_change_7d": 6.73,
        "volume_24h": 410000000,
        "market_cap": 14300000000,
        "sparkline": [
            34.25,
            34.78,
            35.64,
            36.82,
            37.45,
            37.98,
            37.61,
            38.02,
            38.28,
            38.36,
            38.41,
            38.44,
        ],
        "high_24h": 38.62,
        "low_24h": 34.02,
        "description": (
            "Avalanche offers a scalable network of blockchains optimized for "
            "high-throughput DeFi applications."
        ),
    },
    "MATIC": {
        "symbol": "MATIC",
        "name": "Polygon",
        "price": 0.88,
        "percent_change_24h": -2.35,
        "percent_change_7d": -0.92,
        "volume_24h": 610000000,
        "market_cap": 8200000000,
        "sparkline": [
            0.93,
            0.924,
            0.918,
            0.912,
            0.905,
            0.899,
            0.896,
            0.893,
            0.891,
            0.889,
            0.887,
            0.88,
        ],
        "high_24h": 0.94,
        "low_24h": 0.87,
        "description": (
            "Polygon provides Ethereum-compatible scaling solutions for "
            "cost-effective dApp deployments."
        ),
    },
}

_ORDERED_SYMBOLS = sorted(
    _MARKET_DATA.keys(), key=lambda symbol: _MARKET_DATA[symbol]["market_cap"], reverse=True
)


def _filter_fields(asset: dict[str, Any], fields: Iterable[str]) -> dict[str, Any]:
    return {field: copy.deepcopy(asset[field]) for field in fields}


def list_symbols() -> list[str]:
    """Return the list of supported market symbols."""

    return list(_MARKET_DATA.keys())


def get_overview(limit: int | None = None) -> list[dict[str, Any]]:
    """Return a market overview sorted by market cap."""

    symbols = _ORDERED_SYMBOLS
    if limit is not None:
        symbols = symbols[: max(limit, 0)]
    return [_filter_fields(_MARKET_DATA[symbol], _BASE_FIELDS) for symbol in symbols]


def get_top_movers(limit: int = 4) -> dict[str, list[dict[str, Any]]]:
    """Return top gainers and losers by 24h change."""

    limit = max(1, limit)
    sorted_by_change = sorted(
        _MARKET_DATA.values(), key=lambda asset: asset["percent_change_24h"], reverse=True
    )
    gainers = [_filter_fields(asset, _MOVE_FIELDS) for asset in sorted_by_change[:limit]]
    losers = [
        _filter_fields(asset, _MOVE_FIELDS)
        for asset in sorted(_MARKET_DATA.values(), key=lambda asset: asset["percent_change_24h"])[
            :limit
        ]
    ]
    return {"gainers": gainers, "losers": losers}


def get_asset_detail(symbol: str) -> dict[str, Any] | None:
    """Return full detail for a symbol if available."""

    asset = _MARKET_DATA.get(symbol.upper())
    if not asset:
        return None
    return _filter_fields(asset, _DETAIL_FIELDS)


def get_watchlist_snapshots(symbols: Sequence[str]) -> list[dict[str, Any]]:
    """Return overview entries for the requested symbols preserving order."""

    seen: set[str] = set()
    snapshots: list[dict[str, Any]] = []
    for symbol in symbols:
        normalized = symbol.upper()
        if normalized in seen:
            continue
        asset = _MARKET_DATA.get(normalized)
        if asset:
            snapshots.append(_filter_fields(asset, _BASE_FIELDS))
            seen.add(normalized)
    return snapshots


def available_symbol(symbol: str) -> bool:
    """Return True if the dataset includes the symbol."""

    return symbol.upper() in _MARKET_DATA


def normalize_symbol(symbol: str) -> str:
    """Uppercase helper for consistent responses."""

    return symbol.upper()


async def stream_quotes(
    symbols: Sequence[str], *, iterations: int = 5, delay: float = 0.15
) -> AsyncIterator[dict[str, Any]]:
    """Yield pseudo-random price updates for a list of symbols."""

    normalized: list[str] = []
    for symbol in symbols:
        upper = symbol.upper()
        if upper in _MARKET_DATA and upper not in normalized:
            normalized.append(upper)

    if not normalized:
        return

    iterations = max(1, iterations)
    seed = sum(ord(ch) for symbol in normalized for ch in symbol)
    rng = random.Random(seed)

    base_prices = {symbol: _MARKET_DATA[symbol]["price"] for symbol in normalized}
    base_changes = {symbol: _MARKET_DATA[symbol]["percent_change_24h"] for symbol in normalized}

    for _ in range(iterations):
        updates: list[dict[str, Any]] = []
        for symbol in normalized:
            drift = rng.uniform(-0.35, 0.35)
            price = round(base_prices[symbol] * (1 + drift / 100), 2)
            percent_change = round(base_changes[symbol] + drift, 2)
            base_prices[symbol] = price
            base_changes[symbol] = percent_change
            updates.append(
                {
                    "symbol": symbol,
                    "price": price,
                    "percent_change_24h": percent_change,
                }
            )
        yield {"type": "watchlist_snapshot", "quotes": updates}
        await asyncio.sleep(delay)
