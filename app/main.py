import time
from fastapi import FastAPI, Request
from .api import router
from .metrics import REQUESTS_TOTAL, REQUEST_LATENCY

app = FastAPI(title="Task API", version="1.0.0")
app.include_router(router)


@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start

    path = request.url.path
    method = request.method
    status = str(response.status_code)

    REQUESTS_TOTAL.labels(
        method=method,
        path=path,
        status=status,
    ).inc()

    REQUEST_LATENCY.labels(
        method=method,
        path=path,
    ).observe(duration)

    return response
