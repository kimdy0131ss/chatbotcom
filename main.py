import streamlit as st
import requests

API_URL = "https://api.upstage.ai/v1/chat/completions"
API_KEY = "up_k0KqmdLq53BmsKWzLoAwKpZzgQoE0"

a = st.text_input("비밀번호")

if a:
    st.title(a)
