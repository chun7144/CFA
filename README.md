# 📊 고객 피드백 분석 대시보드

고객 피드백 데이터를 분석하여 감성 분석, 키워드 추출, 워드클라우드 등을 제공하는 Streamlit 웹 애플리케이션입니다.

## 🚀 주요 기능

- **파일 업로드**: CSV, Excel 파일 지원
- **감성 분석**: 텍스트의 긍정/부정/중립 감정 분석
- **키워드 추출**: 자주 등장하는 단어 분석
- **워드클라우드**: 시각적 키워드 표현
- **텍스트 길이 분석**: 통계적 분석
- **결과 다운로드**: 분석 결과 CSV 파일 다운로드

## 📦 설치 및 실행

### 로컬 실행

```bash
# 의존성 설치
pip install -r requirements.txt

# 앱 실행
streamlit run streamlit_app.py
```

### Streamlit Cloud 배포

#### 1단계: Git 저장소 준비

```bash
# Git 초기화
git init

# 파일 추가
git add .

# 첫 커밋
git commit -m "Initial commit: Customer Feedback Analysis App"

# GitHub 원격 저장소 추가
git remote add origin https://github.com/사용자명/저장소명.git

# 메인 브랜치로 푸시
git branch -M main
git push -u origin main
```

#### 2단계: Streamlit Cloud 연결

1. [Streamlit Cloud](https://share.streamlit.io/)에 접속
2. GitHub 계정으로 로그인
3. "New app" 클릭
4. GitHub 저장소 선택
5. 메인 파일 경로: `streamlit_app.py`
6. "Deploy!" 클릭

#### 3단계: 배포 완료

- 배포가 완료되면 자동으로 URL이 생성됩니다
- GitHub에 코드를 푸시하면 자동으로 재배포됩니다

## 🛠️ 기술 스택

- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Matplotlib, WordCloud
- **Text Analysis**: TextBlob, Regular Expressions
- **File Handling**: CSV, Excel 파일 지원

## 📁 프로젝트 구조

```
CFA/
├── streamlit_app.py          # 메인 Streamlit 앱
├── app.py                    # 원본 앱 파일
├── requirements.txt          # Python 의존성
├── packages.txt             # 시스템 패키지
├── .streamlit/              # Streamlit 설정
│   └── config.toml
├── .gitignore               # Git 제외 파일
├── README.md                # 프로젝트 설명서
├── cfa-prd.txt             # 프로젝트 요구사항
└── sample_feedback_data.csv # 샘플 데이터
```

## 🔧 설정 파일

### `.streamlit/config.toml`
- 테마 색상 및 폰트 설정
- 서버 설정 (CORS, XSRF 보호 등)

### `packages.txt`
- 시스템 레벨 패키지 설치
- 한글 폰트 지원

## 📊 사용 방법

1. **데이터 업로드**: 사이드바에서 CSV 또는 Excel 파일 선택
2. **컬럼 선택**: 분석할 텍스트 컬럼 선택
3. **결과 확인**: 자동으로 분석 결과 및 시각화 확인
4. **결과 다운로드**: 분석 결과를 CSV 파일로 다운로드

## 🌐 지원 파일 형식

- **CSV**: UTF-8 인코딩 권장
- **Excel**: .xlsx, .xls 형식
- **데이터 구조**: 텍스트 컬럼이 포함된 표 형태

## 🔄 자동 배포

GitHub 저장소에 코드를 푸시하면 Streamlit Cloud에서 자동으로 재배포됩니다:

```bash
git add .
git commit -m "Update: 새로운 기능 추가"
git push origin main
```

## 📞 문제 해결

### 일반적인 문제들

1. **한글 폰트 문제**: `packages.txt`에 한글 폰트가 포함되어 있습니다
2. **의존성 오류**: `requirements.txt`의 버전 호환성 확인
3. **배포 실패**: GitHub 저장소 연결 상태 확인

### 로그 확인

Streamlit Cloud 대시보드에서 배포 로그를 확인할 수 있습니다.

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



