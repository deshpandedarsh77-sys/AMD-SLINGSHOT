import cv2
import os
from ultralytics import YOLO

model = YOLO("custom_pothole_model.pt") 

def analyze_media(file_path, lat, lng, is_video, report_id, reports_db):
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    captured_ids = set() 
    LOADING_GIF = "https://i.gifer.com/ZKZg.gif"
    
    if is_video:
        cap = cv2.VideoCapture(file_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            
            results = model.track(frame, persist=True, conf=0.6)
            
            if results[0].boxes.id is not None:
                track_ids = results[0].boxes.id.int().cpu().tolist()
                for i, track_id in enumerate(track_ids):
                    if track_id not in captured_ids:
                        captured_ids.add(track_id)
                        
                        # Process the frame
                        annotated_frame = results[0].plot() 
                        proof_filename = f"{base_name}_id_{track_id}.jpg"
                        proof_filepath = os.path.join("uploads", proof_filename)
                        cv2.imwrite(proof_filepath, annotated_frame)
                        new_url = f"http://localhost:8000/uploads/{proof_filename}"
                        
                        # 燥 Update DB: Add the photo AND keep the loading gif at the end
                        for report in reports_db:
                            if report["id"] == report_id:
                                # Filter out any old loading gifs first
                                current_images = [img for img in report["images"] if img != LOADING_GIF]
                                # Add the new proof and re-attach the loading gif to the end
                                report["images"] = current_images + [new_url, LOADING_GIF]
                                break
        cap.release()
    else:
        # Photo Logic
        print(f"🚀 [AMD AI ENGINE] Scanning photo at {lat}, {lng}...")
        frame = cv2.imread(file_path) # Load the single image
        if frame is not None:
            # We don't need 'track' for a photo, just a single 'predict'
            results = model.predict(frame, conf=0.6)
            
            if len(results[0].boxes) > 0:
                print(f"⚠️ Pothole found in photo! Saving proof...")
                annotated_frame = results[0].plot() 
                proof_filename = f"{base_name}_proof.jpg"
                proof_filepath = os.path.join("uploads", proof_filename)
                
                cv2.imwrite(proof_filepath, annotated_frame)
                proof_url = f"http://localhost:8000/uploads/{proof_filename}"
                
                # Update the database instantly
                for report in reports_db:
                    if report["id"] == report_id:
                        report["images"] = [proof_url] # Replace loading gif
                        break
    # Logic for photos is simpler since it's just one scan