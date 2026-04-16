import streamlit as st
import easyocr
from PIL import Image
import numpy as np

# Инициализация OCR (загружается один раз)
@st.cache_resource
def load_ocr():
    reader = easyocr.Reader(['ru', 'en'], gpu=False)
    return reader

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
                reader = load_ocr()
                
                # Конвертируем PIL в numpy
                img_np = np.array(image)
                
                # Распознаем текст
                result = reader.readtext(img_np, detail=0)
                text = ' '.join(result)
                text_len = len(text.strip())
                prob_1 = 1 - min(text_len / 100, 1.0)

                if prob_1 > 0.5:
                    result_text = "Класс 1 (релевантное) ✅"
                else:
                    result_text = "Класс 0 (нерелевантное) ❌"

            st.write(f"**{result_text}**")
            st.metric("Вероятность класса 1", f"{prob_1:.2%}")
            
            if text_len > 0:
                with st.expander("📝 Распознанный текст"):
                    st.write(text[:500])

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; padding: 20px;'>
        🚀 Сайт сделан командой <b>SlavickTeam</b>
    </div>
    """,
    unsafe_allow_html=True
)
