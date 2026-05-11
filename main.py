import os
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

# --- GILTILER ---
API_TOKEN = '8787083971:AAE-ottTgfjZpc2fSQscV5TFHlH10ESG1io' 
GEMINI_KEY = 'AIzaSyCDKNiUkPq3oy_WjisMaxXh54mO8ORf6Ls' 
WEB_APP_URL = 'https://Muratbek95.github.io/keleshek-portali/'

# Gemini sazlawı (DURISLANǴAN MODEL ATAMASI)
genai.configure(api_key=GEMINI_KEY)
# Kóp jaǵdayda lokal sistemalarda 'models/' prefiksi kerek boladı
model = genai.GenerativeModel("models/gemini-1.5-flash")

# FastAPI sazlawı
app = FastAPI()
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"]
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
        # AI-ǵa soraw jiberiw
        response = model.generate_content(data.text)
        return {"reply": response.text}
    except Exception as e:
        # Qáteliklerdi anıqlaw (mısalı: API limit yamasa model atı)
        print(f"Gemini qáteligi: {str(e)}")
        return {"reply": f"AI juvap bere almadı. Serverdegi qátelik: {str(e)}"}

# Telegram Bot
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌟 Keleshekke sapar", web_app=WebAppInfo(url=WEB_APP_URL))]
    ])
    await message.answer("Sálem! Lokal serverdegi AI-Mentorǵa xosh kelipsiz.", reply_markup=markup)

def run_api():
    # Uvicorn serverin baslaw
    uvicorn.run(app, host="0.0.0.0", port=7860)

async def main_async():
    # Veb-serverdi bólek potokta baslaw
    api_thread = Thread(target=run_api, daemon=True)
    api_thread.start()
    print("Server http://localhost:7860 mánzilinde baslandı")
    print("Ngrok tuneli arqalı baylanıstı tekseriń!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main_async())
    except (KeyboardInterrupt, SystemExit):
        print("Bot toqtatıldı")
