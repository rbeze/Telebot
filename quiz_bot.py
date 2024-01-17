import json
import time
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

class QuizBot:
    def __init__(self, token):
        self.bot = telepot.Bot(token)
        self.quiz_questions = [
            {
                "question": "What is THE most popular programming language in the world?",
                "options": ["Python", "Javascript/Typescript", "HTML/CSS", "GO", "NOTA"],
                "correct_option": "NOTA"
            },
            {
                "question": "What does HTML stand for?",
                "options": ["Hyper Training Marking Language", "Hyper Text Marketing Language", "Hyper Text Markup Language", "Hyper Text Markup Leveler", "NOTA"],
                "correct_option": "Hyper Text Markup Language"
            },
            {
                "question": "What are two types of network layer firewalls?",
                "options": ["Stateful and stateless", "Dynamic and static", "Anomaly and signature", "Mandatory and discretionary", "NOTA"],
                "correct_option": "Stateful and stateless"
            },
            {
                "question": "Which of the following attacks requires a carrier file to self-replicate?",
                "options": ["Trojan", "Virus", "Worm", "Spam", "NOTA"],
                "correct_option": "Virus"
            },
            {
                "question": "Which of the following offers the strongest wireless signal encryption?",
                "options": ["WEP", "WAP", "WIPS", "WPA"],
                "correct_option": "WPA"
            }
            # Add more quiz questions as needed
        ]
        self.current_question_index = 0

    def start_quiz(self, chat_id):
        self.bot.sendMessage(chat_id, "Welcome to the Programming & Cyber Security Quiz!")
        self.send_question(chat_id)

    def send_question(self, chat_id):
        if self.current_question_index < len(self.quiz_questions):
            question_data = self.quiz_questions[self.current_question_index]
            question_text = question_data["question"]
            options = question_data["options"]

            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=option, callback_data=option)] for option in options
            ])

            self.bot.sendMessage(chat_id, f'{question_text}\nChoose the correct option:', reply_markup=keyboard)
        #else:

    def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        correct_option = self.quiz_questions[self.current_question_index]["correct_option"]

        if query_data == correct_option:
            response_text = "Correct answer! 🎉"
        else:
            response_text = f"Sorry, the correct answer is {correct_option}."

        self.bot.answerCallbackQuery(query_id, text=response_text)

        # Move to the next question
        if self.current_question_index < len(self.quiz_questions)-1:
            self.current_question_index += 1
            self.send_question(from_id)
        else:
            self.bot.sendMessage(from_id, "No more questions available. Quiz completed.")

    def on_chat_message(self, msg):
        content_type, _, chat_id = telepot.glance(msg)

        if content_type == 'text' and '/startquiz' in msg['text'].lower():
            self.start_quiz(chat_id)

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
with open("tokens.json", "r") as f:
    bot_token = json.load(f)["telegram_token"]
    bot_instance = QuizBot(bot_token)

    bot_instance.bot.message_loop({'chat': bot_instance.on_chat_message, 'callback_query': bot_instance.on_callback_query})

print('Bot is listening...')

# Keep the program running
while 1:
    time.sleep(10)