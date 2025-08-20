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
    return dict(word_freq.most_common(top_n))

def create_wordcloud(keywords):
    """워드클라우드 생성"""
    if not keywords:
        return None
    
    wordcloud = WordCloud(
        width=800, 
        height=400, 
        background_color='white',
        font_path='malgun.ttf',  # Windows 기본 한글 폰트
        max_words=50
    ).generate_from_frequencies(keywords)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    
    # Streamlit에 표시
    st.pyplot(fig)
    plt.close()

def main():
    st.title("📊 고객 피드백 분석 대시보드")
    st.markdown("---")
    
    # 사이드바
    st.sidebar.header("📁 데이터 업로드")
    uploaded_file = st.sidebar.file_uploader(
        "CSV 또는 Excel 파일을 업로드하세요",
        type=['csv', 'xlsx', 'xls']
    )
    
    # 샘플 데이터 사용 옵션
    use_sample = st.sidebar.checkbox("샘플 데이터 사용", value=True)
    
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        if df is not None:
            st.success("파일이 성공적으로 업로드되었습니다!")
    elif use_sample:
        df = pd.read_csv("sample_feedback_data.csv")
        st.info("샘플 데이터를 사용하고 있습니다.")
    else:
        st.warning("파일을 업로드하거나 샘플 데이터를 선택해주세요.")
        return
    
    if df is None or df.empty:
        st.error("데이터를 불러올 수 없습니다.")
        return
    
    # 데이터 미리보기
    st.subheader("📋 데이터 미리보기")
    st.dataframe(df.head(), use_container_width=True)
    
    # 기본 통계
    st.subheader("📈 기본 통계")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("총 피드백 수", len(df))
    
    with col2:
        if 'rating' in df.columns:
            avg_rating = df['rating'].mean()
            st.metric("평균 평점", f"{avg_rating:.2f}")
    
    with col3:
        if 'product' in df.columns:
            unique_products = df['product'].nunique()
            st.metric("제품 수", unique_products)
    
    with col4:
        if 'category' in df.columns:
            unique_categories = df['category'].nunique()
            st.metric("카테고리 수", unique_categories)
    
    # 감성 분석
    st.subheader("😊 감성 분석")
    
    if 'feedback_text' in df.columns:
        # 감성 분석 실행
        df['sentiment'] = df['feedback_text'].apply(analyze_sentiment)
        
        # 감성 분포 시각화
        sentiment_counts = df['sentiment'].value_counts()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_pie = px.pie(
                values=sentiment_counts.values,
                names=sentiment_counts.index,
                title="감성 분포",
                color_discrete_map={'긍정': '#2E8B57', '중립': '#FFD700', '부정': '#DC143C'}
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            fig_bar = px.bar(
                x=sentiment_counts.index,
                y=sentiment_counts.values,
                title="감성별 피드백 수",
                color=sentiment_counts.index,
                color_discrete_map={'긍정': '#2E8B57', '중립': '#FFD700', '부정': '#DC143C'}
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # 감성별 상세 분석
        st.subheader("감성별 상세 분석")
        sentiment_filter = st.selectbox("감성 선택", ['전체'] + list(sentiment_counts.index))
        
        if sentiment_filter == '전체':
            filtered_df = df
        else:
            filtered_df = df[df['sentiment'] == sentiment_filter]
        
        st.dataframe(filtered_df[['feedback_text', 'sentiment', 'rating']], use_container_width=True)
    
    # 키워드 분석
    st.subheader("🔍 키워드 분석")
    
    if 'feedback_text' in df.columns:
        # 키워드 추출
        keywords = extract_keywords(df['feedback_text'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 상위 키워드 차트
            if keywords:
                fig_keywords = px.bar(
                    x=list(keywords.values()),
                    y=list(keywords.keys()),
                    orientation='h',
                    title="상위 키워드 빈도",
                    labels={'x': '빈도', 'y': '키워드'}
                )
                st.plotly_chart(fig_keywords, use_container_width=True)
        
        with col2:
            # 워드클라우드
            if keywords:
                st.write("**키워드 워드클라우드**")
                create_wordcloud(keywords)
    
    # 제품별 분석
    if 'product' in df.columns:
        st.subheader("📱 제품별 분석")
        
        product_analysis = df.groupby('product').agg({
            'rating': ['mean', 'count'],
            'sentiment': lambda x: (x == '긍정').sum() / len(x) * 100
        }).round(2)
        
        product_analysis.columns = ['평균 평점', '피드백 수', '긍정 비율(%)']
        st.dataframe(product_analysis, use_container_width=True)
        
        # 제품별 평점 비교
        if 'rating' in df.columns:
            fig_product_rating = px.box(
                df, 
                x='product', 
                y='rating',
                title="제품별 평점 분포"
            )
            st.plotly_chart(fig_product_rating, use_container_width=True)
    
    # 카테고리별 분석
    if 'category' in df.columns:
        st.subheader("🏷️ 카테고리별 분석")
        
        category_analysis = df.groupby('category').agg({
            'rating': ['mean', 'count'],
            'sentiment': lambda x: (x == '긍정').sum() / len(x) * 100
        }).round(2)
        
        category_analysis.columns = ['평균 평점', '피드백 수', '긍정 비율(%)']
        st.dataframe(category_analysis, use_container_width=True)
    
    # 시간별 분석 (날짜가 있는 경우)
    if 'date' in df.columns:
        st.subheader("📅 시간별 분석")
        
        try:
            df['date'] = pd.to_datetime(df['date'])
            df['month'] = df['date'].dt.to_period('M')
            
            monthly_sentiment = df.groupby('month')['sentiment'].apply(
                lambda x: (x == '긍정').sum() / len(x) * 100
            ).reset_index()
            monthly_sentiment['month'] = monthly_sentiment['month'].astype(str)
            
            fig_trend = px.line(
                monthly_sentiment,
                x='month',
                y='sentiment',
                title="월별 긍정 비율 추이",
                labels={'sentiment': '긍정 비율(%)', 'month': '월'}
            )
            st.plotly_chart(fig_trend, use_container_width=True)
            
        except Exception as e:
            st.warning(f"날짜 분석 중 오류가 발생했습니다: {str(e)}")
    
    # 필터링 옵션
    st.subheader("🔍 고급 필터링")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'product' in df.columns:
            selected_products = st.multiselect(
                "제품 선택",
                options=df['product'].unique(),
                default=df['product'].unique()
            )
        
        if 'category' in df.columns:
            selected_categories = st.multiselect(
                "카테고리 선택",
                options=df['category'].unique(),
                default=df['category'].unique()
            )
    
    with col2:
        if 'rating' in df.columns:
            rating_range = st.slider(
                "평점 범위",
                min_value=int(df['rating'].min()),
                max_value=int(df['rating'].max()),
                value=(int(df['rating'].min()), int(df['rating'].max()))
            )
        
        if 'sentiment' in df.columns:
            selected_sentiments = st.multiselect(
                "감성 선택",
                options=df['sentiment'].unique(),
                default=df['sentiment'].unique()
            )
    
    # 필터링된 데이터 표시
    filtered_data = df.copy()
    
    if 'product' in df.columns and selected_products:
        filtered_data = filtered_data[filtered_data['product'].isin(selected_products)]
    
    if 'category' in df.columns and selected_categories:
        filtered_data = filtered_data[filtered_data['category'].isin(selected_categories)]
    
    if 'rating' in df.columns:
        filtered_data = filtered_data[
            (filtered_data['rating'] >= rating_range[0]) & 
            (filtered_data['rating'] <= rating_range[1])
        ]
    
    if 'sentiment' in df.columns and selected_sentiments:
        filtered_data = filtered_data[filtered_data['sentiment'].isin(selected_sentiments)]
    
    st.subheader(f"📊 필터링된 결과 ({len(filtered_data)}개)")
    st.dataframe(filtered_data, use_container_width=True)
    
    # 데이터 다운로드
    st.subheader("💾 데이터 다운로드")
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv = filtered_data.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="CSV 다운로드",
            data=csv,
            file_name="filtered_feedback_data.csv",
            mime="text/csv"
        )
    
    with col2:
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            filtered_data.to_excel(writer, index=False, sheet_name='Feedback Data')
        excel_data = excel_buffer.getvalue()
        
        st.download_button(
            label="Excel 다운로드",
            data=excel_data,
            file_name="filtered_feedback_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if __name__ == "__main__":
    main()
