import streamlit as st
import ollama

MODEL_NAME = "llama3" 

st.set_page_config(page_title="AI Интервьюер", page_icon="💼", layout="centered")
st.title("💼 Онлайн-собеседование с AI")
st.write("Локальный симулятор технического интервью на базе Llama 3")

with st.sidebar:
    st.header("⚙️ Настройки вакансии")
    profession = st.text_input("Какую должность тестируем?", value="Python Developer")

    system_prompt = (
        f"Ты — опытный IT-интервьюер. Проводишь собеседование на позицию: {profession}. "
        f"Задавай строго по ОДНОМУ техническому вопросу за раз. Дождись ответа кандидата. "
        f"Не пиши реплики за пользователя. Будь краток и вежлив. Веди диалог на русском языке."
    )
    
    st.markdown("---")
    finish_interview = st.button("🏁 Завершить и получить оценку", type="primary")
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt},
        {"role": "assistant", "content": f"Привет! Я твой интервьюер на сегодня. Давай начнем собеседование на позицию {profession}. Расскажи, пожалуйста, какие основные технологии ты используешь в работе?"}
    ]
for message in st.session_state.messages:
    if message["role"] != "system": # Скрываем от пользователя системную роль
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if not finish_interview:
    if user_input := st.chat_input("Напишите ваш ответ здесь..."):
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("assistant"):
            with st.spinner("Интервьюер слушает и думает..."):
                try:
                    response = ollama.chat(model=MODEL_NAME, messages=st.session_state.messages)
                    ai_response = response['message']['content']
                    st.markdown(ai_response)
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                except Exception as e:
                    st.error(f"Ошибка подключения к Ollama: {e}. Убедитесь, что приложение Ollama запущено.")
else:
    st.markdown("---")
    st.subheader("📊 Анализ вашего собеседования")
    
    with st.spinner("Принимающий анализирует ваши ответы..."):
        eval_messages = st.session_state.messages.copy()
        eval_messages.append({
            "role": "user", 
            "content": "Собеседование окончено. Сделай подробный разбор моих ответов. Укажи, где я ответил правильно, а где ошибся. Напиши правильные варианты для ошибок и поставь итоговую оценку от 1 до 10."
        })
        
        try:
            response = ollama.chat(model=MODEL_NAME, messages=eval_messages)
            st.info(response['message']['content'])
        except Exception as e:
            st.error(f"Не удалось получить оценку: {e}")
        
    if st.button("🔄 Начать новое собеседование"):
        del st.session_state.messages
        st.rerun()
