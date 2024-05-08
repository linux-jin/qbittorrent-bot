import logging

# noinspection PyPackageRequirements
from telegram import Update, BotCommand
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, Filters

from bot.updater import updater
from utils import u
from utils import Permissions

logger = logging.getLogger(__name__)


HELP_MESSAGE = """<b>命令列表</b>:

<i>读取命令</i>
• /start or /help: 显示帮助信息
• /available_filters: 显示可以用来列出种子数据的命令列表
• /overview: 显示正在下载/上传的总览
• /filter or /f <code>[子菜单]</code>: 筛选子菜单 (从完整菜单筛选)
• /settings or /s: 获取当前设置列表
• /transferinfo: 当前速度、队列和分享率设置总览
• /atm: 自动种子管理设置总览
• /atmyes or /atmno: 列出已启用/禁用自动种子管理的种子
• /json: 备份种子列表
• /version: 获取qbittorrent版本信息

<i>写入命令</i>
• <code>.torrent</code> 后缀文件: 通过文件添加种子
• 磁力链接: 通过磁力链接添加种子

<i>编辑命令</i>
• /altdown: 通过按键设置最大下载速度
• /altdown <code>[kb/s]</code>: 设置最大下载速度
• /altup <code>[kb/s]</code>: 设置最大上传速度
• /pauseall: 暂停所有种子
• /resumeall: 恢复所有种子
• /set <code>[设置] [新值]</code>: 修改设置
• <code>+tag</code> or <code>-tag</code>:  "<code>+xxx tags</code>" 或者 \
"<code>-xxx tags</code>" 给种子添加/删除标签. 可以使用多个标签，通过逗号“,”分隔 \
(标签可以包含空格)

<i>管理员命令</i>
• /permissions: 配置当前权限
• /pset <code>[密钥] [值]</code>: 更改权限值
• /freespace: 获取剩余磁盘空间

<i>释放命令</i>
• /rmkb: 移除键盘，如果有的话"""


@u.check_permissions(required_permission=Permissions.READ)
@u.failwithmessage
def on_help(update: Update, context: CallbackContext):
    logger.info('/help from %s', update.message.from_user.first_name)

    update.message.reply_html(HELP_MESSAGE)


updater.add_handler(CommandHandler('help', on_help), bot_command=BotCommand("help", "显示帮助信息"))
updater.add_handler(MessageHandler(Filters.regex(r'^\/start$'), on_help))
