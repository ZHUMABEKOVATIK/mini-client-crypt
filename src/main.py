from fastapi import FastAPI
from src.core import life_span, setup_cors
from src.api import routers

app = FastAPI(lifespan=life_span)
setup_cors(app)

app.include_router(routers)