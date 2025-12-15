import google.generativeai as genai

# Configure the Gemini API key
genai.configure(api_key="AIzaSyBA6UJcbf3DSrHLtePYJPv6sASctt0pA_s")

def generate_from_llm(prompt, instructions):
    """
    Generates a quiz from the given prompt using the configured LLM.
    """
    full_prompt = f"{instructions}\n\n{prompt}"
    return call_gemini(full_prompt)


def call_gemini(full_prompt):
    """
    Calls the Gemini API to generate a quiz from the given prompt.
    """
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(full_prompt)

        return response.text.strip()
    except Exception as e:
        print(f"❌ An error occurred while calling the Gemini API: {e}")
        # Fallback to a simple error message
        return f"# Error Generating Quiz\n\nCould not generate the quiz. Please check your API key and the model's response.\n\n**Error details:** {e}"
