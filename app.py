import subprocess
import sys

# Установка Tesseract (только если не установлен)
try:
    subprocess.run(['tesseract', '--version'], capture_output=True, check=True)
except:
    subprocess.run(['apt-get', 'update'], check=True)
    subprocess.run(['apt-get', 'install', '-y', 'tesseract-ocr', 'tesseract-ocr-rus'], check=True)
    print("Tesseract установлен!")

import streamlit as st
import pytesseract
from PIL import Image
import os
# Путь к Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

st.set_page_config(page_title="Классификатор изображений", page_icon="📷")

st.title("📷 Классификатор изображений")
st.write("Загрузите фото для классификации")

uploaded_file = st.file_uploader("Выберите картинку...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.write(f"**{uploaded_file.name}**")
    image = Image.open(uploaded_file)

    st.write("## Фото загружено")

    col1, col2 = st.columns(2)

    with col1:
        st.image(image, caption="Ваше фото", use_container_width=True)

    with col2:
        st.write("### Результат анализа")

        if st.button("Классифицировать"):
            with st.spinner("Анализируем..."):
                text = pytesseract.image_to_string(image, lang='rus+eng')
                text_len = len(text.strip())
                prob_1 = 1 - min(text_len / 100, 1.0)

                # Простая классификация
                if prob_1 > 0.5:
                    result = "Класс 1 (релевантное) ✅"
                else:
                    result = "Класс 0 (нерелевантное) ❌"

            st.write(f"**{result}**")
            st.metric("Вероятность класса 1", f"{prob_1:.2%}")

# Подпись внизу
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; padding: 20px;'>
        🚀 Сайт сделан командой <b>SlavickTeam</b>
    </div>
    """,
    unsafe_allow_html=True
)
