import logging

# noinspection PyPackageRequirements
from telegram import Update, BotCommand
from telegram.ext import CommandHandler, CallbackContext

from bot.qbtinstance import qb
from bot.updater import updater
from utils import u
from utils import Permissions

logger = logging.getLogger(__name__)


@u.check_permissions(required_permission=Permissions.READ)
@u.failwithmessage
def on_version_command(update: Update, context: CallbackContext):
    logger.info('/version from %s', update.message.from_user.first_name)

    text = 'qBittorrent 版本: <code>{}</code>\nAPI 版本: <code>{}</code>\n\n构建信息:\n<code>{}</code>'.format(
        qb.qbittorrent_version,
        qb.api_version,
        "\n".join([f"{k} {v}" for k, v in qb.build_info().items()])
    )

    update.message.reply_html(text)


updater.add_handler(CommandHandler('version', on_version_command), bot_command=BotCommand("version", "查看qbittorrent版本号"))
