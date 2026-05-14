"""Gemini text generation via LangChain (ChatGoogleGenerativeAI)."""
from __future__ import annotations

import os
from typing import Optional

from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

DEFAULT_MODEL = "gemini-2.5-flash"


def gemini_generate_text(prompt: str, *, api_key: Optional[str] = None, model: str = DEFAULT_MODEL) -> Optional[str]:
    """
    Returns stripped plain text from Gemini, or None if the key is missing,
    the prompt is empty, or the model returns no usable text.
    """
    key = api_key if api_key is not None else os.getenv("GEMINI_API_KEY")
    if not key or not (prompt or "").strip():
        return None
    llm = ChatGoogleGenerativeAI(model=model, google_api_key=key)
    message = llm.invoke([HumanMessage(content=prompt)])
    raw = message.content
    if raw is None:
        return None
    if isinstance(raw, list):
        text = "".join(
            part if isinstance(part, str) else (part.get("text", "") if isinstance(part, dict) else str(part))
            for part in raw
        )
    else:
        text = str(raw)
    text = text.strip()
    return text or None
