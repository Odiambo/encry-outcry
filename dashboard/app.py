#React scaffold for interaction in src/

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import os
import json

app = FastAPI()

LOG_DIRECTORY = os.environ.get("LOG_DIRECTORY", "storage/logs")
AUDIT_LOG = os.environ.get("AUDIT_LOG", "audit/audit.log")

@app.get("/logs/{log_id}")
def get_log(log_id: str):
    filepath = f"{LOG_DIRECTORY}/{log_id}.log"
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Log not found")
    with open(filepath, "r") as f:
        content = f.read()
    return {"log_id": log_id, "content": content}

@app.get("/audit")
def get_audit_trail():
    if not os.path.exists(AUDIT_LOG):
        return JSONResponse(content=[], status_code=200)
    with open(AUDIT_LOG, "r") as f:
        lines = f.readlines()
        entries = [json.loads(line) for line in lines]
    return entries
