from dotenv import load_dotenv
import streamlit as st
import requests
import os

load_dotenv()

if "isopen" not in st.session_state:
    st.session_state.isopen = False

if not st.session_state.isopen:
    st.title("비밀번호")

    a = st.text_input("비밀번호를 입력하시오")

    if a == "5178579":
        st.session_state.isopen = True
        st.rerun()

    if a:
        st.error("잘못된 비밀번호입니다.")

else:
    API_URL = os.getenv("API_URL")
    API_KEY = os.getenv("API_KEY")
    prompt = os.getenv("prompt")
        
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
            {"role": "system", "content": prompt}
        ]
    
    st.title("챗봇")
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
    
        with st.spinner("줮까세요 싶팔"):
            response = requests.post(API_URL, headers=headers, json=payload)
            if response.status_code == 200:
                reply = response.json()["choices"][0]["message"]["content"]
            else:
                reply = "오류 발생"
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()
    else:
        render_messages(st.session_state.messages)
