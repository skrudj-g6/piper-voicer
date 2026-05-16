import asyncio
import subprocess
import uuid
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart

TOKEN = "8679908051:AAFKMKskfQZcGq4yXnh0GT1SwtyCYB64Edc"

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Отправь текст, и я озвучу его."
    )


@dp.message(F.text)
async def tts_handler(message: Message):

    text = message.text
    wav_file = f"{uuid.uuid4()}.wav"

    # запуск Piper
    process = subprocess.run(
        [
            "piper.exe",
            "--model",
            "ru_RU-irina-medium.onnx",
            "--output_file",
            wav_file
        ],
        input=text,
        text=True,
        encoding="utf-8",
        capture_output=True
    )

    # если ошибка
    if process.returncode != 0:
        await message.answer(
            f"Ошибка Piper:\n{process.stderr}"
        )
        return

    # проверяем что файл создался
    if not os.path.exists(wav_file):
        await message.answer("WAV файл не был создан")
        return

    voice_file = FSInputFile(wav_file)

    await message.answer_voice(
        voice=voice_file
    )

    # удаляем wav
    os.remove(wav_file)


async def main():
    print("BOT STARTED")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())