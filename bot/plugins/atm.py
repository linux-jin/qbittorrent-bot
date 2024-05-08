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
def on_atm_command(update: Update, context: CallbackContext):
    logger.info('/atm command used by %s', update.effective_user.first_name)

    preferences = qb.preferences()
    text = "默认自动种子管理: {auto_tmm_enabled}\n\n" \
           "- 重新定位种子如果分类改变: {torrent_changed_tmm_enabled}\n" \
           "- 重新定位受影响的种子如果默认保存路径改变: {save_path_changed_tmm_enabled}\n" \
           "- 重新定位受影响的种子 " \
           "分类保存路径改变: {category_changed_tmm_enabled}".format(**preferences)

    update.message.reply_html(text)


@u.check_permissions(required_permission=Permissions.READ)
@u.failwithmessage
def on_atm_list_command(update: Update, context: CallbackContext):
    logger.info('/atmyes or /atmno command used by %s', update.effective_user.first_name)

    torrents = qb.torrents()

    atm_enabled = update.message.text.lower().endswith("atmyes")

    base_string = "• <code>{short_name}</code> ({size_pretty}, {state_pretty}) [<a href=\"{info_deeplink}\">info</a>]"
    strings_list = [torrent.string(base_string=base_string) for torrent in torrents if torrent['auto_tmm'] is atm_enabled]

    update.message.reply_html(
        f"有 <b>{len(strings_list)}/{len(torrents)}</b> 种子"
        f"自动种子管理状态为 {'enabled' if atm_enabled else 'disabled'}:"
    )

    if not strings_list:
        update.message.reply_text("-")
        return

    for strings_chunk in u.split_text(strings_list):
        update.message.reply_html('\n'.join(strings_chunk))


updater.add_handler(CommandHandler(['atm'], on_atm_command), bot_command=BotCommand("atm", "关于自动种子管理的信息"))
updater.add_handler(CommandHandler(['atmyes'], on_atm_list_command), bot_command=BotCommand("atmyes", "列出已启用自动管理的种子"))
updater.add_handler(CommandHandler(['atmno'], on_atm_list_command), bot_command=BotCommand("atmno", "列出已禁用自动管理的种子"))
