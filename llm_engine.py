import google.generativeai as genai

genai.configure(api_key="")

model = genai.GenerativeModel("gemini-3-flash-preview")

def generate_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ AI quota exceeded or error occurred.\n\nFallback insight:\n{basic_fallback(prompt)}"


def basic_fallback(prompt):
    return "This match showed strong momentum shifts and key performances influenced the outcome."
