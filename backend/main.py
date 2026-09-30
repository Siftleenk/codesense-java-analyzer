
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from analyzer.analyzer import generate_report


app = FastAPI(
    title="CodeSense API",
    description="Java Code Quality and Code Smell Analyzer",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=False,

    allow_methods=["*"],

    allow_headers=["*"],
)


class CodeRequest(BaseModel):
    code: str


@app.get("/")
def home():

    return {
        "message": "Welcome to CodeSense API"
    }


@app.post("/analyze")
def analyze_code(request: CodeRequest):

    report = generate_report(
        request.code
    )

    return report
