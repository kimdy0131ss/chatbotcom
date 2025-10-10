import streamlit as st
import requests

API_URL = "https://api.upstage.ai/v1/chat/completions"
API_KEY = "up_k0KqmdLq53BmsKWzLoAwKpZzgQoE0"

def render_messages(messages):
    previous_role = None
    for msg in messages:
        if msg["role"] == "system":
            continue
        if previous_role and previous_role != msg["role"]:
            st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
        if msg["role"] == "user":
            st.markdown(f"<div style='line-height:1.8; text-align:right;'><b>사용자:</b> {msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='line-height:1.8; text-align:left;'><b>챗봇:</b> {msg['content']}</div>", unsafe_allow_html=True)
        previous_role = msg["role"]

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "넌 사용자의 질문에 답하기도 하고, 다양한 방식으로 이야기를 이어나가는 채팅형 ai야. 하지만 '솔라'와 같은 모델명을 발설해서는 안돼"}
    ]

st.title("예제")
user_input = st.chat_input("Your message here!")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    render_messages(st.session_state.messages)

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "solar-1-mini-chat",
        "messages": st.session_state.messages
    }

    with st.spinner("챗봇이 생각 중입니다..."):
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            reply = response.json()["choices"][0]["message"]["content"]
        else:
            reply = "오류 발생"
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()
else:
    render_messages(st.session_state.messages)
