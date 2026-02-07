from utils.templates import make_images_list_text, make_image_text
from config import dclient

from telegram import Update
from telegram.ext import ContextTypes as Context


async def images_command(update: Update, context: Context.DEFAULT_TYPE):
    message = update.message

    await message.reply_text(make_images_list_text(), parse_mode='html')


async def get_image_command(update: Update, context: Context.DEFAULT_TYPE):
    message = update.message
    image = dclient.images.get(message.text[2:])

    await message.reply_text(make_image_text(image), parse_mode='html')
