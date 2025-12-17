---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.18.1
  kernelspec:
    display_name: CSPLab pipelines_opik
    language: python
    name: csplab-pipelines_opik
---

## Imports

```python
import json
import os
import time
from typing import Any, Dict

import opik
import requests
from dotenv import load_dotenv
from opik import track
from opik.opik_context import update_current_trace
```

## Config

```python
load_dotenv()

# --- AlbertAPI OCR ---
ALBERT_API_BASE_URL = "https://albert.api.etalab.gouv.fr"
ALBERT_API_KEY = os.getenv("ALBERT_API_KEY")
ALBERT_OCR_MODEL = "albert-large"

# --- Opik Configuration ---
os.environ["OPIK_PROJECT_NAME"] = "OCR-ALBERT-LLM-GPT5"
opik.configure(
    api_key="clqmymaMEq37utj1CxN87S1Hf",                # A renseigner
    workspace="ouladhima",
    use_local=False
)
```

## Prompts

```python
# --- Prompt ---
PROMPT_ALBERT_TEXT = """Tu es un assistant qui extrait les expériences professionnelles et les compétences d'un CV.

Consignes importantes :

Le CV est en français.
Tu DOIS répondre STRICTEMENT en JSON valide, sans texte autour.
Le format de sortie doit être exactement :
{ "experiences": [ { "title": "string", "company": "string", "sector": "string|null", "description": "string" } ], "skills": ["string"] }

Règles supplémentaires :

"experiences" : une entrée par expérience significative.
"sector" peut être null si l'information n'est pas claire.
"skills" : liste de compétences (techniques, outils, soft skills) au format string.
N'invente pas d'informations si elles ne sont pas dans le CV."""

PROMPT_ALBERT = opik.Prompt(
    name="albert_cv_extraction_v1",
    prompt=PROMPT_ALBERT_TEXT,
    metadata={"pipeline": "A", "use": "ocr_structured_extraction"}
)
```

## Utils

```python
@track(name="tool_albert_ocr")
def call_albert_ocr(
    pdf_bytes: bytes,
    prompt: str | None = None,
    dpi: int = 200,
    return_json: bool = False,
) -> Any:
    """Call Albert OCR API."""
    url = f"{ALBERT_API_BASE_URL}/v1/ocr-beta"
    headers = {"Authorization": f"Bearer {ALBERT_API_KEY}"}
    files = {"file": ("document.pdf", pdf_bytes, "application/pdf")}
    data = {"model": ALBERT_OCR_MODEL, "dpi": str(dpi)}
    if prompt:
        data["prompt"] = prompt

    resp = requests.post(url, headers=headers, files=files, data=data, timeout=120)
    resp.raise_for_status()
    data = resp.json()

    if return_json:
        return data

    text = data.get("content")
    if isinstance(text, str):
        return text
    if isinstance(text, list):
        parts = []
        for item in text:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                val = item.get("text")
                if isinstance(val, str):
                    parts.append(val)
        return "\n".join(parts)
    return str(data)


def extract_json_from_fenced_content(text: str) -> dict:
    """Extract JSON from Markdown code block."""
    text = text.strip()
    if text.startswith("```"):
        first_newline = text.find("\n")
        if first_newline != -1:
            text = text[first_newline + 1:]
        fence_pos = text.rfind("```")
        if fence_pos != -1:
            text = text[:fence_pos]
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {}


def normalize_albert_ocr_structured(ocr_data: Any) -> dict:
    """Normalize Albert OCR JSON output.
    Handles multi-page CVs where Albert returns a list of pages with JSON fragments.
    """
    final_experiences = []
    final_skills = []

    # Case 1: Already the final dict
    if isinstance(ocr_data, dict):
        if "experiences" in ocr_data and "skills" in ocr_data:
            return ocr_data

        # Case 2: Multi-page structure
        if "data" in ocr_data and isinstance(ocr_data["data"], list):
            found_any = False
            for page in ocr_data["data"]:
                if isinstance(page, dict):
                    content = page.get("content")
                    if isinstance(content, str):
                        parsed_page = extract_json_from_fenced_content(content)
                        if parsed_page:
                            exps = parsed_page.get("experiences", [])
                            sks = parsed_page.get("skills", [])
                            if isinstance(exps, list):
                                final_experiences.extend(exps)
                            if isinstance(sks, list):
                                final_skills.extend(sks)
                            found_any = True

            if found_any:
                unique_skills = list(set(final_skills)) if final_skills else []
                return {"experiences": final_experiences, "skills": unique_skills}

        # Case 3: JSON in "text" field
        text = ocr_data.get("text")
        if isinstance(text, str):
            parsed = extract_json_from_fenced_content(text)
            if isinstance(parsed, dict) and ("experiences" in parsed or "skills" in parsed):
                return parsed

    # Case 4: Raw string
    if isinstance(ocr_data, str):
        parsed = extract_json_from_fenced_content(ocr_data)
        if isinstance(parsed, dict) and ("experiences" in parsed or "skills" in parsed):
            return parsed

    # Fallback
    return {"experiences": [], "skills": []}
```

## Pipeline

```python
@track(name="pipeline_A_ocr_only")
def pipeline_a_ocr_only(pdf_path: str) -> Dict[str, Any]:
    """Pipeline A: OCR-only extraction using Albert API."""
    start = time.perf_counter()
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    ocr_structured_raw = call_albert_ocr(
        pdf_bytes, prompt=PROMPT_ALBERT.prompt, dpi=200, return_json=True
    )
    structured = normalize_albert_ocr_structured(ocr_structured_raw)
    latency = time.perf_counter() - start

    n_exp = len(structured.get("experiences", []) or [])
    n_sk = len(structured.get("skills", []) or [])

    update_current_trace(
        feedback_scores=[
            {"name": "n_experiences", "value": float(n_exp)},
            {"name": "n_skills", "value": float(n_sk)}
        ],
        metadata={
            "file": os.path.basename(pdf_path),
            "ocr_model_id": ALBERT_OCR_MODEL,
            "llm_model_id": None,
            "use_anonymization": False
        },
        prompts=[PROMPT_ALBERT],
    )

    return {
        "pipeline": "A_OCR_ONLY",
        "file": os.path.basename(pdf_path),
        "latency_sec": latency,
        "output": structured,
        "debug": {
            "raw_ocr_response": str(ocr_structured_raw)
        }
    }
```

```python

```
