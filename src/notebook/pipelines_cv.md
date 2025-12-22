"""Benchmark Extraction CV (OCR + LLM + Anonymisation)

Ce script permet d'extraire des données structurées (Expériences et Compétences) à partir d'un dossier de CVs au format PDF. Il compare trois approches (pipelines) différentes et envoie les traces d'exécution vers Opik pour analyse.

Fonctionnalités:

Le script exécute 3 pipelines pour chaque fichier PDF :

-- Pipeline A (OCR Only) : Utilise l'API Albert (Gouv) pour faire l'OCR et l'extraction structurée en une seule étape.
-- Pipeline B (PDF2Text + LLM) : Extrait le texte via pdfplumber (sans OCR), anonymise les données sensibles via Presidio, puis utilise un LLM via OpenRouter pour structurer.
-- Pipeline C (OCR + LLM) : Utilise Albert pour l'OCR brut, anonymise le texte, puis utilise OpenRouter pour structurer.

usage :
python pipelines_cv.py ./dossier_cvs
"""

import json
import os
import time
from typing import Any, Dict, List

import opik
import pdfplumber
import requests
from dotenv import load_dotenv
from opik import track
from opik.opik_context import update_current_trace
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

# =============================
#  CONFIG
# =============================

load_dotenv()

# --- AlbertAPI OCR ---
ALBERT_API_BASE_URL = "https://albert.api.etalab.gouv.fr"
ALBERT_API_KEY = os.getenv("ALBERT_API_KEY")
ALBERT_OCR_MODEL = "albert-large"

# --- OpenRouter LLM ---
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = "openai/gpt-5"

# --- Anonymisation (Presidio) ---
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()
DEFAULT_PRESIDIO_LANG = "en"

# --- Paramètres Pipelines ---
ENABLE_ANONYMIZATION = True

# =============================
#  OPIK INIT
# =============================
os.environ["OPIK_PROJECT_NAME"] = "OCR-ALBERT-LLM-GPT5"
opik.configure(
    api_key="",                # A renseigner
    workspace="ouladhima",      # None = va chercher dans ENV
    use_local=False      # indispensable pour envoyer vers Comet
)


# =============================
#  PROMPTS OPIK
# =============================

PROMPT_ALBERT_TEXT = """
Tu es un assistant qui extrait les expériences professionnelles et les compétences d'un CV.

Consignes importantes :
- Le CV est en français.
- Tu DOIS répondre STRICTEMENT en JSON valide, sans texte autour.
- Le format de sortie doit être exactement :

{
  "experiences": [
    {
      "title": "string",
      "company": "string",
      "sector": "string|null",
      "description": "string"
    }
  ],
  "skills": ["string"]
}

Règles supplémentaires :
- "experiences" : une entrée par expérience significative.
- "sector" peut être null si l'information n'est pas claire.
- "skills" : liste de compétences (techniques, outils, soft skills) au format string.
- N'invente pas d'informations si elles ne sont pas dans le CV.
"""

PROMPT_ALBERT = opik.Prompt(
    name="albert_cv_extraction_v1",
    prompt=PROMPT_ALBERT_TEXT,
    metadata={"pipeline": "A", "use": "ocr_structured_extraction"}
)

PROMPT_LLM_TEXT = """
Tu es un assistant qui extrait les expériences professionnelles et les compétences d'un CV.

Consignes importantes :
- Le CV est en français.
- Tu DOIS répondre STRICTEMENT en JSON valide, sans texte autour.
- Le format de sortie doit être exactement :

{
  "experiences": [
    {
      "title": "string",
      "company": "string",

      "sector": "string|null",
      "description": "string"
    }
  ],
  "skills": ["string"]
}

Règles supplémentaires :
- "experiences" : une entrée par expérience significative.
- "sector" peut être null si l'information n'est pas claire.
- "skills" : liste de compétences (techniques, outils, soft skills) au format string.
- N'invente pas d'informations si elles ne sont pas dans le CV.

Voici le contenu du CV (texte brut) :

\"\"\"{{cv_text}}\"\"\"
"""

PROMPT_LLM = opik.Prompt(
    name="llm_cv_extraction_v1",
    prompt=PROMPT_LLM_TEXT,
    metadata={"pipeline": "B/C", "use": "llm_structured_extraction"}
)

# =============================
#  HELPERS
# =============================

def anonymize_text(text: str) -> str:
    """Anonymise le texte avec Presidio."""
    results = analyzer.analyze(text=text, language=DEFAULT_PRESIDIO_LANG)
    anonymized = anonymizer.anonymize(
        text=text,
        analyzer_results=results
    ).text
    return anonymized


def pdf_to_text(pdf_path: str) -> str:
    """Extraction texte 'native' depuis un PDF (sans OCR)."""
    parts: List[str] = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            parts.append(page.extract_text() or "")
    return "\n".join(parts)

@track(name="tool_albert_ocr")
def call_albert_ocr(
    pdf_bytes: bytes,
    prompt: str | None = None,
    dpi: int = 200,
    return_json: bool = False,
) -> Any:
    url = f"{ALBERT_API_BASE_URL}/v1/ocr-beta"
    headers = {"Authorization": f"Bearer {ALBERT_API_KEY}"}
    files = {"file": ("document.pdf", pdf_bytes, "application/pdf")}
    data = {"model": ALBERT_OCR_MODEL, "dpi": str(dpi)}
    if prompt:
        data["prompt"] = prompt

    resp = requests.post(url, headers=headers, files=files, data=data, timeout=120)
    resp.raise_for_status()
    data = resp.json()

    if return_json: return data

    text = data.get("content")
    if isinstance(text, str): return text
    if isinstance(text, list):
        parts = []
        for item in text:
            if isinstance(item, str): parts.append(item)
            elif isinstance(item, dict):
                val = item.get("text")
                if isinstance(val, str): parts.append(val)
        return "\n".join(parts)
    return str(data)


def extract_json_from_fenced_content(text: str) -> dict:
    """Extrait le JSON d'un bloc de code Markdown."""
    text = text.strip()
    if text.startswith("```"):
        first_newline = text.find("\n")
        if first_newline != -1: text = text[first_newline + 1:]
        fence_pos = text.rfind("```")
        if fence_pos != -1: text = text[:fence_pos]
    try: return json.loads(text)
    except json.JSONDecodeError: return {} # Renvoie vide en cas d'erreur pour ne pas crasher


def normalize_albert_ocr_structured(ocr_data: Any) -> dict:
    """Normalise la sortie JSON d'Albert.
    Gère le cas où Albert renvoie une liste de pages contenant chacune un bout de JSON.
    """
    final_experiences = []
    final_skills = []

    # 1. Cas simple : c'est déjà le dict final
    if isinstance(ocr_data, dict):
        if "experiences" in ocr_data and "skills" in ocr_data:
            return ocr_data

        # 2. Cas complexe : Liste de pages (ex: CV multipages)
        # Chaque page peut contenir son propre bloc ```json ... ```
        if "data" in ocr_data and isinstance(ocr_data["data"], list):
            found_any = False
            for page in ocr_data["data"]:
                if isinstance(page, dict):
                    content = page.get("content")
                    if isinstance(content, str):
                        # On essaie de parser CHAQUE page indépendamment
                        parsed_page = extract_json_from_fenced_content(content)
                        if parsed_page:
                            # Si on trouve des données, on les ajoute à la liste globale (fusion)
                            exps = parsed_page.get("experiences", [])
                            sks = parsed_page.get("skills", [])
                            if isinstance(exps, list): final_experiences.extend(exps)
                            if isinstance(sks, list): final_skills.extend(sks)
                            found_any = True

            # Si on a trouvé des données dans au moins une page
            if found_any:
                # On dédoublonne les skills (optionnel, mais propre)
                # Note: pour les experiences c'est plus dur de dédoubloner, on garde tout.
                unique_skills = list(set(final_skills)) if final_skills else []
                return {"experiences": final_experiences, "skills": unique_skills}

        # 3. Cas où le JSON est dans le champ "text"
        text = ocr_data.get("text")
        if isinstance(text, str):
            parsed = extract_json_from_fenced_content(text)
            if isinstance(parsed, dict) and ("experiences" in parsed or "skills" in parsed):
                return parsed

    # 4. Cas chaîne brute
    if isinstance(ocr_data, str):
        parsed = extract_json_from_fenced_content(ocr_data)
        if isinstance(parsed, dict) and ("experiences" in parsed or "skills" in parsed):
            return parsed

    # Fallback vide
    return {"experiences": [], "skills": []}


def build_extraction_prompt(cv_text: str) -> str:
    return PROMPT_LLM.format(cv_text=cv_text)

@track(name="tool_openrouter_llm")
def call_openrouter_llm(prompt: str) -> Dict[str, Any]:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "X-Title": "CV Extraction Benchmark"
    }
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": "Tu es un assistant d'extraction d'information pour des CV."},
            {"role": "user", "content": prompt}
        ],
        "response_format": {"type": "json_object"}
    }
    resp = requests.post(OPENROUTER_API_URL, headers=headers, data=json.dumps(payload), timeout=120)
    resp.raise_for_status()
    data = resp.json()
    content = data["choices"][0]["message"]["content"]
    try: parsed = json.loads(content)
    except json.JSONDecodeError: raise ValueError(f"Réponse LLM non-json : {content[:500]}")
    return parsed


# =============================
#  PIPELINES
# =============================

@track(name="pipeline_A_ocr_only")
def pipeline_a_ocr_only(pdf_path: str) -> Dict[str, Any]:
    start = time.perf_counter()
    with open(pdf_path, "rb") as f: pdf_bytes = f.read()

    ocr_structured_raw = call_albert_ocr(
        pdf_bytes, prompt=PROMPT_ALBERT.prompt, dpi=200, return_json=True
    )
    # Appel à la nouvelle fonction de normalisation qui gère le multi-page
    structured = normalize_albert_ocr_structured(ocr_structured_raw)
    latency = time.perf_counter() - start

    n_exp = len(structured.get("experiences", []) or [])
    n_sk = len(structured.get("skills", []) or [])

    update_current_trace(
        feedback_scores=[{"name": "n_experiences", "value": float(n_exp)}, {"name": "n_skills", "value": float(n_sk)}],
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
            "eval_context": text_reference,
            "raw_ocr_response": str(ocr_structured_raw)
        }
    }


@track(name="pipeline_B_pdf2text_llm")
def pipeline_b_pdf2text_llm(pdf_path: str) -> Dict[str, Any]:
    start = time.perf_counter()

    text = pdf_to_text(pdf_path)

    if ENABLE_ANONYMIZATION:
        processed_text = anonymize_text(text)
    else:
        processed_text = text

    prompt_text = build_extraction_prompt(processed_text)
    structured = call_openrouter_llm(prompt_text)
    latency = time.perf_counter() - start

    if not isinstance(structured, dict): structured = {"experiences": [], "skills": []}
    n_exp = len(structured.get("experiences", []) or [])
    n_sk = len(structured.get("skills", []) or [])

    update_current_trace(
        feedback_scores=[{"name": "n_experiences", "value": float(n_exp)}, {"name": "n_skills", "value": float(n_sk)}],
        metadata={
            "file": os.path.basename(pdf_path),
            "ocr_model_id": None,
            "llm_model_id": OPENROUTER_MODEL,
            "use_anonymization": ENABLE_ANONYMIZATION
        },
        prompts=[PROMPT_LLM],
    )

    return {
        "pipeline": "B_PDF2TEXT_LLM",
        "file": os.path.basename(pdf_path),
        "latency_sec": latency,
        "output": structured,
        "debug": {"eval_context": processed_text}
    }


@track(name="pipeline_C_ocr_llm")
def pipeline_c_ocr_llm(pdf_path: str) -> Dict[str, Any]:
    start_total = time.perf_counter()
    with open(pdf_path, "rb") as f: pdf_bytes = f.read()

    # 1. OCR
    start_ocr = time.perf_counter()
    ocr_text = str(call_albert_ocr(
        pdf_bytes, prompt="Texte brut lisible...", return_json=False
    ))
    end_ocr = time.perf_counter()
    ocr_duration = end_ocr - start_ocr

    # 2. Anonymisation
    if ENABLE_ANONYMIZATION:
        processed_text = anonymize_text(ocr_text)
    else:
        processed_text = ocr_text

    prompt_text = build_extraction_prompt(processed_text)

    # 3. LLM
    start_llm = time.perf_counter()
    structured = call_openrouter_llm(prompt_text)
    end_llm = time.perf_counter()
    llm_duration = end_llm - start_llm

    latency_total = time.perf_counter() - start_total
    if not isinstance(structured, dict): structured = {"experiences": [], "skills": []}

    n_exp = len(structured.get("experiences", []) or [])
    n_sk = len(structured.get("skills", []) or [])

    update_current_trace(
        feedback_scores=[{"name": "n_experiences", "value": float(n_exp)}, {"name": "n_skills", "value": float(n_sk)}],
        metadata={
            "file": os.path.basename(pdf_path),
            "ocr_model_id": ALBERT_OCR_MODEL,
            "llm_model_id": OPENROUTER_MODEL,
            "use_anonymization": ENABLE_ANONYMIZATION,
            "latency_ocr_step": ocr_duration,
            "latency_llm_step": llm_duration
        },
        prompts=[PROMPT_LLM],
    )

    return {
        "pipeline": "C_OCR_LLM",
        "file": os.path.basename(pdf_path),
        "latency_sec": latency_total,
        "latency_details": {"ocr": ocr_duration, "llm": llm_duration},
        "output": structured,
        "debug": {
            "eval_context": processed_text,
            "ocr_text_preview": ocr_text[:200] + "..."
        }
    }


# =============================
#  MAIN
# =============================

def run_all_pipelines_on_folder(folder: str, out_json: str = "results_benchmark.jsonl") -> None:
    pdf_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(".pdf")]
    print(f"Trouvé {len(pdf_files)} PDF dans {folder}")
    print(f"Anonymisation activée : {ENABLE_ANONYMIZATION}")

    with open(out_json, "w", encoding="utf-8") as out_f:
        for pdf_path in pdf_files:
            print(f"\n=== Fichier : {os.path.basename(pdf_path)} ===")
            for func in (pipeline_a_ocr_only, pipeline_b_pdf2text_llm, pipeline_c_ocr_llm):
                try:
                    result = func(pdf_path)
                    lat = result['latency_sec']
                    print(f"  -> {result['pipeline']} : {lat:.2f} s")
                    out_f.write(json.dumps(result, ensure_ascii=False) + "\n")
                except Exception as e:
                    print(f"  !! Erreur {func.__name__} : {e}")
                    out_f.write(json.dumps({"error": str(e)}, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python pipelines_cv.py <dossier_pdfs>")
        raise SystemExit(1)
    run_all_pipelines_on_folder(sys.argv[1])
