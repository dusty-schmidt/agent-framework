from zai import ZaiClient

# Initialize client
client = ZaiClient(api_key="284423fbd71c4c90a314d24f7768792e.lwWcSmfTEqe7oaA4")

# Create chat completion request
response = client.chat.completions.create(
    model="glm-4.5",
    messages=[
        {
            "role": "system",
            "content": "you are a helpful assistant"
        },
        {
            "role": "user",
            "content": "Hello, please introduce yourself."
        }
    ],
    temperature=0.7,
    top_p=0.8
)

# Get response
print(response.choices[0].message.content)
