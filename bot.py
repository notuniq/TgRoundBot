import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from moviepy.editor import VideoFileClip
import random
import logging
import tempfile
import crop_video
import config

bot = Bot(token=config.bot_token)
logging.basicConfig(level=logging.INFO)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Привет! Отправь мне квадратное видео, и я сделаю его круглым.")
    
@dp.message_handler(content_types=["video"])
async def convert(message: types.Message):
    response = await message.answer("Получил ваше видео, превращаю его в круглое видео! Пожалуйста, подождите...")
    downloads_dir = 'downloads'
    os.makedirs(downloads_dir, exist_ok=True)

    with tempfile.NamedTemporaryFile(suffix='.mp4', dir=downloads_dir, delete=False) as video_tmp:
        await bot.download_file_by_id(message.video.file_id, video_tmp.name)
        video_path = video_tmp.name

    with tempfile.NamedTemporaryFile(suffix='.mp4', dir=downloads_dir, delete=False) as out_video_tmp:
        out_video_path = out_video_tmp.name

    video_clip = VideoFileClip(video_path)
    if video_clip.duration > 60:
        await response.edit_text('Длительность видео должна быть не больше 1 минуты!')
    else:
        size, duration = crop_video.video_crop(video_path, out_video_path)

        with open(out_video_path, 'rb') as out_video_file:
            answer = await message.answer_video_note(
                video_note=out_video_file.read(),
                duration=duration
            )

        if not answer:
            await response.edit_text("Не получилось сконвертировать видео, попробуйте снова!")
        else:
            await response.delete()
    
    os.remove(video_path)
    os.remove(out_video_path)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
