import streamlit as st
import sqlite3
import g4f
import datetime

from g4f.Provider import (
    Bard,
    Bing,
    HuggingChat,
    OpenAssistant,
    OpenaiChat,
)

providers = {"Bing": Bing, "OpenAssistant": OpenAssistant}
models = {"g4f.models.default": g4f.models.default, "gpt-3.5-turbo": "gpt-3.5-turbo"}

g4f.debug.logging = True  # enable logging
g4f.check_version = False  # Disable automatic version checking

# Создание базы данных
conn = sqlite3.connect('test3.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS history
             (date text, role text, content text)''')

# Загрузка истории сообщений из базы данных
c.execute("SELECT * FROM history")
message_history = [{"date": row[0], "role": row[1], "content": row[2]} for row in c.fetchall()]

if message_history:
    prompt = message_history[0]["content"]
else:
    prompt = "Привет"

# Streamlit interface
st.title("Почти Рабочий v2.3")
prompt = st.text_input("Enter your prompt: ", prompt)
#role = st.text_input("Enter the role (leave blank for default): ")
#role_default = st.selectbox("Select from default roles: ", ["professional", "assistant", "psychologist"])
model_name = st.selectbox("Select an available model: ", list(models.keys()))
#provider_name = st.selectbox("Select a provider: ", list(providers.keys()))
#provider = providers[provider_name]
model = models[model_name]

if st.button("Submit"):
    # Получение текущей даты и времени
    current_time = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    #if len(role) == 0:
        #role = role_default

    new_message = {"date": current_time, "role": "user", "content": prompt}
    message_history.append(new_message)

    # Создание запроса с использованием истории сообщений
    response = g4f.ChatCompletion.create(
        model=model,
        provider=Bing,
        messages=message_history,
        stream=True
    )

    print(type(response))

    message = ""

    for letters in response:
        message += letters
    st.write(message)
    message_info = {"date": current_time, "role": "user", "content": message}
    message_history.append(message_info)
    c.execute("INSERT INTO history VALUES (?, ?, ?)", (message_info['date'], message_info['role'], message))
    conn.commit()
    conn.close()
