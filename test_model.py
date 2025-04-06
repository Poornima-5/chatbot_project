import google.generativeai as genai

genai.configure(api_key="AIzaSyA0UddCrV6RzX3pe0b5OSi0biwo1YwgK18")

# List available models
for m in genai.list_models():
    print(m.name)
