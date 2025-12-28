from fastapi import FastAPI
from api.routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI Credit Risk Decisioning API",
    version="1.0.0"
)

prod_origins = ["https://credit-ai-app.whitestone-2b0f5c99.eastus.azurecontainerapps.io"]
# ✅ CORS configuration (safe for internal tools)


app.add_middleware(
    CORSMiddleware,
    allow_origins=prod_origins,          # For local dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
