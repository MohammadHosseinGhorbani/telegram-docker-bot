from utils.templates import make_containers_list_text, make_images_list_text, make_volumes_list_text

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes as Context
import i18n


async def start_command(update: Update, context: Context.DEFAULT_TYPE):
    message = update.message

    await message.reply_text(i18n.t('start_response'), parse_mode='html')


async def menu_command(update: Update, context: Context.DEFAULT_TYPE):
    message = update.message

    await message.reply_text(i18n.t('menu_response'), parse_mode='html', reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton(i18n.t('menu_button_containers'), callback_data='m_containers')],
        [InlineKeyboardButton(i18n.t('menu_button_images'), callback_data='m_images')],
        [InlineKeyboardButton(i18n.t('menu_button_volumes'), callback_data='m_volumes')]
    ]
    ))


async def menu_buttons(update: Update, context: Context.DEFAULT_TYPE):
    query = update.callback_query
    selection = query.data.split('_')[-1]

    match selection:
        case "containers":
            await query.edit_message_text(make_containers_list_text(), parse_mode='html')
        case "images":
            await query.edit_message_text(make_images_list_text(), parse_mode='html')
        case "volumes":
            await query.edit_message_text(make_volumes_list_text(), parse_mode='html')

