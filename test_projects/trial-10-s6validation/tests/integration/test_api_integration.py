"""Integration tests: API endpoint ↔ string_stats core boundary."""
import asyncio

import pytest
from httpx import ASGITransport, AsyncClient

from src.api import app


@pytest.fixture
def anyio_backend():
    """Set asyncio as the anyio backend."""
    return "asyncio"


@pytest.mark.asyncio
async def test_analyze_returns_all_metrics():
    """API returns all 4 metrics for valid text."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.get("/analyze", params={"text": "Hello world. Goodbye."})
        assert resp.status_code == 200
        data = resp.json()
        assert "word_count" in data
        assert "char_count" in data
        assert "sentence_count" in data
        assert "paragraph_count" in data


@pytest.mark.asyncio
async def test_api_word_count_matches_core():
    """AC-1.4: API word_count equals direct function call."""
    text = "the quick brown fox"
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.get("/analyze", params={"text": text})
        assert resp.status_code == 200
        assert resp.json()["word_count"] == 4


@pytest.mark.asyncio
async def test_api_char_count_matches_core():
    """API char_count equals direct function call."""
    text = "hello world"
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.get("/analyze", params={"text": text})
        assert resp.status_code == 200
        assert resp.json()["char_count"] == 10


@pytest.mark.asyncio
async def test_api_sentence_count_matches_core():
    """API sentence_count equals direct function call."""
    text = "Hello. World!"
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.get("/analyze", params={"text": text})
        assert resp.status_code == 200
        assert resp.json()["sentence_count"] == 2


@pytest.mark.asyncio
async def test_api_paragraph_count_matches_core():
    """API paragraph_count equals direct function call."""
    text = "para one\n\npara two\n\npara three"
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.get("/analyze", params={"text": text})
        assert resp.status_code == 200
        assert resp.json()["paragraph_count"] == 3


@pytest.mark.asyncio
async def test_api_empty_text_returns_zeros():
    """Integration: empty text returns all zeros."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.get("/analyze", params={"text": ""})
        assert resp.status_code == 200
        data = resp.json()
        assert data["word_count"] == 0
        assert data["char_count"] == 0
        assert data["sentence_count"] == 0
        assert data["paragraph_count"] == 0
