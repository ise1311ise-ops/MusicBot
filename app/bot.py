import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext

from .config import settings
from .keyboards import main_kb
from .state import GenState
from .jobs import run_job, cancel, jobs, Job

async def start(m: Message, s: FSMContext):
    await s.clear()
    await m.answer(
        "🎵 Я создаю трек (текст + вокал + mp3).\nНажми 💬 Чат",
        reply_markup=main_kb,
    )

async def chat(m: Message, s: FSMContext):
    await s.set_state(GenState.waiting_prompt)
    await m.answer("Опиши песню:")

async def stop(m: Message):
    cancel(m.from_user.id)
    await m.answer("⛔ Остановлено")

async def sound(m: Message):
    job = jobs.get(m.from_user.id)
    if not job or not job.file:
        await m.answer("Нет готового трека")
        return
    await m.answer_audio(FSInputFile(job.file))

async def prompt(m: Message, s: FSMContext):
    await s.clear()
    await m.answer("🎶 Генерирую трек…")
    task = asyncio.create_task(run_job(m.from_user.id, m.text))
    jobs[m.from_user.id] = Job(id="x", task=task)
    try:
        path = await task
        jobs[m.from_user.id].file = path
        await m.answer("✅ Готово! Жми 🔔 Звук")
    except asyncio.CancelledError:
        await m.answer("⛔ Отменено")

def main():
    bot = Bot(settings.bot_token)
    dp = Dispatcher()
    dp.message.register(start, CommandStart())
    dp.message.register(chat, F.text == "💬 Чат")
    dp.message.register(sound, F.text == "🔔 Звук")
    dp.message.register(stop, F.text == "⛔ Стоп")
    dp.message.register(prompt, GenState.waiting_prompt)
    dp.run_polling(bot)

if __name__ == "__main__":
    main()
