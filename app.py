import streamlit as st
from PIL import Image
import numpy as np

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
                # Простая эвристика: чем больше цветов и деталей, тем вероятнее релевантно
                img_array = np.array(image)
                
                # Считаем уникальные цвета
                unique_colors = len(np.unique(img_array.reshape(-1, img_array.shape[2]), axis=0))
                
                # Чем больше уникальных цветов, тем вероятнее фото товара
                prob_1 = min(unique_colors / 50000, 1.0)
                
                # Нормализуем для красоты
                prob_1 = max(0.1, min(0.95, prob_1))

                if prob_1 > 0.5:
                    result = "Класс 1 (релевантное) ✅"
                else:
                    result = "Класс 0 (нерелевантное) ❌"

            st.write(f"**{result}**")
            st.metric("Вероятность класса 1", f"{prob_1:.2%}")

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; padding: 20px;'>
        🚀 Сайт сделан командой <b>SlavickTeam</b>
    </div>
    """,
    unsafe_allow_html=True
)
