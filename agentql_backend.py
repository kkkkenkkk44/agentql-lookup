from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import agentql
from playwright.sync_api import sync_playwright
from typing import List

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class AgentQLInput(BaseModel):
    url: str
    query: str
    emails: List[str] = []

@app.post("/run")
def run_query(data: AgentQLInput):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = agentql.wrap(browser.new_page())
            print(f"🔍 Visiting: {data.url}")
            page.goto(data.url, timeout=300000)
            result = page.query_data(data.query)
            browser.close()
            return {
                "emails": data.emails,
                "result": result
            }
    except Exception as e:
        print("❌ Error:", str(e))
        return {"error": str(e)}
