import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import uvicorn
from threading import Thread

# --- 1. SAZLAWLAR ---
# Render-de "Environment Variables" bólimine qosılatuǵın giltler
API_TOKEN = os.environ.get('BOT_TOKEN', '8582698330:AAFKN6hDY_x2IYIVAv8CrN4oYzFFtdwBE4M')
GEMINI_KEY = os.environ.get('GEMINI_KEY')
# Siziń Vercel yamasa GitHub Pages mánzilińiz
WEB_APP_URL = 'https://muratbek95.github.io/keleshek-portali/' 

# Gemini AI-dı sazlaw
genai.configure(api_key=GEMINI_KEY)
SYSTEM_INSTRUCTION = """
Sen Muratbek Kutlimuratov tárepinen mektep oqıwshıları ushın jaratılǵan AI-Mentor psixologsań.
1. Sır saqlaw: Barlıq maǵlıwmatlar sır saqlanıwın turaqlı eslat.
2. Jıllı qatnas: Qaraqalpak tilinde, jıllı hám motivatsiyalı sóyles.
3. 10 soraw: Oqıwshınıń qábiletin anıqlaw ushın 10 oylandırıwshı soraw ber.
4. Jeke sorawlar: Muratbek haqqında sorasalar, jeke sorawlardı Muratbek aǵanıń ózine jazıwın ayt.
"""
model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=SYSTEM_INSTRUCTION)

# --- 2. BOT BÓLIMI ---
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌟 Keleshekke sapar", web_app=WebAppInfo(url=WEB_APP_URL))]
    ])
    await message.answer(
        f"Assalawma áleykum, {message.from_user.first_name}! 👋\n\n"
        "Men — Muratbek Kutlimuratov tárepinen jaratılǵan AI-Mentorpan.\n"
        "Tómendegi túymeni basıń hám keleshegińizge birge sapar qılayıq. "
        "Barlıq maǵlıwmatlar sır saqlanadı! 🔒",
        reply_markup=markup
    )

# --- 3. API SERVER BÓLIMI (FastAPI) ---
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

chat_sessions = {}

class UserMessage(BaseModel):
    user_id: str
    text: str

@app.post("/ask")
async def ask_ai(data: UserMessage):
    user_id = data.user_id
    if user_id not in chat_sessions:
        chat_sessions[user_id] = model.start_chat(history=[])
    
    try:
        response = chat_sessions[user_id].send_message(data.text)
        return {"reply": response.text}
    except Exception as e:
        return {"reply": "Keshiresiz, texnikalıq qátelik júz berdi. Qaytadan jazıp kórıń."}

# --- 4. ISKE TÜSIRIW (Render-ge sáykeslestirilgen) ---
def run_api():
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

async def run_bot():
    await dp.start_polling(bot)

if __name__ == "__main__":
    Thread(target=run_api).start()
    asyncio.run(run_bot())
