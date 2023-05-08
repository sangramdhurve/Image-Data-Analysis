import os
import shutil
from fastapi import FastAPI, File, UploadFile
from typing import List
from Analyze_dataset.DataAnalysis import analyze_dataset

app = FastAPI()

# Create a temporary directory to store uploaded files
temp_dir = "temp"
if not os.path.exists(temp_dir):
    os.mkdir(temp_dir)

@app.post("/analyze")
async def analyze(images: List[UploadFile] = File(...)):
    """
    Analyzes the given dataset and returns various statistics.
    """
    # Save the uploaded images to the temporary directory
    filenames = []
    for img in images:
        filename = os.path.join(temp_dir, img.filename)
        with open(filename, "wb") as f:
            shutil.copyfileobj(img.file, f)
        filenames.append(filename)

    # Analyze the dataset
    result = analyze_dataset(temp_dir, filenames)

    # Remove the temporary directory and files
    shutil.rmtree(temp_dir)

    return result

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=5500)


# run commad for this app would be:- uvicorn app:app --port 5500

