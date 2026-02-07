from utils.templates import make_volumes_list_text, make_volume_text
from config import dclient

from telegram import Update
from telegram.ext import ContextTypes as Context


async def volumes_command(update: Update, context: Context.DEFAULT_TYPE):
    message = update.message

    await message.reply_text(make_volumes_list_text(), parse_mode='html')


async def get_volume_command(update: Update, context: Context.DEFAULT_TYPE):
    message = update.message

    dashes = list(map(int, message.text[-3 - int(message.text[-1]):-3]))

    periods_offset = -3 - int(message.text[-1])
    periods = list(map(int, message.text[periods_offset - int(message.text[-2]):periods_offset]))

    underscores_offset = periods_offset - int(message.text[-2])
    underscores = list(map(int, message.text[underscores_offset - int(message.text[-3]):underscores_offset]))

    volume_id = message.text[2:underscores_offset - int(message.text[-3])]
    for char_id, index_list in enumerate([underscores, periods, dashes]):
        for i in index_list:
            volume_id = volume_id[:i] + ['_', '.', '-'][char_id] + volume_id[i:]

    volume = [vol for vol in dclient.volumes.list() if vol.short_id == volume_id][0]
    await message.reply_text(make_volume_text(volume), parse_mode='html')
