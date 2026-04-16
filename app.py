import streamlit as st
import torch
import clip
from PIL import Image

device = "cuda" if torch.cuda.is_available() else "cpu"


@st.cache_resource
def load_model():
    model, preprocess = clip.load("ViT-B/32", device=device)
    model.eval()
    return model, preprocess


st.title("Классификатор изображений")
st.write("Загрузите фото для классификации")

uploaded_file = st.file_uploader("Выберите картинку...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Ваше фото", use_container_width=True)

    if st.button("Классифицировать"):
        model, preprocess = load_model()

        with st.spinner("Анализируем..."):
            image_input = preprocess(image).unsqueeze(0).to(device)

            # Варианты описаний изображений
            descriptions = [
                "кресло-качалка",
                "кот на кресле",
                "кошка",
                "стул",
                "диван",
                "животное"
            ]

            text = torch.cat([clip.tokenize(f"это {desc}") for desc in descriptions]).to(device)

            with torch.no_grad():
                image_features = model.encode_image(image_input)
                text_features = model.encode_text(text)

                image_features = image_features / image_features.norm(dim=-1, keepdim=True)
                text_features = text_features / text_features.norm(dim=-1, keepdim=True)

                similarity = (image_features @ text_features.T).squeeze(0)
                probs = similarity.softmax(dim=0).cpu().numpy()

            best_idx = probs.argmax()
            best_desc = descriptions[best_idx]
            best_prob = probs[best_idx]

        st.success(f"### 🖼️ Это **{best_desc}**")
        st.metric("Вероятность", f"{best_prob:.1%}")

        # Показываем топ-3 варианта
        with st.expander("Другие варианты"):
            for i in range(len(descriptions)):
                if i != best_idx:
                    st.write(f"- {descriptions[i]}: {probs[i]:.1%}")

st.markdown("---")
st.markdown("<div style='text-align: center;'>🚀 Сайт сделан командой SlavickTeam</div>", unsafe_allow_html=True)