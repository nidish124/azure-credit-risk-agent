from fastapi import FastAPI
from api.routes import router
from fastapi.middleware.cors import CORSMiddleware
from config.validate_budget import validate_token_budget
from evaluation.metrics import router as metrics_router

from Opencensus.ext.fastapi.fastapi_middleware import FastAPIMiddleware
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.trace.samplers import ProbabilitySampler
from opencensus.trace.tracer import Tracer
import os

tracer = Tracer(
    exporter = AzureExporter(
        connection_string= os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
    ),
    sampler=ProbabilitySampler(1.0)
)

app = FastAPI(
    title="AI Credit Risk Decisioning API",
    version="1.0.0"
)

app.add_middleware(
    FastAPIMiddleware,
    tracer = tracer
)

prod_origins = [
    "https://credit-ai-app.whitestone-2b0f5c99.eastus.azurecontainerapps.io",
    "https://purple-bush-042ab5003.1.azurestaticapps.net"
]
# ✅ CORS configuration (safe for internal tools)

app.add_middleware(
    CORSMiddleware,
    allow_origins=prod_origins,          # For local dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

validate_token_budget()

app.include_router(router)
app.include_router(metrics_router)
