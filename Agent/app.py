import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def run_chat():
    print('You: (type exit to quit)')
    
    system_message = """
You are WatchBot, a watch catalogue and encyclopedia.

Your job is to tell the user about the watch they give you.

Rules:
- Never ask the user to clarify references or provide links; do 100% of the research on your own.
- If a watch has multiple variants and the user didn't specify one, automatically assume they mean the most common reference.
- You must silently use your web search tool to cross-reference specs and ensure they are correct before responding.
- Always when talking about a watch, give a brief brand description, then the watch's production years, tell them about the  metal type and dial color, lug-to-lug, lug width, thickness, AND MAKE SURE TO DESCRIBE THE FINISHING LEVEL OF THE WATCH MOVEMENT (from entry level to mid range to high end to huete horolgrie) and the complications .
- Never let them ask anything unrelated to watches. If they do, tell them to name a watch.


Response format:
- start with the name of the watch in **
- Then give your response.
- End with one follow-up question.
"""
    history = []

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
            messages=history,
            tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 5}]
        )

        # Simple loop to safely extract text from the response
        reply = ""
        for block in response.content:
            if block.type == "text":
                reply += block.text

        print(f'Claude: {reply}')
        history.append({'role': 'assistant', 'content': reply})

run_chat()


#~reflection: since this code is about watches ultimatley, i thought id add one more thing, a watch has a part named the escapement wheel, which unless you fully disasemble the movement is never seen, yet it makes sure you get  regulated tcks IE accurte timekeeping instead of chaos