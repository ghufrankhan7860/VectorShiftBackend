from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get('/')
def read_root():
    return {'Ping': 'Pong'}

from typing import List, Tuple
from pydantic import BaseModel

class PipelineParams(BaseModel):
    nodes: List[str]
    edges: List[Tuple[str, str]]

class PipelineRequest(BaseModel):
    pipeline: PipelineParams

@app.post('/pipelines/parse')
def parse_pipeline(pipeline: PipelineRequest):
    return {'status': 'parsed'}
