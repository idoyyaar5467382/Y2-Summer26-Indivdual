import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def run_chat():
    print('You: (type exit to quit)')
    system_message = "Your name is Alex. You are a helpful and friendly assistant who helps students learn about technology and computer science. You explain things clearly and always encourage curiosity."
    history = []

    total_input_tokens = 0
    total_output_tokens = 0
    total_cost_cents = 0.0

    INPUT_COST_PER_TOKEN = 0.25 / 1_000_000
    OUTPUT_COST_PER_TOKEN = 1.25 / 1_000_000

    while True:
        user_input = input('>> ')

        if user_input.lower() == 'exit':
            break

        history.append({'role': 'user', 'content': user_input})

        response = client.messages.create(
            model='claude-haiku-4-5-20251001',
            max_tokens=300,
            temperature=0.7,
            system=system_message,
            messages=history
        )

        reply = response.content[0].text
        print(f'\nClaude: {reply}\n')
        history.append({'role': 'assistant', 'content': reply})

        # tgis is bonuss 1
        in_tokens = response.usage.input_tokens
        out_tokens = response.usage.output_tokens
        turn_total = in_tokens + out_tokens

        # this is bonuss 2
        total_input_tokens += in_tokens
        total_output_tokens += out_tokens
        session_total_tokens = total_input_tokens + total_output_tokens

        # this is bonuss 3
        turn_cost_cents = ((in_tokens * INPUT_COST_PER_TOKEN) + (out_tokens * OUTPUT_COST_PER_TOKEN)) * 100
        total_cost_cents += turn_cost_cents

        print("─" * 60)
        print(f"  [This Turn]  In: {in_tokens} | Out: {out_tokens} | Total: {turn_total}")
        print(f"  [Session]    In: {total_input_tokens} | Out: {total_output_tokens} | Total: {session_total_tokens}")
        print(f"  [Est. Cost]  Turn: {turn_cost_cents:.5f}¢ | Session Total: {total_cost_cents:.5f}¢")
        print("─" * 60 + "\n")

if __name__ == '__main__':
    run_chat()


    #the tokens are sort of like how you buy something in a video game for say .99$, and again and again, because hey its under a dollar right? until its 500 dollars
    #1,2,3:
#1: AI gets full chat histry + your new msg. input_tokens jump up every single time.
#2: Bot foregts its own last reply. Token count snowballs because old output becoms new input next  turn.
#3: Nope, no diffrence. Printing is just for your eyes, the code logic works  exactely the same.