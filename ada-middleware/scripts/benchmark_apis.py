"""Script de comparación reproducible entre Groq API y Google Gemini API para ADA.

Uso:
    python scripts/benchmark_apis.py
Requiere configurar GROQ_API_KEY y/o GEMINI_API_KEY en .env o variables de entorno.
"""
import asyncio
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.agent.orchestrator import QuestionOrchestrator
from app.providers.router import ProviderRouter
from app.schemas.questions import QuestionGenerationRequest


async def run_benchmark() -> None:
    router = ProviderRouter()
    configured = router.configured_providers()
    if not configured:
        print("No hay API keys configuradas en .env (GROQ_API_KEY / GEMINI_API_KEY).")
        return

    out_dir = ROOT / "benchmark_outputs"
    out_dir.mkdir(exist_ok=True)
    orchestrator = QuestionOrchestrator(router=router)

    for provider in configured:
        req = QuestionGenerationRequest(
            moodle_version="5.0",
            course_shortname="ADA-PRUEBA-01",
            topic="Complejidad algorítmica (notación Big-O) y búsqueda binaria",
            count=3,
            difficulty="intermediate",
            language="es",
            provider=provider,  # type: ignore[arg-type]
        )
        print(f"\n--- Probando proveedor: {provider} ---")
        try:
            resp = await orchestrator.generate_multichoice_xml(req)
            out_file = out_dir / f"preguntas_{provider}.xml"
            out_file.write_text(resp.exported_content, encoding="utf-8")
            print(f"OK | Modelo: {resp.model_used} | Latencia: {resp.latency_ms} ms | Reintentos: {resp.retries}")
            print(f"Preguntas generadas: {len(resp.questions)} | Archivo XML: {out_file}")
        except Exception as exc:
            print(f"ERROR en {provider}: {exc}")


if __name__ == "__main__":
    asyncio.run(run_benchmark())

