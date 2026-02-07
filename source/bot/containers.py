from config import dclient, CONFIG, jinja, logger
from utils.templates import make_containers_list_text, make_container_text, make_container_keyboard
from utils.templates import commands_past

from telegram.ext import ContextTypes as Context
from telegram import Update, InlineKeyboardMarkup

from docker.errors import APIError

import html
import i18n


async def containers_command(update: Update, context: Context.DEFAULT_TYPE):
    message = update.message

    await message.reply_text(make_containers_list_text(), parse_mode='html')


async def get_container_command(update: Update, context: Context.DEFAULT_TYPE):
    message = update.message
    container = dclient.containers.get(message.text[2:])

    await message.reply_text(make_container_text(container), parse_mode='html', reply_markup=InlineKeyboardMarkup(
        make_container_keyboard(container)))


async def container_buttons(update: Update, context: Context.DEFAULT_TYPE):
    query = update.callback_query
    container_id = query.data.split('_')[1]
    command = query.data.split('_')[-1]

    if command == 'list':
        await query.edit_message_text(make_containers_list_text())
        await query.answer()
    elif command == 'logs':
        container = dclient.containers.get(container_id)
        response = container.logs().decode()[-CONFIG['logs_character_limit']:]
        await query.message.chat.send_message(jinja.from_string(i18n.t('container_logs')).render(html.escape(response)), parse_mode='html')
        await query.answer(jinja.from_string(i18n.t('container_logs_button_answer')).render(container=container.name))
    else:
        container = dclient.containers.get(container_id)
        try:
            getattr(container, command)()
            logger.info(f'User {query.from_user.id} {commands_past[command]} container {container.name or container.short_id}')
            await query.answer(jinja.from_string(i18n.t('container_action_done')).render(
                name=container.name,
                _id=container.short_id,
                action=commands_past[command]
            ))
        except APIError as e:
            logger.error(str(e.explanation))
            await query.message.chat.send_message(str(e.explanation))
            await query.answer('ERROR!')

        else:
            container.reload()
            await query.edit_message_text(make_container_text(container), parse_mode='html', reply_markup=InlineKeyboardMarkup(
                make_container_keyboard(container)))
