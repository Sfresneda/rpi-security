# -*- coding: utf-8 -*-

import logging
import os
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
import _thread

from rpisec.enumerations import Actions
from rpisec.enumerations import TextChains

logging.getLogger("telegram").setLevel(logging.ERROR)
logger = logging.getLogger()


def telegram_bot(rpis, camera):
    """
    This function runs the telegram bot that responds to commands like /enable, /disable or /status.
    """
    def save_chat_id(update, context):
        if 'telegram_chat_ids' not in rpis.saved_data or rpis.saved_data['telegram_chat_ids'] is None:
            rpis.save_telegram_chat_id(update.message.chat_id)
            logger.debug('Set Telegram chat_id {0}'.format(update.message.chat_id))
        else:
            if len(rpis.saved_data['telegram_chat_ids']) < rpis.telegram_users_number:
                if update.message.chat_id not in rpis.saved_data['telegram_chat_ids']:
                    rpis.save_telegram_chat_id(update.message.chat_id)
                    logger.debug('Set Telegram chat_id {0}'.format(update.message.chat_id))

    def debug(update, context):
        logger.debug('Received Telegram bot message: {0}'.format(update.message.text))

    def check_chat_id(update):
        if 'telegram_chat_ids' in rpis.saved_data and update.message.chat_id \
                not in rpis.saved_data['telegram_chat_ids']:
            logger.debug('Ignoring Telegram update with filtered chat id {0}: {1}'.format(update.message.chat_id,
                                                                                          update.message.text))
            return False
        else:
            return True

    def show_help(update, context):
        if check_chat_id(update):
            result = ""
            for action in Actions:
                action_text = Actions.text_for_action(action)
                if 0 < len(action_text):
                    result += action_text + "\n"

            update.message.reply_text(parse_mode='Markdown', text=result,
                                      timeout=10)

    def status(update, context):
        if check_chat_id(update):
            update.message.reply_text(parse_mode='Markdown', text=rpis.state.generate_status_text(), timeout=10)

    def disable(update, context):
        if check_chat_id(update):
            rpis.state.update_state('disabled')

    def enable(update, context):
        if check_chat_id(update):
            rpis.state.update_state('disarmed')

    def photo(update, context):
        if check_chat_id(update):
            update.message.reply_text(parse_mode='Markdown', text=TextChains.CR_TAKING_PHOTO.value, timeout=10)
            photo_file = camera.take_photo()
            rpis.telegram_send_file(photo_file)

    def gif(update, context):
        if check_chat_id(update):
            update.message.reply_text(parse_mode='Markdown', text=TextChains.CR_RECORDING_GIF.value, timeout=10)
            gif_file = camera.take_gif()
            rpis.telegram_send_file(gif_file)

    def reboot(update, context):
        update.message.reply_text(parse_mode='Markdown', text=TextChains.CR_REBOOTING_SYSTEM.value, timeout=10)
        logger.info('Rebooting after receiving reboot command')
        os.system('reboot')

    def error_callback(update, context):
        logger.error('Update "{0}" caused error "{1}"'.format(update, context.error))

    try:
        updater = Updater(rpis.telegram_bot_token, use_context=True)
        dp = updater.dispatcher
        dp.add_handler(MessageHandler(Filters.regex('.*'), save_chat_id), group=1)
        dp.add_handler(MessageHandler(Filters.regex('.*'), debug), group=2)
        for action in Actions:
            associated_action = {
                Actions.STATUS: status,
                Actions.HELP: show_help,
                Actions.DISABLE: disable,
                Actions.ENABLE: enable,
                Actions.PHOTO: photo,
                Actions.GIF: gif,
                Actions.REBOOT: reboot
            }.get(action, show_help)
            dp.add_handler(CommandHandler(action.value, associated_action), group=3)

        dp.add_error_handler(error_callback)
        updater.start_polling(timeout=10)
    except Exception as e:
        logger.error('Telegram Updater failed to start with error {0}'.format(repr(e)))
        _thread.interrupt_main()
    else:
        logger.info("thread running")
