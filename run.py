import uvicorn

if __name__ == "__main__":
    # This script runs your app but tells the reloader to IGNORE the uploads folder
    uvicorn.run(
        "main:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True, 
        reload_excludes=["uploads/*"]  # 👈 This is the permanent fix
    )