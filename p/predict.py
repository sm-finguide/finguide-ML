import joblib
from stt import convert_audio_to_text 

# 모델 & 벡터라이저 로드
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

def predict_phishing(text):
    """입력된 문장의 보이스피싱 여부 예측"""
    text_vectorized = vectorizer.transform([text])  # 텍스트 벡터화
    #prediction = model.predict(text_vectorized)  # 예측
    #return "보이스피싱" if prediction[0] == 1 else "정상"
    prediction_prob = model.predict_proba(text_vectorized)
    phishing_prob = prediction_prob[0][1]
    if phishing_prob > 0.5:
        return f"{phishing_prob * 100:.2f}%의 확률로 보이스피싱입니다."
    else:
        return f"{(1 - phishing_prob) * 100:.2f}%의 확률로 보이스피싱이 아닙니다."

'''
# 테스트 실행
if __name__ == "__main__":
    sample_text = "보안팀 연결을 위해 인증번호를 입력해주세요."
    print(predict_phishing(sample_text))
'''
# 테스트 실행
if __name__ == "__main__":
    audio_path = "test.mp3"  # 음성 파일 경로
    wav_path = "test.wav"  # 변환된 WAV 파일 저장 경로; 추가함
    text = convert_audio_to_text(audio_path, wav_path)  # 수정된 함수 호출
    print("STT 결과:", text)

    if text not in ["음성을 인식할 수 없습니다.", "STT 서비스 오류"]:  # 오류 메시지가 아닐 때만 예측 실행
        result = predict_phishing(text)
        print("예측 결과:", result)
    else:
        print("STT 변환 실패로 인해 예측을 실행할 수 없습니다.")
