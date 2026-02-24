import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정
st.set_page_config(page_title="AI 튜터 뉴턴", page_icon="🍎")
st.header("🍎 과학 전문 AI 튜터 '뉴턴'")

# 2. API 설정 (중요: Client 대신 configure를 씁니다)
API_KEY = "AIzaSyDoqIexHHHjWNL9QR1yci3SMavjHUXax58" 
genai.configure(api_key=API_KEY)

# 3. 뉴턴의 교육 페르소나
instruction = """너는 초중고 과학 전문 교사 AI 튜터 '뉴턴'이야.
- 따뜻하게 격려하며 대화를 시작해줘.
- 비유를 통해 스스로 생각하게 유도해줘.
- 마지막엔 호기심을 자극하는 질문을 던져줘."""

# 4. 모델 설정 (구형/신형 라이브러리 모두에서 가장 안정적인 호출 방식)
model = genai.GenerativeModel('gemini-1.5-flash')

# 5. 채팅 기록 관리
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. 사용자 입력 및 답변 생성
if prompt := st.chat_input("오늘 배운 과학 중 궁금한 게 있나요?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Client 방식이 아닌 GenerativeModel의 직통 방식을 씁니다.
        full_prompt = f"지침: {instruction}\n\n학생 질문: {prompt}"
        response = model.generate_content(full_prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
    except Exception as e:
        st.error(f"뉴턴 선생님과 연결 중 오류가 발생했어요: {e}")
