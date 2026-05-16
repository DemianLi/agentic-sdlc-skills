"""E2E tests: main user flows through the API."""
import pytest
from httpx import ASGITransport, AsyncClient

from src.api import app


@pytest.fixture
def anyio_backend():
    """Set asyncio as the anyio backend."""
    return "asyncio"


@pytest.mark.asyncio
async def test_flow1_analyze_standard_text():
    """Flow 1: User analyzes a standard paragraph — all metrics > 0."""
    text = "The quick brown fox jumps over the lazy dog. It was a bright day."
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.get("/analyze", params={"text": text})
        assert resp.status_code == 200
        data = resp.json()
        assert data["word_count"] > 0
        assert data["char_count"] > 0
        assert data["sentence_count"] > 0
        assert data["paragraph_count"] > 0


@pytest.mark.asyncio
async def test_flow2_analyze_empty_text():
    """Flow 2: User sends empty text — all metrics return 0 without error."""
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


@pytest.mark.asyncio
async def test_flow3_analyze_multi_paragraph():
    """Flow 3: User sends multi-paragraph text — paragraph_count >= 2."""
    text = "First paragraph here.\n\nSecond paragraph here.\n\nThird paragraph."
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.get("/analyze", params={"text": text})
        assert resp.status_code == 200
        assert resp.json()["paragraph_count"] >= 2


@pytest.mark.asyncio
async def test_flow4_analyze_text_without_sentence_endings():
    """Flow 4: User sends text with no punctuation — sentence_count = 0."""
    text = "This text has no sentence ending punctuation marks"
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.get("/analyze", params={"text": text})
        assert resp.status_code == 200
        assert resp.json()["sentence_count"] == 0


@pytest.mark.asyncio
async def test_flow_s1_long_text():
    """Flow S1: Very long text (10,000 chars) — returns 200 OK."""
    text = "word " * 2000  # ~10,000 chars
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.get("/analyze", params={"text": text})
        assert resp.status_code == 200
        assert resp.json()["word_count"] == 2000


@pytest.mark.asyncio
async def test_flow_s2_whitespace_only():
    """Flow S2: Whitespace-only text — word_count=0, char_count=0."""
    text = "   \n\n   \t   "
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.get("/analyze", params={"text": text})
        assert resp.status_code == 200
        data = resp.json()
        assert data["word_count"] == 0
        assert data["char_count"] == 0
