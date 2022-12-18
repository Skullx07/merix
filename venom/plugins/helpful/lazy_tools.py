# by Ryuk and Kakashi

from venom import *
from pyrogram.errors import UsernameInvalid

HELP_ = Config.HELP[plugin_name(__name__)] = {'type': 'helpful', 'commands': []}

HELP_['commands'].extend([
    {
        'command': 'joinc',
        'flags': None,
        'usage': 'join private / public chat using link or @username',
        'syntax': (
            '{tr}join chat_link or @username'
        ),
        'sudo': True
    },
    {
        'command': 'click',
        'flags': None,
        'usage': ('Click a button in replied message.\n'
                  '**Note:** Is case sensitive.\n'
                  'Defaults to 1st button if no input is provided.'),
        'syntax': '{tr}click Yes',
        'sudo': True
    }
])

########################################################################################################################


@venom.trigger("joinc")
async def join_chat(_, message: MyMessage):
    reply = message.reply_to_message
    link = reply.text or message.input_str
    if not link:
        return await message.edit(
            "Bruh, can't Join without a Link...", del_in=3
        )
    try:
        await venom.join_chat(link)
    except UsernameInvalid:
        link = link.split("/")[-1]
        await venom.join_chat(link)
    except BaseException as e:
        if str(e).startswith("Telegram says: [400 Bad Request] - [400 INVITE_REQUEST_SENT]"):
            return await message.reply("`Join Request Sent.`")
        else:
            raise e
    await message.reply("`Joined.`")

########################################################################################################################


@venom.trigger("click")
async def click_it(_, message: MyMessage):
    button_name = message.input_str
    button = message.reply_to_message
    if not button:
        return await message.edit("`Reply to a button...`", del_in=5)
    try:
        if button_name:
            if button_name.isdigit():
                button_name = int(button_name)
            await button.click(button_name)
        else:
            await button.click(0)
    except ValueError:
        await message.edit("`Button doesn't exists...`")
    except AttributeError:
        await message.edit("`Reply to a message with button...`")
    except TimeoutError:
        return

########################################################################################################################

HELP_['commands'].append(
    {
        'command': 'reply',
        'flags': {
            '-c': 'change client'
        },
        'usage': 'reply to any message',
        'syntax': '{tr}reply text',
        'sudo': False
    }
)


@venom.trigger('reply')
async def reply_(_, message: MyMessage):
    """ reply to any message """
    input_ = message.input_str
    flags = message.flags
    if not input_:
        return
    reply_ = message.replied
    reply_to = reply_.id if reply_ else None
    if '-c' not in flags:
        await venom.both.send_message(message.chat.id, input_, reply_to_message_id=reply_to)
    else:
        await venom.both.bot.send_message(message.chat.id, input_, reply_to_message_id=reply_to)