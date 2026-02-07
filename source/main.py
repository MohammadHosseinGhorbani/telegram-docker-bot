from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters

from config import logger, CONFIG, prerun
from bot.containers import containers_command, container_buttons, get_container_command
from bot.images import images_command, get_image_command
from bot.volumes import volumes_command, get_volume_command
from bot.general import start_command, menu_command, menu_buttons


if __name__ == '__main__':
    prerun()

    app = Application.builder().token(CONFIG['bot_token']).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('menu', menu_command))
    app.add_handler(CallbackQueryHandler(menu_buttons, '^m'))

    app.add_handler(CommandHandler('containers', containers_command))
    app.add_handler(CallbackQueryHandler(container_buttons, '^c'))
    app.add_handler(MessageHandler(filters.COMMAND & filters.Regex(r'^/c'), get_container_command))

    app.add_handler(CommandHandler('images', images_command))
    app.add_handler(MessageHandler(filters.COMMAND & filters.Regex(r'^/i'), get_image_command))

    app.add_handler(CommandHandler('volumes', volumes_command))
    app.add_handler(MessageHandler(filters.COMMAND & filters.Regex(r'^/v'), get_volume_command))

    logger.info('Starting the bot')
    app.run_polling(drop_pending_updates=True)
