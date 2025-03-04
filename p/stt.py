'''
import speech_recognition as sr
from pydub import AudioSegment

def convert_audio_to_text(audio_path):
    """음성 파일(MP3)을 텍스트로 변환"""
    # MP3 → WAV 변환 (AWS Lambda는 MP3 지원 안 함)
    audio = AudioSegment.from_mp3(audio_path)
    #audio.export("converted.wav", format="wav")
    audio.export(wav_path, format="wav")

    # 음성 인식 (STT)
    recognizer = sr.Recognizer()
    with sr.AudioFile("converted.wav") as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language="ko-KR")
            return text
        except sr.UnknownValueError:
            return "음성을 인식할 수 없습니다."
        except sr.RequestError as e:
            return f"STT 서비스 오류: {e}"

# 테스트 실행
if __name__ == "__main__":
    audio_path = "test.mp3"
    print("변환된 텍스트:", convert_audio_to_text(audio_path))
'''

import speech_recognition as sr
from pydub import AudioSegment
import os

def convert_audio_to_text(audio_path, wav_path):
    """음성 파일(MP3)을 텍스트로 변환 (AWS Lambda 지원)"""
    # MP3 → WAV 변환 (AWS Lambda는 MP3 지원 안 함)
    audio = AudioSegment.from_mp3(audio_path)
    audio.export(wav_path, format="wav")  # 변환된 파일을 지정된 경로에 저장

    # 음성 인식 (STT)
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language="ko-KR")
            return text
        except sr.UnknownValueError:
            return "음성을 인식할 수 없습니다."
        except sr.RequestError as e:
            return f"STT 서비스 오류: {e}"

# 테스트 실행
if __name__ == "__main__":
    audio_path = "test.mp3"
    wav_path = "converted.wav"  # 로컬 테스트용
    print("변환된 텍스트:", convert_audio_to_text(audio_path, wav_path))
