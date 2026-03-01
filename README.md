Markdown
# 🛣️ RoadCare: AI-Powered Pothole Reporting & Management System

![RoadCare Banner](https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?auto=format&fit=crop&q=80&w=1200&h=400)

RoadCare is a smart, crowdsourced road maintenance platform designed to bridge the gap between citizens, government bodies, and maintenance vendors. Powered by an advanced AI engine (YOLO), it automatically analyzes citizen-submitted videos to detect, track, and log unique potholes, assigning them to local vendors for repair.

Built for the **AMD Slingshot Competition**, this project demonstrates high-performance parallel processing, real-time UI updates, and a closed-loop civic accountability system.

---

## ✨ Key Features

* **🤖 AI Video Processing:** Uses a custom YOLO model to scan high-framerate video uploads in the background. It utilizes object tracking (`model.track`) to ensure the same pothole isn't counted twice, extracting only unique proof frames.
* **🗺️ Interactive Live Map:** A global Leaflet.js map showing all reported hazards, color-coded by AI-determined severity (High/Medium/Low).
* **🔄 Real-Time Auto-Polling:** Dashboards update instantly without page refreshes when the AI finishes a scan or a vendor accepts a job.
* **🔐 Role-Based Access (Mock Aadhaar):** Secure, distinct portals for Citizens (Reporters) and Vendors (Fixers) using simulated government ID verification.
* **✅ Closed-Loop Accountability:** Vendors receive automated assignments and cannot close a ticket without uploading photographic proof of the repaired road. Citizens then rate the repair quality.



---

## 🏗️ Architecture & Tech Stack

* **Frontend:** HTML5, Tailwind CSS, Vanilla JavaScript, Leaflet.js (Mapping).
* **Backend:** Python, FastAPI, Uvicorn.
* **AI / Computer Vision:** Ultralytics (YOLO), OpenCV.
* **Storage:** Local File System (`/uploads`), In-Memory JSON (for rapid prototyping).

---

## 🚀 Local Setup & Installation

Follow these steps to run the RoadCare platform on your local machine.

### 1. Prerequisites
* Python 3.8 or higher installed on your system.
* A custom YOLO model named `custom_pothole_model.pt` placed in the root directory.

### 2. Clone the Repository
`bash
git clone [https://github.com/yourusername/roadcare.git](https://github.com/yourusername/roadcare.git)
cd roadcare

3. Install Dependencies
Create a virtual environment (optional but recommended) and install the required Python packages:

Bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install fastapi uvicorn python-multipart ultralytics opencv-python

4. Run the Server
Use the custom runner script to start the server. This script intentionally ignores the uploads/ folder to prevent the server from continuously restarting while the AI saves video frames!

Bash
python run.py
The application will now be running at: http://127.0.0.1:8000

🧪 How to Demo the Platform
The database comes pre-loaded with mock Aadhaar identities for testing.

👤 Testing as a Citizen
Go to http://127.0.0.1:8000

Select the Citizen tab.

Enter Aadhaar: 452188901234 (Auto-fills: Aarav Sharma)

Password: password123

Action: Click "Report a Pothole", drop a pin on the map, and upload a test photo or video.

👷‍♂️ Testing as a Vendor
Log out or open an Incognito window to http://127.0.0.1:8000.

Select the Vendor tab.

Enter Aadhaar: 100200300401 (Auto-fills: RoadBuilders Pvt Ltd)

Password: road123

Action: You will see the citizen's report automatically routed here. Click Accept Report, then upload a repair photo to mark it Completed.

📁 Project Structure
Plaintext
📦 roadcare
 ┣ 📂 uploads/                # Local storage for citizen media and vendor proofs (auto-generated)
 ┣ 📜 main.py                 # FastAPI backend, routing, and database state management
 ┣ 📜 processor.py            # AI Engine: OpenCV and YOLO tracking logic for media analysis
 ┣ 📜 run.py                  # Uvicorn server entry point (with cache/reload exclusions)
 ┣ 📜 securityadd.html        # Main Frontend UI (Tailwind, JS, Leaflet Map)
 ┗ 📜 custom_pothole_model.pt # Your trained YOLO pothole detection model (MUST ADD THIS)
🔮 Future Roadmap
Cloud Database Migration: Move from in-memory JSON to PostgreSQL for persistent data storage.

Hardware Acceleration: Further optimize the AI processing pipeline for AMD GPUs.

Mobile App: Build a native React Native application for easier on-the-go reporting.

Predictive Maintenance: Use historical data to predict which roads are most likely to develop potholes in the next monsoon season.

Developed with ❤️ for safer roads.
