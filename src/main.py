from fastapi import FastAPI
from src.core import life_span, setup_cors

app = FastAPI(lifespan=life_span)
setup_cors(app)
