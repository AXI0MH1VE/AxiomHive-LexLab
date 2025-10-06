from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from src.reasoning_body.logic_engine import ReasoningBody
from src.emotional_analyzer.emotion_processor import EmotionalAnalyzer
from src.ethics_sentinel.ethical_guard import EthicsSentinel
from src.entropy_matrix_harmonizer.coherence_engine import EntropyMatrixHarmonizer
from src.memory_trace_manager.memory_graph import MemoryTraceManager
from src.abstract_pattern_detector.pattern_finder import AbstractPatternDetector

app = FastAPI(
    title="Transcendent AI Chatbot API",
    description="A distributed, modular cognitive architecture for superior conversational AI.",
    version="3.0.0"
)

# Serve the frontend static files under /ui if the frontend folder exists
try:
    import os
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
    if os.path.isdir(frontend_path):
        app.mount('/ui', StaticFiles(directory=frontend_path, html=True), name='ui')
except Exception:
    # silent: if mounting fails we still expose API
    pass


@app.get('/')
async def root():
    return RedirectResponse(url='/ui/')

# Initialize core cognitive matrices
reasoning_body = ReasoningBody()
emotional_analyzer = EmotionalAnalyzer()
ethics_sentinel = EthicsSentinel()
harmonizer = EntropyMatrixHarmonizer()
memory_manager = MemoryTraceManager()
pattern_detector = AbstractPatternDetector()

class ChatbotRequest(BaseModel):
    user_id: str
    message: str
    conversation_id: str = None
    metadata: dict = {}


@app.post("/chat/process")
async def process_chat_message(request: ChatbotRequest):
    if not ethics_sentinel.validate_request(request.message):
        raise HTTPException(status_code=403, detail="Message violates ethical guidelines.")

    logical_analysis = reasoning_body.analyze(request.message)
    emotional_context = emotional_analyzer.analyze(request.message)
    pattern_analysis = pattern_detector.detect(request.message)

    memory_manager.add_memory(f"user_message_{request.user_id}_{request.conversation_id}",
                               {"content": request.message, "timestamp": app.extra.get("current_time", "unknown")})

    harmonized_output = harmonizer.synthesize(
        logical_analysis,
        emotional_context,
        pattern_analysis,
    )

    if not ethics_sentinel.validate_response(harmonized_output):
        return {"user_id": request.user_id, "response": "Response filtered by ethical guidelines. Please rephrase your query.", "conversation_id": request.conversation_id}

    return {"user_id": request.user_id, "response": harmonized_output, "conversation_id": request.conversation_id}


@app.get("/system/health")
async def health_check():
    return {"status": "operational", "cognitive_matrices": "online"}
