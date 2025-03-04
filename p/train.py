# 필요한 라이브러리 설치
# joblib install 완료
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# 1. 데이터 로드 (CSV 파일 사용)
df = pd.read_csv("voice.csv")  # 음성 데이터 텍스트화된 파일
X = df["추출된 텍스트"]
y = df["label"]  # 보이스피싱: 1, 정상: 0

# 2. 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. TF-IDF 벡터화
vectorizer = TfidfVectorizer(max_features=5000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# 4. 모델 학습
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train_tfidf, y_train)

# 5. 모델 평가
y_pred = model.predict(X_test_tfidf)
print("정확도:", accuracy_score(y_test, y_pred))

# 6. 모델 & 벡터라이저 저장
joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")
print("모델 저장 완료")
