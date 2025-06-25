from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError


class QuestionRequest(BaseModel):
    question: str

class QAResponse(BaseModel):
    question: str
    answer: str


class QAController:

    def __init__(self, ai_service):
        self.app = FastAPI()
        self.register_routes()
        self.register_exception_handlers()
        self.ai_service = ai_service

    def register_routes(self):
        @self.app.post("/ask", response_model=QAResponse)
        async def ask_question(request: QuestionRequest):
            # Simple logic to generate an answer
            answer = self.ai_service.answer(request.question) # <==== IA service aqui
            return {"question": request.question, "answer": answer}

    def register_exception_handlers(self):
        @self.app.exception_handler(ValidationError)
        async def validation_exception_handler(request: Request, exc: ValidationError):
            return JSONResponse(
                status_code=400,
                content={"error": "Invalid input", "details": exc.errors()}
            )

        @self.app.exception_handler(Exception)
        async def generic_exception_handler(request: Request, exc: Exception):
            return JSONResponse(
                status_code=500,
                content={"error": "Internal server error", "details": str(exc)}
            )