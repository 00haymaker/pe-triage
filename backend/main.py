import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from coordinator import Coordinator

app = FastAPI(title="PE Triage API")

# 프론트엔드 연동을 위한 CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

coordinator = Coordinator()

@app.post("/api/analyze")
async def analyze_file(file: UploadFile = File(...)):
    # 1. uploads 폴더에 대용량 대응용 디스크 임시 저장
    temp_file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 저장 실패: {str(e)}")

    try:
        # 2. Coordinator 호출 (저장된 경로 전달)
        result = coordinator.run_triage(temp_file_path)
        return result
    finally:
        # 3. 분석 완료 후 임시 파일 정리
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)