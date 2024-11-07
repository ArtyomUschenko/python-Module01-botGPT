from g4f.client import Client

client = Client()
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Задаем вопрос тут"}],
    # Add any other necessary parameters
)
print(response.choices[0].message.content)