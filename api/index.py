from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import statistics
from fastapi import Response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Embed telemetry data as a Python list (copied from your JSON file above)
telemetry_raw = [
    {"region": "apac", "service": "catalog", "latency_ms": 148.88, "uptime_pct": 98.304, "timestamp": 20250301},
    {"region": "apac", "service": "catalog", "latency_ms": 188.21, "uptime_pct": 98.94, "timestamp": 20250302},
    {"region": "apac", "service": "checkout", "latency_ms": 186.76, "uptime_pct": 98.655, "timestamp": 20250303},
    {"region": "apac", "service": "checkout", "latency_ms": 228.86, "uptime_pct": 99.232, "timestamp": 20250304},
    {"region": "apac", "service": "payments", "latency_ms": 191.24, "uptime_pct": 97.215, "timestamp": 20250305},
    {"region": "apac", "service": "payments", "latency_ms": 159.61, "uptime_pct": 98.301, "timestamp": 20250306},
    {"region": "apac", "service": "catalog", "latency_ms": 218.37, "uptime_pct": 98.942, "timestamp": 20250307},
    {"region": "apac", "service": "catalog", "latency_ms": 196.12, "uptime_pct": 98.527, "timestamp": 20250308},
    {"region": "apac", "service": "support", "latency_ms": 186.19, "uptime_pct": 98.527, "timestamp": 20250309},
    {"region": "apac", "service": "support", "latency_ms": 143.83, "uptime_pct": 98.213, "timestamp": 20250310},
    {"region": "apac", "service": "analytics", "latency_ms": 190.72, "uptime_pct": 97.692, "timestamp": 20250311},
    {"region": "apac", "service": "recommendations", "latency_ms": 162.46, "uptime_pct": 97.249, "timestamp": 20250312},
    {"region": "emea", "service": "catalog", "latency_ms": 170.31, "uptime_pct": 97.153, "timestamp": 20250301},
    {"region": "emea", "service": "catalog", "latency_ms": 160.74, "uptime_pct": 97.345, "timestamp": 20250302},
    {"region": "emea", "service": "payments", "latency_ms": 176.04, "uptime_pct": 97.605, "timestamp": 20250303},
    {"region": "emea", "service": "analytics", "latency_ms": 167.8, "uptime_pct": 99.494, "timestamp": 20250304},
    {"region": "emea", "service": "payments", "latency_ms": 191.99, "uptime_pct": 97.355, "timestamp": 20250305},
    {"region": "emea", "service": "catalog", "latency_ms": 140.18, "uptime_pct": 98.675, "timestamp": 20250306},
    {"region": "emea", "service": "analytics", "latency_ms": 163.46, "uptime_pct": 97.885, "timestamp": 20250307},
    {"region": "emea", "service": "analytics", "latency_ms": 135.73, "uptime_pct": 99.48, "timestamp": 20250308},
    {"region": "emea", "service": "catalog", "latency_ms": 120.44, "uptime_pct": 98.789, "timestamp": 20250309},
    {"region": "emea", "service": "catalog", "latency_ms": 141.64, "uptime_pct": 98.782, "timestamp": 20250310},
    {"region": "emea", "service": "payments", "latency_ms": 131.51, "uptime_pct": 98.675, "timestamp": 20250311},
    {"region": "emea", "service": "support", "latency_ms": 217.84, "uptime_pct": 98.148, "timestamp": 20250312},
    {"region": "amer", "service": "catalog", "latency_ms": 227.72, "uptime_pct": 97.481, "timestamp": 20250301},
    {"region": "amer", "service": "analytics", "latency_ms": 117.73, "uptime_pct": 98.449, "timestamp": 20250302},
    {"region": "amer", "service": "checkout", "latency_ms": 150.23, "uptime_pct": 98.163, "timestamp": 20250303},
    {"region": "amer", "service": "analytics", "latency_ms": 126.17, "uptime_pct": 97.75, "timestamp": 20250304},
    {"region": "amer", "service": "analytics", "latency_ms": 206.68, "uptime_pct": 99.482, "timestamp": 20250305},
    {"region": "amer", "service": "analytics", "latency_ms": 115.65, "uptime_pct": 97.332, "timestamp": 20250306},
    {"region": "amer", "service": "support", "latency_ms": 164.75, "uptime_pct": 98.803, "timestamp": 20250307},
    {"region": "amer", "service": "checkout", "latency_ms": 188.13, "uptime_pct": 98.526, "timestamp": 20250308},
    {"region": "amer", "service": "analytics", "latency_ms": 113.92, "uptime_pct": 99.344, "timestamp": 20250309},
    {"region": "amer", "service": "analytics", "latency_ms": 130.34, "uptime_pct": 97.702, "timestamp": 20250310},
    {"region": "amer", "service": "catalog", "latency_ms": 202.44, "uptime_pct": 97.792, "timestamp": 20250311},
    {"region": "amer", "service": "catalog", "latency_ms": 104.13, "uptime_pct": 99.01, "timestamp": 20250312}
]

def get_metrics(region, threshold):
    region_records = [r for r in telemetry_raw if r["region"] == region]
    latencies = [r["latency_ms"] for r in region_records]
    uptimes = [r["uptime_pct"] for r in region_records]
    breaches = sum(l > threshold for l in latencies)
    # 95th percentile (manual)
    sorted_latencies = sorted(latencies)
    if sorted_latencies:
        idx = max(int(0.95 * len(sorted_latencies)) - 1, 0)
        p95 = sorted_latencies[idx]
        avg_latency = round(statistics.mean(latencies), 2)
        avg_uptime = round(statistics.mean(uptimes), 3)
    else:
        p95 = avg_latency = avg_uptime = 0
    return {
        "avg_latency": avg_latency,
        "p95_latency": round(p95, 2),
        "avg_uptime": avg_uptime,
        "breaches": breaches
    }

@app.options("/")
async def options_handler():
    return Response(status_code=200)

@app.post("/")
async def post_metrics(request: Request):
    body = await request.json()
    regions = body.get("regions", [])
    threshold = body.get("threshold_ms", 0)
    resp = {region: get_metrics(region, threshold) for region in regions}
    return resp

# Root GET for quick status check
@app.get("/")
def root():
    return {"status": "working"}
