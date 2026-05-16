"""FastAPI application for string statistics."""
from fastapi import FastAPI
from src.string_stats import char_count, paragraph_count, sentence_count, word_count

app = FastAPI(title="String Stats API")


@app.get("/analyze")
async def analyze(text: str = ""):
    """Analyze text and return statistics."""
    return {
        "word_count": word_count(text),
        "char_count": char_count(text),
        "sentence_count": sentence_count(text),
        "paragraph_count": paragraph_count(text),
    }
