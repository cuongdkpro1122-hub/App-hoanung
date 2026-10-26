import os
import streamlit as st
from google import genai

# Thiết lập giao diện Web
st.set_page_config(page_title="Trợ lý Gemini", page_icon="🤖")
st.title("Ứng dụng AI tích hợp Google Search")

# Ô nhập API Key
api_key_input = st.text_input("Nhập Gemini API Key:", type="password")
api_key = api_key_input if api_key_input else os.environ.get("GEMINI_API_KEY")

# Ô nhập yêu cầu
user_input = st.text_area("Nhập yêu cầu của bạn:", placeholder="Ví dụ: Tìm kiếm thông tin về thời tiết hôm nay...")

# Xử lý khi bấm nút
if st.button("Gửi yêu cầu"):
    if not api_key:
        st.error("Vui lòng nhập API Key để sử dụng.")
    elif not user_input:
        st.warning("Vui lòng nhập yêu cầu.")
    else:
        with st.spinner("AI đang suy nghĩ và tìm kiếm..."):
            try:
                client = genai.Client(api_key=api_key)
                tools = [{'type': 'google_search'}]
                generation_config = {
                    'max_output_tokens': 65536,
                    'thinking_level': 'high',
                }
                
                interaction = client.interactions.create(
                    model='models/gemini-3.8-flash',
                    input=user_input,
                    tools=tools,
                    generation_config=generation_config,
                )
                
                st.markdown("### Kết quả:")
                st.write(interaction.steps[-1])
                
            except Exception as e:
                st.error(f"Có lỗi xảy ra: {e}")