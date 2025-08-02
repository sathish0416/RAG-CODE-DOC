# ask.py

from rag_gemini import generate_answer

while True:
    user_input = input("\nAsk a question (or type 'exit'): ")
    if user_input.lower() == "exit":
        break

    answer = generate_answer(user_input)
    print(f"\n[ANSWER]\n{answer}")
