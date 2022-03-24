from nonebot.plugin import on_command
from nonebot.params import ArgStr
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, Message, MessageEvent
from nonebot import logger

from upload import Reporter

temperature = on_command('体温上报',rule = to_me())
@temperature.got('session_id',"成电智慧学工Session Id：")
async def upload_temperature(bot: Bot, event: MessageEvent, key: Message = ArgStr()):
    reporter = await Reporter(key)
    logger.info(f"get session:{key}")
    result, state = await reporter.run()
    msg=f"填报状态：{state}\n"+"请自行手动填报" if not result else ''
    logger.info(f"{msg}")
    await temperature.finish(Message(msg))