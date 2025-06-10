from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dag import DAG, DAGInput
from typing import List, Tuple
from pydantic import BaseModel
from pydantic import BaseModel, UUID4
from typing import List, Tuple
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://your-frontend-domain.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Allow specific origins (use ["*"] for all)
    allow_credentials=True,
    allow_methods=["*"],              # Allow all HTTP methods
    allow_headers=["*"],              # Allow all headers
)

@app.get('/')
def read_root():
    return {'Ping': 'Pong'}

class Pipeline(BaseModel):
    nodes: List[UUID4]
    edges: List[Tuple[UUID4, UUID4]]

class PipelineRequest(BaseModel):
    pipeline: Pipeline

@app.post('/pipelines/parse')
def parse_pipeline(body: PipelineRequest):
    try:
        # Validate input with Pydantic and DAGInput
        dag_input = DAGInput(nodes=body.pipeline.nodes, edges=body.pipeline.edges)
        dag = DAG(dag_input)

        # Check for cycle
        has_cycle = dag.has_cycle()

        return {
            "num_nodes": len(dag_input.nodes),
            "num_edges": len(dag_input.edges),
            "is_dag": not has_cycle
        }

    except ValueError as ve:
        # Raised from DAG logic like cycle detection or invalid edge
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as e:
        # Unexpected errors (e.g., programming issues)
        raise HTTPException(status_code=500, detail="Internal Server Error: " + str(e))
