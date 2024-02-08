from aiogram import Bot, F, Router
from aiogram.types import Message


HIGHEST_RESOL_INDEX = -1

router = Router()


@router.message(F.photo)
async def get_photo(message: Message, bot: Bot):
    file = await bot.get_file(message.photo[HIGHEST_RESOL_INDEX].file_id)
    await bot.download_file(file.file_path, "saving images/image.jpg")
    await message.answer("Image saved")
