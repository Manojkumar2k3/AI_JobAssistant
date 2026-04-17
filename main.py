from fastapi import FastAPI, UploadFile, File, Form
from services.resume_parser import extract_text_from_pdf
from services.ai_analyzer import extract_skills
from services.job_matcher import match_resume_with_jd
from models.request import JDRequest 

app = FastAPI()

@app.get("/")
def home():
    return{"message":"server working."}


@app.post("/analyze-resume")
async def analyze_resume(file: UploadFile = File(...)):
    text = extract_text_from_pdf(file.file)
    result = extract_skills(text)
    return {"analysis": result}

# API end-point
@app.post("/match-job") 
# User input 
async def match_job( 
    job_description: str = Form(...),
    file: UploadFile = File(...)
):
    resume_text = extract_text_from_pdf(file.file) #Resume Parsing
    result = match_resume_with_jd(resume_text, job_description) # Resume Matching(AI)
    return {"result": result} # Display Result

