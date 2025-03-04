from fastapi import FastAPI, File, UploadFile
from mangum import Mangum
import shutil
import os
from stt import convert_audio_to_text
from predict import predict_phishing
from pydub import AudioSegment

# Lambda에서 사용할 ffmpeg 경로 명시적으로 설정
AudioSegment.ffmpeg = "/opt/bin/ffmpeg"
AudioSegment.ffprobe = "/opt/bin/ffprobe"

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the API!"}

@app.post("/predict")
async def predict_voice(file: UploadFile = File(...)):
    """음성 파일을 업로드하면 보이스피싱 여부 반환"""
    temp_dir = "/tmp"  # Lambda에서는 /tmp만 사용 가능

    file_path = os.path.join(temp_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 변환된 WAV 파일 저장 경로
    wav_path = os.path.join(temp_dir, "converted.wav")

    # 음성을 텍스트로 변환
    text = convert_audio_to_text(file_path, wav_path)

    if text in ["음성을 인식할 수 없습니다.", "STT 서비스 오류"]:
        return {"text": text, "prediction": "예측 불가 (STT 실패)"}

    # 보이스피싱 예측
    result = predict_phishing(text)

    # 처리 후 임시 파일 삭제
    os.remove(file_path)
    if os.path.exists(wav_path):
        os.remove(wav_path)
        
    return {"text": text, "prediction": result}

# Lambda에서 실행할 수 있도록 Mangum 핸들러 추가
handler = Mangum(app)