import logging

# noinspection PyPackageRequirements
from telegram import Update, BotCommand
from telegram.ext import CommandHandler, CallbackContext

from bot.updater import updater
from utils import u
from utils import Permissions
from utils import permissions

logger = logging.getLogger(__name__)


@u.check_permissions(required_permission=Permissions.ADMIN)
@u.failwithmessage
def get_permissions(update: Update, context: CallbackContext):
    logger.info('/permissions from %s', update.effective_user.first_name)

    update.message.reply_html('<code>{}</code>'.format(str(permissions)))


@u.check_permissions(required_permission=Permissions.ADMIN)
@u.failwithmessage
def set_permission(update: Update, context: CallbackContext):
    logger.info('/pset from %s', update.effective_user.first_name)

    if len(context.args) < 2:
        update.message.reply_html('使用: /pset <code>[授权密钥] [true/false/1/0]</code>')
        return

    key = context.args[0].lower()
    val = context.args[1].lower()
    if val.lower() not in ('true', 'false', '0', '1'):
        update.message.reply_html('传递错误的值。 使用: /pset <code>[授权密钥] [true/false/1/0]</code>')
        return

    if permissions.get(key, None) is None:
        update.message.reply_text('错误的密钥. 使用 /permissions 查看当前权限配置')
        return

    actual_val = True if val in ('true', '1') else False
    permissions.set(key, actual_val)

    update.message.reply_html('<b>新配置</b>:\n\n<code>{}</code>'.format(str(permissions)))


updater.add_handler(CommandHandler(['permissions', 'p'], get_permissions), bot_command=BotCommand("permissions", "查看配置权限"))
updater.add_handler(CommandHandler(['pset'], set_permission), bot_command=BotCommand("pset", "修改某项权限"))
