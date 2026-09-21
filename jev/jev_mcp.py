#!/usr/bin/env python3
"""Minimal MCP server exposing TypeSafe's Jev (System One) model as typed-judgment
tools for Claude Code. Three tools map to Jev's three primitives:

  jev_classify  -> Choice : pick one of N labeled options (+ probabilities, confidence)
  jev_check     -> Noul   : probability a yes/no condition holds (0..1)
  jev_score     -> Score  : graded position along ordered levels (+ confidence)

Auth: reads TYPESAFE_API_KEY from the environment. The key is never stored here.
Deps: the official `mcp` SDK only; the HTTP call uses the stdlib (urllib).
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from mcp.server.fastmcp import FastMCP

API_URL = "https://api.typesafe.ai/v1/systemone"
MODEL = os.environ.get("TYPESAFE_MODEL", "jev-latest")
RETRY_STATUS = {429, 500, 502, 503, 504}  # transient; TypeSafe returns intermittent 503s
MAX_ATTEMPTS = 4

mcp = FastMCP("jev")


def _ask(state: str, question: dict) -> dict:
    """POST one question to Jev and return its answer object.

    Retries transient errors (429/5xx) with exponential backoff so a passing
    TypeSafe blip does not surface as a failed tool call.
    """
    key = os.environ.get("TYPESAFE_API_KEY")
    if not key:
        raise RuntimeError("TYPESAFE_API_KEY is not set")
    body = json.dumps({"model": MODEL, "state": state, "questions": {"q": question}}).encode()
    req = urllib.request.Request(
        API_URL,
        data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.load(resp)["answers"]["q"]
        except urllib.error.HTTPError as err:
            if err.code not in RETRY_STATUS or attempt == MAX_ATTEMPTS:
                raise
        except urllib.error.URLError:
            if attempt == MAX_ATTEMPTS:
                raise
        time.sleep(0.5 * 2 ** (attempt - 1))  # 0.5s, 1s, 2s
    raise RuntimeError("unreachable")


@mcp.tool()
def jev_classify(state: str, options: dict[str, str], instructions: str) -> dict:
    """Pick exactly one option for `state` using Jev (fast, calibrated).

    Use for routing/classification when the answer is one of a fixed set:
    which team handles a ticket, the sentiment bucket of a headline, the
    category of an item. `options` maps each label to a short description of
    when it applies. Returns {choice, probabilities, confidence}. Prefer this
    over reasoning it yourself when the task is high-volume or needs a
    confidence number to gate on.
    """
    return _ask(state, {"type": "choice", "instructions": instructions, "criteria": options})


@mcp.tool()
def jev_check(state: str, condition: str) -> dict:
    """Return the probability (0..1) that a yes/no `condition` holds for `state`.

    Use for verification/gating: "does this text request a human?", "is this
    claim supported by the evidence?". Returns {noul: <prob>} where the number
    is both the answer and the certainty (near 0.5 = genuinely unsure).
    """
    return _ask(state, {"type": "noul", "instructions": condition})


@mcp.tool()
def jev_score(state: str, dimension: str, levels: list[str]) -> dict:
    """Rate `state` along an ordered scale using Jev.

    `dimension` describes what is being rated; `levels` are ordered level
    descriptions from lowest to highest (each must stand on its own).
    Use for graded judgments (severity, urgency, relevance strength).
    Returns {score, legend, probabilities, confidence}.
    """
    return _ask(state, {"type": "score", "instructions": dimension, "criteria": levels})


if __name__ == "__main__":
    mcp.run()
