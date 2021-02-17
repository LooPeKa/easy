import json

from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, Text, KeyboardButtonColor
from vkbottle_types import GroupTypes
from vkbottle_types.events import GroupEventType
from vkcoinapi import *
coin = VKCoin(key='rGFC#ONxp3KdR5d3pq_mM82hAfYpn9xwjJFNV5v[83Vjr=Thsa', merchantId=494089789)

bot = Bot("66697a7990c2b21a36eccc3a5082ca88debe845b40da2119bae68a52615c4293203ab2dcb63eab4d6fe8a")

ref1 = '100000'
ref2 = '250000'


def reg(message):
    data = json.load(open('data.json', 'r'))
    if str(message.from_id) not in data['balance']:
        if message.ref is not None:
            data['balance'][str(message.from_id)] = '0'
            data['refs'][str(message.from_id)] = {}
            data['refs'][str(message.ref)][str(message.from_id)] = '1'
            data['id'][str(message.from_id)] = str(len(data['id']) + 1)
        else:
            data['balance'][str(message.from_id)] = '0'
            data['refs'][str(message.from_id)] = {}
            data['id'][str(message.from_id)] = str(len(data['id']) + 1)
        json.dump(data, open('data.json', 'w'))
    else:
        pass


main = (
    Keyboard()
        .add(Text('🌈 Получить реф. ссылку'), color=KeyboardButtonColor.POSITIVE)
        .row()
        .add(Text('💎 Профиль'), color=KeyboardButtonColor.PRIMARY)
        .row()
        .add(Text('📊 Статистика'), color=KeyboardButtonColor.NEGATIVE)
        .add(Text('💵 Вывод'), color=KeyboardButtonColor.NEGATIVE)
        .add(Text('🎈 Реклама'), color=KeyboardButtonColor.NEGATIVE)
)


@bot.on.message(text=['Начать', 'начать'])
async def hello(message: Message):
    reg(message)
    await message.answer(f'''🥤 Привет !
В этом боте ты за каждого реферала активируещего профиль, ты получишь {ref2} VKcoin''', keyboard=main)


@bot.on.message(text=['🌈 Получить реф. ссылку'])
async def hello(message: Message):
    reg(message)
    await message.answer(f'''🌟 Твоя реф. ссылка - https://vk.me/pieref?ref={message.from_id}

💎 За каждого реферала активируещего профиль ты получаешь {ref2} VKcoin''')


@bot.on.message(text=['💎 Профиль'])
async def hello(message: Message):
    reg(message)
    data = json.load(open('data.json', 'r'))
    await message.answer(f'''👾 id - {data['id'][str(message.from_id)]}

💰 Баланс - {data['balance'][str(message.from_id)]} VKcoin

👪 Рефералов - {len(data['refs'][str(message.from_id)])}''', keyboard=main)



@bot.on.message(text=['📊 Статистика'])
async def hello(message: Message):
    reg(message)
    data = json.load(open('data.json', 'r'))
    await message.answer(f'''📊 Статистика -

⚡ Всего выведено {data['balance'][str(message.from_id)]} VKcoin.

💥 Всего игроков {len(data['balance'])}''', keyboard=main)

@bot.on.message(text=['💵 Вывод'])
async def hello(message: Message):
    reg(message)
    data = json.load(open('data.json', 'r'))
    if coin.getBalance()['response']['494089789'] < int(data['balance'][str(message.from_id)]):
        await message.answer('🌟 Упс... Баланса бота недостаточно, ожидай пополнение...')

    else:
        coin.sendPayment(to=message.from_id, amount=int(data['balance'][str(message.from_id)])*1000)
        await message.answer(f'💵 Успешно выведено {data["balance"][str(message.from_id)]} VKcoin.', keyboard=main)
        data['>'] = str(int(data['>']) + int(data['balance'][str(message.from_id)]))
        data['balance'][str(message.from_id)] = '0'
        json.dump(data, open('data.json', 'w'))


@bot.on.message(text=['🎈 Реклама'])
async def hello(message: Message):
    reg(message)
    await message.answer('''💰 Купить рекламу (рассылка, пост) можно у него: https://vk.com/i_to_nuzhen_nenado''', keyboard=main)



@bot.on.raw_event(GroupEventType.GROUP_JOIN, dataclass=GroupTypes.GroupJoin)
async def group_join_handler(event: GroupTypes.GroupJoin):
    user_id = event.object.user_id
    data = json.load(open('data.json', 'r'))
    for i in data['refs']:
        if len(i) >= 1:
            if str(user_id) in data['refs'][i]:
                if data['refs'][i][str(user_id)] == '1':
                    data['balance'][str(user_id)] = str(int(data['balance'][str(user_id)]) + int(ref1))
                    data['balance'][str(i)] = str(int(data['balance'][str(i)]) + int(ref2))
                    data['refs'][str(i)][str(user_id)] = '2'
                    json.dump(data, open('data.json', 'w'))

                    await bot.api.messages.send(random_id=0,
                                                    user_id=int(i),
                                                    message=f'💎 Твой реферал подписался на группу, на твой баланс зачислено {ref2} VKcoin.')



bot.run_forever()
