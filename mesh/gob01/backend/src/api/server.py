import asyncio
import json
import os
import uuid
from typing import Dict, List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime, timezone

from src.common.models import (
    MemoryItem, MemorySaveRequest, MemoryQueryResponse,
    BehaviorAdjustRequest, AgentRunRequest, AgentRunResponse, ErrorResponse
)

PORT = int(os.getenv("PORT", "8080"))
ALLOW_ORIGINS = os.getenv("ALLOW_ORIGINS", "*").split(",")

app = FastAPI(title="Modular AI Backend", version="0.0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory stores (Phase 1)
MEMORY: Dict[str, MemoryItem] = {}
BEHAVIOR: Dict[str, List[str]] = {"global": []}

# Simple WS hub
class Hub:
    def __init__(self):
        self.connections: List[WebSocket] = []
        self.seq: int = 0

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.connections.append(ws)

    def remove(self, ws: WebSocket):
        if ws in self.connections:
            self.connections.remove(ws)

    async def publish(self, event_type: str, payload: dict, correlation_id: str | None = None):
        self.seq += 1
        AUDIT["events_emitted"] += 1
        AUDIT["last_seq"] = self.seq
        envelope = {
            "id": str(uuid.uuid4()),
            "ts": datetime.now(timezone.utc).isoformat(),
            "type": event_type,
            "source": "backend",
            "correlation_id": correlation_id or str(uuid.uuid4()),
            "seq": self.seq,
            "payload": payload,
        }
        dead = []
        for ws in self.connections:
            try:
                await ws.send_text(json.dumps(envelope))
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.remove(ws)

hub = Hub()

@app.websocket("/ws/stream")
async def ws_stream(ws: WebSocket):
    await hub.connect(ws)
    try:
        while True:
            # Keepalive / optional client messages
            await asyncio.sleep(60)
    except WebSocketDisconnect:
        hub.remove(ws)

@app.post("/memory/save", response_model=MemoryItem)
async def memory_save(req: MemorySaveRequest, request: Request):
    mid = str(uuid.uuid4())
    item = MemoryItem(id=mid, type=req.type, tags=req.tags, content=req.content, metadata=req.metadata)
    MEMORY[mid] = item
    corr = request.headers.get("x-correlation-id", str(uuid.uuid4()))
    await hub.publish("memory.saved", item.model_dump(), correlation_id=corr)
    return item

@app.get("/memory/query", response_model=MemoryQueryResponse)
async def memory_query(type: str | None = None, tag: str | None = None):
    items = list(MEMORY.values())
    if type:
        items = [i for i in items if i.type == type]
    if tag:
        items = [i for i in items if tag in i.tags]
    return MemoryQueryResponse(items=items)

@app.post("/behavior/adjust")
async def behavior_adjust(req: BehaviorAdjustRequest, request: Request):
    scope = req.scope or "global"
    rules = BEHAVIOR.get(scope, [])
    # simple merge, dedupe
    new_rules = list(dict.fromkeys(rules + req.rules))
    BEHAVIOR[scope] = new_rules
    corr = request.headers.get("x-correlation-id", str(uuid.uuid4()))
    await hub.publish("behavior.updated", {"scope": scope, "rules": new_rules}, correlation_id=corr)
    return {"ok": True, "scope": scope, "rules": new_rules}

@app.get("/behavior")
async def behavior_get(scope: str = "global"):
    return {"scope": scope, "rules": BEHAVIOR.get(scope, [])}

@app.post("/agents/run", response_model=AgentRunResponse)
async def agents_run(req: AgentRunRequest, request: Request):
    run_id = str(uuid.uuid4())
    corr = request.headers.get("x-correlation-id", run_id)

    # Emit a few fake log tokens over WS to simulate an agent run
    async def simulate():
        await hub.publish("agent.logs", {"run_id": run_id, "msg": f"Starting: {req.instruction}"}, correlation_id=corr)
        await asyncio.sleep(0.2)
        await hub.publish("agent.logs", {"run_id": run_id, "msg": "Thinking..."}, correlation_id=corr)
        await asyncio.sleep(0.2)
        await hub.publish("agent.logs", {"run_id": run_id, "msg": "Done."}, correlation_id=corr)

    asyncio.create_task(simulate())
    return AgentRunResponse(run_id=run_id)

@app.get("/health")
async def health():
    return {"status": "ok", "audit": AUDIT}

# Entry point
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api.server:app", host="0.0.0.0", port=PORT, reload=False)

from typing import Optional
from collections import defaultdict

AUDIT = {
    "requests": 0,
    "events_emitted": 0,
    "last_seq": 0,
}

@app.middleware("http")
async def correlation_and_audit(request, call_next):
    AUDIT["requests"] += 1
    cid = request.headers.get("x-correlation-id")
    response = await call_next(request)
    if cid:
        response.headers["x-correlation-id"] = cid
    return response


from fastapi.responses import JSONResponse

@app.exception_handler(HTTPException)
async def http_exc_handler(request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": {"code": exc.status_code, "message": exc.detail, "details": {}}})

@app.exception_handler(Exception)
async def unhandled_exc_handler(request, exc: Exception):
    return JSONResponse(status_code=500, content={"error": {"code": 500, "message": "Internal Server Error", "details": {"type": type(exc).__name__}}})
