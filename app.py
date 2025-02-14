from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
import os
import openai
import re
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins; you can restrict this to specific domains
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

def handle_task_A1(email):
    return f"A1 executed for {email}"

def parse_task_with_llm(task: str) -> dict:
    """
    Uses GPT-4o-Mini via the AI Proxy to parse the plain-English task and extract a structured task code.
    Expected output JSON format: {"task_code": "A3"}, for example.
    """
    token = os.environ.get("AIPROXY_TOKEN")
    if not token:
        raise Exception("AIPROXY_TOKEN environment variable not set")
    
    # Set the API key and base URL for the proxy.
    openai.api_key = token
    openai.api_base = "https://aiproxy.sanand.workers.dev/openai/v1"
    
    # Construct a prompt with explicit mappings between task descriptions and task codes.
    prompt = (
        "You are a task parser for DataWorks Solutions. Below are the explicit mappings of task descriptions to task codes:\n\n"
        "A1: 'Install uv (if required) and run datagen.py with ${user.email} as the only argument'\n"
        "A2: 'Format the contents of /data/format.md using prettier@3.4.2, updating the file in-place'\n"
        "A3: 'The file /data/dates.txt contains a list of dates, one per line. Count the number of Wednesdays and write just the number to /data/dates-wednesdays.txt'\n"
        "A4: 'Sort the array of contacts in /data/contacts.json by last_name, then first_name, and write the result to /data/contacts-sorted.json'\n"
        "A5: 'Write the first line of the 10 most recent .log files in /data/logs/ to /data/logs-recent.txt, most recent first'\n"
        "A6: 'Find all Markdown (.md) files in /data/docs/, extract the first occurrence of each H1, and create an index file /data/docs/index.json mapping filenames to titles'\n"
        "A7: '/data/email.txt contains an email message. Extract the sender’s email address using an LLM and write it to /data/email-sender.txt'\n"
        "A8: '/data/credit-card.png contains a credit card number. Use an LLM to extract the card number and write it without spaces to /data/credit-card.txt'\n"
        "A9: '/data/comments.txt contains a list of comments, one per line. Using embeddings, find the most similar pair of comments and write them to /data/comments-similar.txt, one per line'\n"
        "A10: 'The SQLite database file /data/ticket-sales.db has a table tickets with columns type, units, and price. Calculate the total sales for the \"Gold\" ticket type and write the number to /data/ticket-sales-gold.txt'\n\n"
        "Given the following instruction, determine which task code applies. "
        "Return a JSON object with a single key 'task_code' whose value is one of A1, A2, A3, A4, A5, A6, A7, A8, A9, or A10. "
        "If the instruction does not match any known task, return 'UNKNOWN'.\n\n"
        f"Instruction: \"{task}\"\n\n"
        "Return only the JSON object."
    )
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful task parser."},
                {"role": "user", "content": prompt},
            ]
        )
        
        # Debug: print the raw response.
        print("Raw LLM response:", response)
        
        # Extract the content.
        raw_message = response["choices"][0]["message"]["content"]
        
        # Remove markdown code fences if present.
        raw_message = re.sub(r"^```json\s*", "", raw_message)
        raw_message = re.sub(r"\s*```$", "", raw_message)
        
        if not raw_message.strip():
            raise Exception("LLM returned an empty response: " + str(response))
        
        parsed = json.loads(raw_message)
        return parsed
    except Exception as e:
        raise Exception(f"Error calling LLM: {str(e)}")

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
async def run_task(task: str = Query(...)):
    if not task:
        raise HTTPException(status_code=400, detail="Task description required")
    
    # Use the LLM to parse the task instruction.
    try:
        parsed_task = parse_task_with_llm(task)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing task with LLM: {str(e)}")
    
    task_code = parsed_task.get("task_code", "UNKNOWN").upper()
    
    # Map the task_code to the corresponding internal function using a dictionary.
    task_map = {
        "A1": lambda: handle_task_A1(os.environ.get("USER_EMAIL", "default@example.com")),
        # "A2": lambda: handle_task_A2(),
        # "A3": lambda: handle_task_A3(),
        # "A4": lambda: handle_task_A4(),
        # "A5": lambda: handle_task_A5(),
        # "A6": lambda: handle_task_A6(),
        # "A7": lambda: handle_task_A7(),
        # "A8": lambda: handle_task_A8(),
        # "A9": lambda: handle_task_A9(),
        # "A10": lambda: handle_task_A10()
    }

    try:
        # Execute the function based on the task_code, or raise an error for unknown task codes
        if task_code not in task_map:
            raise Exception("Unrecognized or unsupported task code returned by LLM.")
        
        result = task_map[task_code]()  # Call the corresponding lambda function
        
        return {"status": "success", "result": result}
    
    except Exception as e:
        # Return a specific error message based on the exception
        if isinstance(e, ValueError):
            raise HTTPException(status_code=400, detail=f"Error with task execution: {str(e)}")
        elif isinstance(e, KeyError):
            raise HTTPException(status_code=400, detail=f"Missing required data: {str(e)}")
        else:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/read")
async def read_file(path: str = Query(..., description="File path")):
    # Check if the file exists
    print(f"Received path: {path}")
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