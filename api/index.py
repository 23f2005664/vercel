from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import statistics
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"]
)
# Load the telemetry data (make sure the q-vercel-latency.json is present)
with open("q-vercel-latency.json") as f:
    telemetry = json.load(f)

@app.post("/metrics")
async def metrics(request: Request):
    body = await request.json()
    regions = body["regions"]
    threshold = body["threshold_ms"]
    output = {}
    for region in regions:
        records = telemetry[region]
        latencies = [r["latency_ms"] for r in records]
        uptimes = [r["uptime"] for r in records]
        breaches = sum(l > threshold for l in latencies)
        output[region] = {
            "avg_latency": statistics.mean(latencies),
            "p95_latency": statistics.quantiles(latencies, n=100)[94],
            "avg_uptime": statistics.mean(uptimes),
            "breaches": breaches
        }
    return output
