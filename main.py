from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from typing import Optional
import shutil
import os
import uuid
import random
from datetime import datetime
from processor import analyze_media

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

reports_db = []

@app.get("/")
async def serve_frontend():
    return FileResponse("securityadd.html")

@app.get("/api/reports")
async def get_reports():
    return reports_db

def background_ai_job(report_id: str, file_path: str, lat: float, lng: float, is_video: bool):
    analyze_media(file_path, lat, lng, is_video, report_id, reports_db)
    
    LOADING_GIF = "https://i.gifer.com/ZKZg.gif"
    for report in reports_db:
        if report["id"] == report_id:
            report["images"] = [img for img in report["images"] if img != LOADING_GIF]
            report["status"] = "pending"
            report["statusText"] = "Pending Vendor"
            report["description"] = f"AI scanning complete. {len(report['images'])} unique potholes verified."
            break

# --- CITIZEN ACTION: SUBMIT REPORT ---
@app.post("/api/reports/submit")
async def submit_report(
    background_tasks: BackgroundTasks,
    lat: float = Form(...),
    lng: float = Form(...),
    locationStr: str = Form("Unknown Location"),
    city: str = Form(""),
    district: str = Form(""),
    state: str = Form(""),
    reportedBy: str = Form("Anonymous"), 
    photo: Optional[UploadFile] = File(None),
    video: Optional[UploadFile] = File(None)
):
    file_id = f"RPT-{str(uuid.uuid4())[:6].upper()}"
    active_file = video if video else photo
    is_video = video is not None

    file_extension = os.path.splitext(active_file.filename)[1] or (".mp4" if is_video else ".jpg")
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}{file_extension}")
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(active_file.file, buffer)

    VENDORS = ["RoadBuilders Pvt Ltd", "City Infra Solutions", "Metro Maintenance Corp"]
    assigned_vendor = random.choice(VENDORS)

    new_report = {
        "id": file_id,
        "location": locationStr, 
        "reportedBy": reportedBy, 
        "date": datetime.now().strftime("%Y-%m-%d"),
        "status": "in-progress", 
        "statusText": "⏳ AI Processing...",
        "severity": "medium", 
        "vendor": assigned_vendor, 
        "description": "AMD AI is currently scanning every frame...",
        "images": ["https://i.gifer.com/ZKZg.gif"], 
        "lat": lat,
        "lng": lng,
        "city": city,
        "district": district,
        "state": state 
    }
    
    reports_db.insert(0, new_report) 
    background_tasks.add_task(background_ai_job, file_id, file_path, lat, lng, is_video)

    return {"status": "success", "message": "Report lodged!", "report": new_report}

# --- VENDOR ACTION: ACCEPT REPORT ---
@app.post("/api/reports/{report_id}/accept")
async def accept_report(report_id: str, vendor_name: str = Form(...)):
    for report in reports_db:
        if report["id"] == report_id:
            report["status"] = "in-progress"
            report["statusText"] = "Vendor Working"
            report["vendor"] = vendor_name
            return {"status": "success", "report": report}
    return {"status": "error", "message": "Report not found"}

# --- VENDOR ACTION: COMPLETE REPAIR ---
@app.post("/api/reports/{report_id}/complete")
async def complete_repair(report_id: str, photo: UploadFile = File(...)):
    file_id = f"FIX-{uuid.uuid4().hex[:6].upper()}"
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.jpg")
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)
        
    for report in reports_db:
        if report["id"] == report_id:
            report["status"] = "completed"
            report["statusText"] = "Repair Completed"
            report["images"].append(f"http://localhost:8000/uploads/{file_id}.jpg")
            return {"status": "success", "report": report}
    return {"status": "error", "message": "Report not found"}

# --- CITIZEN ACTION: RATE VENDOR ---
@app.post("/api/reports/{report_id}/rate")
async def rate_vendor(report_id: str, rating: int = Form(...)):
    for report in reports_db:
        if report["id"] == report_id:
            report["rating"] = rating
            return {"status": "success"}
    return {"status": "error"}