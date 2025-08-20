import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from textblob import TextBlob
import re
from collections import Counter
# NLTK 관련 import 제거 (한국어 처리에 불필요)
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import io
import base64

# 페이지 설정
st.set_page_config(
    page_title="고객 피드백 분석",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'

# NLTK 데이터 다운로드 제거 (한국어 처리에 불필요)

# 한국어 불용어 설정
korean_stopwords = set(['이', '그', '저', '것', '수', '등', '때', '곳', '말', '일', '년', '월', '일', '시', '분', '초'])

def load_data(uploaded_file):
    """데이터 파일 로드"""
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("지원되지 않는 파일 형식입니다. CSV 또는 Excel 파일을 업로드해주세요.")
            return None
        return df
    except Exception as e:
        st.error(f"파일 로드 중 오류가 발생했습니다: {str(e)}")
        return None

def preprocess_text(text):
    """텍스트 전처리"""
    if pd.isna(text):
        return ""
    
    # 특수문자 제거 및 소문자 변환
    text = re.sub(r'[^\w\s]', '', str(text))
    text = text.lower()
    
    # 간단한 공백 기반 토큰화 (NLTK 의존성 제거)
    tokens = text.split()
    
    # 불용어 제거
    tokens = [token for token in tokens if token not in korean_stopwords and len(token) > 1]
    
    return ' '.join(tokens)

def analyze_sentiment(text):
    """감성 분석 (TextBlob 사용)"""
    if pd.isna(text) or text == "":
        return "중립"
    
    # 한국어 텍스트를 영어로 번역하여 감성 분석 (간단한 구현)
    # 실제 프로덕션에서는 한국어 전용 감성 분석 모델 사용 권장
    
    # 간단한 키워드 기반 감성 분석
    positive_words = ['좋', '편', '빠르', '유용', '친절', '깔끔', '직관', '간단']
    negative_words = ['느리', '어렵', '오류', '충돌', '문제', '불편', '아프', '작']
    
    text_lower = str(text).lower()
    
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count > negative_count:
        return "긍정"
    elif negative_count > positive_count:
        return "부정"
    else:
        return "중립"

def extract_keywords(texts, top_n=10):
    """키워드 추출"""
    all_words = []
    for text in texts:
        if pd.notna(text):
            processed_text = preprocess_text(text)
            words = processed_text.split()
            all_words.extend(words)
    
    # 빈도 계산
    word_freq = Counter(all_words)
    
    # 상위 키워드 반환
    return word_freq.most_common(top_n)

def create_wordcloud(texts):
    """워드클라우드 생성"""
    if not texts or all(pd.isna(texts)):
        return None
    
    # 텍스트 결합
    combined_text = ' '.join([str(text) for text in texts if pd.notna(text)])
    
    if not combined_text.strip():
        return None
    
    # 워드클라우드 생성
    wordcloud = WordCloud(
        font_path='malgun.ttf',  # Windows 기본 한글 폰트
        width=800, 
        height=400,
        background_color='white',
        max_words=100,
        colormap='viridis'
    ).generate(combined_text)
    
    return wordcloud

def main():
    st.title("📊 고객 피드백 분석 대시보드")
    st.markdown("---")
    
    # 사이드바 - 파일 업로드
    st.sidebar.header("📁 데이터 업로드")
    uploaded_file = st.sidebar.file_uploader(
        "CSV 또는 Excel 파일을 선택하세요",
        type=['csv', 'xlsx', 'xls']
    )
    
    if uploaded_file is not None:
        # 데이터 로드
        df = load_data(uploaded_file)
        
        if df is not None:
            st.success(f"✅ {uploaded_file.name} 파일이 성공적으로 로드되었습니다!")
            
            # 데이터 미리보기
            st.subheader("📋 데이터 미리보기")
            st.dataframe(df.head(), use_container_width=True)
            
            # 데이터 정보
            st.subheader("ℹ️ 데이터 정보")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("총 행 수", len(df))
            with col2:
                st.metric("총 열 수", len(df.columns))
            with col3:
                st.metric("메모리 사용량", f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
            
            # 텍스트 컬럼 선택
            text_columns = df.select_dtypes(include=['object']).columns.tolist()
            
            if text_columns:
                selected_text_column = st.sidebar.selectbox(
                    "분석할 텍스트 컬럼을 선택하세요",
                    text_columns
                )
                
                if selected_text_column:
                    st.subheader(f"📝 {selected_text_column} 컬럼 분석")
                    
                    # 감성 분석
                    st.write("**감성 분석 결과**")
                    df['감성'] = df[selected_text_column].apply(analyze_sentiment)
                    
                    sentiment_counts = df['감성'].value_counts()
                    fig_sentiment = px.pie(
                        values=sentiment_counts.values,
                        names=sentiment_counts.index,
                        title="감성 분석 분포",
                        color_discrete_map={'긍정': '#2E8B57', '중립': '#FFD700', '부정': '#DC143C'}
                    )
                    st.plotly_chart(fig_sentiment, use_container_width=True)
                    
                    # 키워드 추출
                    st.write("**상위 키워드**")
                    keywords = extract_keywords(df[selected_text_column], top_n=15)
                    
                    if keywords:
                        # 키워드 시각화
                        keyword_df = pd.DataFrame(keywords, columns=['키워드', '빈도'])
                        fig_keywords = px.bar(
                            keyword_df,
                            x='빈도',
                            y='키워드',
                            orientation='h',
                            title="상위 키워드 빈도",
                            color='빈도',
                            color_continuous_scale='viridis'
                        )
                        st.plotly_chart(fig_keywords, use_container_width=True)
                        
                        # 키워드 테이블
                        st.dataframe(keyword_df, use_container_width=True)
                    
                    # 워드클라우드
                    st.write("**워드클라우드**")
                    wordcloud = create_wordcloud(df[selected_text_column])
                    
                    if wordcloud:
                        fig, ax = plt.subplots(figsize=(10, 6))
                        ax.imshow(wordcloud, interpolation='bilinear')
                        ax.axis('off')
                        st.pyplot(fig)
                    else:
                        st.warning("워드클라우드를 생성할 수 없습니다.")
                    
                    # 텍스트 길이 분석
                    st.write("**텍스트 길이 분석**")
                    df['텍스트_길이'] = df[selected_text_column].astype(str).str.len()
                    
                    fig_length = px.histogram(
                        df,
                        x='텍스트_길이',
                        nbins=30,
                        title="텍스트 길이 분포",
                        labels={'텍스트_길이': '텍스트 길이', 'count': '빈도'}
                    )
                    st.plotly_chart(fig_length, use_container_width=True)
                    
                    # 길이 통계
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("평균 길이", f"{df['텍스트_길이'].mean():.1f}")
                    with col2:
                        st.metric("중앙값", f"{df['텍스트_길이'].median():.1f}")
                    with col3:
                        st.metric("최소 길이", f"{df['텍스트_길이'].min()}")
                    with col4:
                        st.metric("최대 길이", f"{df['텍스트_길이'].max()}")
                    
                    # 감성별 텍스트 길이 비교
                    st.write("**감성별 텍스트 길이 비교**")
                    fig_sentiment_length = px.box(
                        df,
                        x='감성',
                        y='텍스트_길이',
                        title="감성별 텍스트 길이 분포",
                        color='감성',
                        color_discrete_map={'긍정': '#2E8B57', '중립': '#FFD700', '부정': '#DC143C'}
                    )
                    st.plotly_chart(fig_sentiment_length, use_container_width=True)
                    
                    # 상세 분석 결과 다운로드
                    st.subheader("💾 분석 결과 다운로드")
                    
                    # 감성 분석 결과를 CSV로 다운로드
                    csv = df[['감성', '텍스트_길이']].to_csv(index=False, encoding='utf-8-sig')
                    st.download_button(
                        label="감성 분석 결과 다운로드 (CSV)",
                        data=csv,
                        file_name="sentiment_analysis_results.csv",
                        mime="text/csv"
                    )
                    
            else:
                st.warning("분석할 수 있는 텍스트 컬럼이 없습니다.")
                
        else:
            st.error("파일을 로드할 수 없습니다. 파일 형식을 확인해주세요.")
    
    else:
        st.info("👆 사이드바에서 데이터 파일을 업로드해주세요.")
        
        # 샘플 데이터 사용 안내
        st.subheader("📚 사용 방법")
        st.markdown("""
        1. **파일 업로드**: 사이드바에서 CSV 또는 Excel 파일을 선택하세요
        2. **컬럼 선택**: 분석할 텍스트 컬럼을 선택하세요
        3. **결과 확인**: 자동으로 감성 분석, 키워드 추출, 워드클라우드가 생성됩니다
        4. **결과 다운로드**: 분석 결과를 CSV 파일로 다운로드할 수 있습니다
        """)
        
        # 샘플 데이터 표시
        st.subheader("📖 지원되는 파일 형식")
        st.markdown("""
        - **CSV 파일**: UTF-8 인코딩 권장
        - **Excel 파일**: .xlsx, .xls 형식 지원
        - **데이터 구조**: 텍스트 컬럼이 포함된 표 형태의 데이터
        """)

if __name__ == "__main__":
    main()
