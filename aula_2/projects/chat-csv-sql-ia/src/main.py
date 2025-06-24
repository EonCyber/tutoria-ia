import uvicorn
import os
from controller.api import QAController
from ai.service import AiService
from db.engine import DataBase
from pipeline.to_sql import CsvToSqlPipeline
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv('DB_PATH') # [db folder]
DATA_PATH = os.getenv('DATA_PATH') # [csv folder]

# Configure Database [sqlite] and Run Data Pipeline [csv to sql]
pipeline = CsvToSqlPipeline(DATA_PATH)
engine = DataBase(pipeline).create_engine_and_run_conversion_pipelines()
# Connect and start Ai Chains [langchain]
ia_service = AiService(engine)
# Start Api Controller [fastapi]
qa_controller = QAController(ia_service)
app = qa_controller.app

# Start Server on Port
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)