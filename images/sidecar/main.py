import os
from fastapi import FastAPI
import uvicorn
import uuid

app = FastAPI()

class App:
    @staticmethod
    def get_token():
        #command = "bash /usr/local/bin/get-freepbx-credentials.sh"
        #token = os.popen(command).read()
        token = str(uuid.uuid4())
        return token

@app.get("/token")
async def get_vault_token():
    token = App.get_token()
    return token


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", log_level="info")

