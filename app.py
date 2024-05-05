from fastapi import FastAPI, File, UploadFile
import uvicorn
import os
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse, FileResponse
from main import main

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

UPLOAD_FOLDER= '/Users/payal/Downloads/capstone/Modular'

@app.post("/Modular")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Save the uploaded file
        filename = file.filename
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        json_data = main(file_path)

        # Return the JSON data as a file response
        return FileResponse('excelToJson.json', media_type="application/json", filename="output.json")

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8087)
