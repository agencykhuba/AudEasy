from fastapi import FastAPI
import pandas as pd

app = FastAPI()

@app.get("/hello")
async def read_root():
    return {"message": "Hello, AudEasy Backend!"}

@app.get("/audit")
async def audit():
    df = pd.DataFrame({"value": [1, 2, 3]})
    return {"sum": int(df.sum())}
