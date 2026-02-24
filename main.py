import streamlit as st
from google import genai

# 1. 페이지 설정 및 디자인
st.set_page_config(page_title="AI 튜터 뉴턴", page_icon="🍎", layout="centered")
st.title("🍎 과학 전문 AI 튜터 '뉴턴'")
st.markdown("---")
st.info("안녕하세요! 저는 과학을 사랑하는 뉴턴 선생님이에요. 궁금한 것이 있다면 무엇이든 물어보세요!")

# ---------------------------------------------------------
# [핵심] 'Create API key in new project'로 만든 새 키를 넣으세요!
# ---------------------------------------------------------
API_KEY = "AIzaSyDoqIexHHHjWNL9QR1yci3SMavjHUXax58"

# 클라이언트 설정 (에러 방지를 위해 v1 버전 명시)
try:
    client = genai.Client(api_key=API_KEY, http_options={'api_version': 'v1'})
except Exception as e:
    st.error(f"연결 설정 중 오류가 발생했어요: {e}")

# 2. 뉴턴의 교육 페르소나 (지침)
instruction = """너는 초중고 과학 전문 교사 AI 튜터 '뉴턴'이야.
1. 학생의 답변에 상관없이 항상 따뜻한 격려로 대화를 시작해줘.
2. 정답을 바로 가르쳐주지 말고, 비유를 들어서 스스로 생각하게 유도해줘.
3. 마지막엔 항상 학생의 호기심을 자극하는 질문을 하나 던져줘.
예: '빛이 굴절되는 걸 본 적이 있니? 컵 속의 빨대가 꺾여 보이는 것도 같은 원리란다. 왜 그럴까?'"""

# 3. 채팅 대화 기록 관리
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 대화 내용 화면에 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. 사용자 입력창 및 AI 답변 생성
if prompt := st.chat_input("오늘 배운 과학 중 궁금한 게 있나요?"):
    # 사용자 메시지 저장
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 뉴턴의 답변 생성
    try:
        # 모델 경로를 명확히 하고 지침과 질문을 합쳐서 보냅니다.
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=f"지침: {instruction}\n\n학생 질문: {prompt}"
        )
        
        # 답변 출력 및 저장
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
    except Exception as e:
        # 404 에러가 날 경우를 대비한 친절한 안내
        st.error(f"뉴턴 선생님과 연결이 잠시 끊겼어요. (에러: {e})")
        if "404" in str(e):
            st.warning("팁: API 키를 'New Project'에서 새로 발급받았는지 확인해보세요!")
