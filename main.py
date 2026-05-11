﻿import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import uvicorn
from threading import Thread

# Giltlerdi Hugging Face Secrets-ten alıw
API_TOKEN = os.environ.get('BOT_TOKEN')
GEMINI_KEY = os.environ.get('GEMINI_KEY')
# Siziń GitHub Pages mánzilińiz
WEB_APP_URL = 'https://Muratbek95.github.io/keleshek-portali/'

# Gemini sazlawı
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# FastAPI (Veb-bet ushın)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserMessage(BaseModel):
    user_id: str
    text: str

@app.get("/")
def home():
    return {"status": "AI-Mentor serveri islep tur"}

@app.post("/ask")
async def ask_ai(data: UserMessage):
    try:
        response = model.generate_content(data.text)
        return {"reply": response.text}
    except Exception as e:
        return {"reply": f"Qátelik boldı: {str(e)}"}

# Bot (Telegram ushın)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌟 Keleshekke sapar", web_app=WebAppInfo(url=WEB_APP_URL))]
    ])
    await message.answer("Sálem! Hugging Face serverindegi AI-Mentorǵa xosh kelipsiz.", reply_markup=markup)

def run_api():
    # Hugging Face ushın port turaqlı 7860 bolıwı shart
    uvicorn.run(app, host="0.0.0.0", port=7860)

async def main_async():
    # API-dı bólek potokta iske túsiremiz
    api_thread = Thread(target=run_api, daemon=True)
    api_thread.start()
    # Bottı baslaymız
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main_async())
    except (KeyboardInterrupt, SystemExit):
        print("Bot toqtatıldı")
