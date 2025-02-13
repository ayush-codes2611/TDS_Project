from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins; you can restrict this to specific domains
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def home(): 
    return {"message": "Hello!"}

# A mock function to simulate task execution (replace with LLM logic in your real application)
def execute_task(task_description: str):
    # Simulate task execution; replace this with actual logic (e.g., call to an LLM)
    if task_description == "example":
        return "Task executed successfully: Example task"
    else:
        raise ValueError("Invalid task description")

@app.post("/run")
async def run_task(task: str = Query(..., description="Task description")):
    try:
        # Attempt to execute the task
        result = execute_task(task)
        return {"message": "Task executed successfully", "result": result}
    except ValueError as e:
        # Handle task-related errors
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Catch all other exceptions (e.g., agent errors)
        raise HTTPException(status_code=500, detail=f"Agent failed to execute task: {str(e)}")

@app.get("/read")
async def read_file(path: str = Query(..., description="File path")):
    # Check if the file exists
    if os.path.exists(path):
        try:
            # Read and return the file content
            with open(path, 'r') as file:
                file_content = file.read()
            return file_content
        except Exception as e:
            # In case of an error reading the file, return HTTP 500
            raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")
    else:
        # File does not exist, return HTTP 404
        raise HTTPException(status_code=404, detail="File not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)