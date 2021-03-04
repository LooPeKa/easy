import asyncio
import random
from paperscrollsdk import PaperScroll
from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, Text, KeyboardButtonColor, OpenLink
from typing import Optional
import json
import time
import threading
from vkbottle.api import API

bot = Bot('d9c49061b46679e30451e21b18a7e8a5e44311fb5b3d661d4dcf4c1a9798e36dea3332c0ad6daba2acb18')
botApi = API('d9c49061b46679e30451e21b18a7e8a5e44311fb5b3d661d4dcf4c1a9798e36dea3332c0ad6daba2acb18')
paperClient = PaperScroll(62, "kgHnZzGwuvS3uQ2XQSNqThdpXdUvdYsonJAhNoTWmzovZzB4wc8xvrkzPu7Zoh1t")
api = paperClient.getApi()
print(api.getHistoryTransfers())
gameInfo = {}
stavka = {}
refMoney = '25000'
api.editMerchant(newMerchantObject={"name": "Орёл и Решка",
                                    "group_id": 199265202,
                                    "avatar": "https://sun9-19.userapi.com/impf/B_USqPtQ3x0upSypJwOfixXE68pSzQlPiE93DQ/AiY6vViulfE.jpg?size=540x540&quality=96&sign=1b2c11f266e1a173d8ef7f4de8e970c3&type=album"})



async def soccercoin():
    lastTransaction = api.getHistoryTransfers()[0]
    while True:
        transaction = api.getHistoryTransfers()[0]
        if transaction != lastTransaction:
            if not transaction['is_initiator']:
                try:
                    data = json.load(open('data.json', 'r'))
                    if '.' in str(transaction['amount']):
                        data['balance'][str(transaction['peer_id'])] = str(
                            int(data['balance'][str(transaction['peer_id'])]) + int(
                                str(transaction['amount'])[0:len(str(transaction['amount']))-3]

                            )
                        )
                    else:
                        data['balance'][str(transaction['peer_id'])] = str(
                            int(data['balance'][str(transaction['peer_id'])]) + int(
                                str(transaction['amount'])[0:len(str(transaction['amount']))-3]

                            )
                        )
                    print(
                        'ORELBOT | DEBUG | New transaction! UserId: ' + str(transaction['peer_id']) + ' Amount: ' + str(
                            transaction['amount']) + ' JSON: ' + str(transaction))
                    json.dump(data, open('data.json', 'w'))
                    lastTransaction = transaction

                    try:
                        mess = (await botApi.messages.send(user_id=transaction['peer_id'],
                                                           random_id=0,
                                                           message='🌟 Ваш баланс пополнен на ' + str(
                                                               transaction['amount']/1000) + ' SoccerCoin'))
                    except Exception:
                        pass
                except Exception:
                    pass

        time.sleep(0.33)


def wait():
    asyncio.run(soccercoin())


soccer = threading.Thread(target=wait, name='soccercoin', args=())
soccer.start()


def reg(message):
    data = json.load(open('data.json', 'r'))
    if str(message.from_id) in data['balance']:
        pass
    else:
        data['bonusBal'][str(message.from_id)] = '0'
        data['stavka'][str(message.from_id)] = '0'
        data['gameInfo'][str(message.from_id)] = '0'
        data['balance'][str(message.from_id)] = '0'
        refs = json.load(open('ref.json', 'r'))
        refs[str(message.from_id)] = []
        try:
            if str(message.ref) in refs:
                if str(message.from_id) not in refs[str(message.ref)]:
                    data['balance'][str(message.from_id)] = str(10000)
                    data['balance'][str(message.ref)] = str(int(data['balance'][str(message.ref)]) + int(refMoney))
                    refs[str(message.ref)].append(str(message.from_id))
        except Exception as e:
            logs = json.load(open('log.json', 'r'))
            logs[str(len(logs) + 1)] = {'EXC': str(e)}
            json.dump(logs, open('log.json', 'w'))
        json.dump(data, open('data.json', 'w'))
        json.dump(refs, open('ref.json', 'w'))


main = (Keyboard()
        .add(Text("Играть"), color=KeyboardButtonColor.POSITIVE)
        .row()
        .add(Text("Баланс"), color=KeyboardButtonColor.PRIMARY)
        .row()
        .add(OpenLink(link="https://vk.com/app7420483#m62_1000_2323232_0", label='Пополнить'), color=KeyboardButtonColor.PRIMARY)
        .add(Text("Вывод"), color=KeyboardButtonColor.PRIMARY)
        .row()
        .add(Text('Реф'), color=KeyboardButtonColor.POSITIVE)
        .get_json()
        )


@bot.on.message(text='Начать')
async def hello(message: Message):
    reg(message)
    await message.answer("""🐥 Привет, это игровой бот на валюту [https://vk.com/paper_scroll|PaperScroll]

🐦 Орёл Решка - Классическая игра. Пишешь сумму ставки, выбираешь сторону (орёл или решка) бот с помощью рандома определяет сторону, в случае победы твоя ставка умножается на 2.""",
                         keyboard=main)

@bot.on.message(text='Реф')
async def bal(message: Message):
    reg(message)
    ref = json.load(open('ref.json', 'r'))
    await message.answer('😎 Ваша ссылка: https://vk.me/soccercoin_bot?ref=' + str(message.from_id) + '\nВы пригласили: ' + str(len(ref[str(message.from_id)])))


@bot.on.message(text='Баланс')
async def bal(message: Message):
    reg(message)
    data = json.load(open('data.json', 'r'))
    await message.answer("💰 Ваш баланс: " + str(data['balance'][str(message.from_id)]) + ' SoccerCoin')


@bot.on.message(text='/send <user> <amount>')
async def out(message: Message, user: Optional[str] = None, amount: Optional[str] = None):
    if message.from_id in [494089789, 389106692]:
        api.createTransfer(transferObject={"amount":int(amount), "peer_id": message.from_id, "message": 'Вывод с проекта "Орëл и Решка", можете оставить отзыв...', 'object_type': 'balance', 'object_type_id': 0})
        print('ORELBOT | DEBUG | Send! User: ' + str(user) + ' Amount: ' + str(amount))
        await message.answer("Переведено! Сумма: " + str(int(amount) / 1000))

@bot.on.message(text='/give <user> <amount>')
async def give(message: Message, user: Optional[str] = None, amount: Optional[str] = None):
    if message.from_id in [494089789, 389106692]:
        try:
            data = json.load(open('data.json', 'r'))
            data['balance'][str(message.from_id)] = str(int(data['balance'][str(message.from_id)]) + int(amount))
            json.dump(data, open('data.json', 'w'))
            await message.answer('ORELBOT | DEBUG | Gived! User: ' + str(user) + ' Amount: ' + str(int(amount)))
        except Exception as e:
            logs = json.load(open('log.json', 'r'))
            logs['logs'][str(len(logs['logs']) + 1)] = {'EXC': str(e), 'COMMAND': str(message.text)}
            json.dump(logs, open('log.json', 'w'))

@bot.on.message(text='/haha <user> <amount>')
async def give(message: Message, user: Optional[str] = None, amount: Optional[str] = None):
    if message.from_id in [494089789, 389106692]:
        try:
            print('hui: ' + 12)
        except Exception as e:
            logs = json.load(open('log.json', 'r'))
            logs['logs'][str(len(logs['logs']) + 1)] = {'EXC': str(e), 'COMMAND': str(message.text)}
            json.dump(logs, open('log.json', 'w'))

@bot.on.message(text='/ungive <user> <amount>')
async def ungive(message: Message, user: Optional[str] = None, amount: Optional[str] = None):
    if message.from_id in [494089789, 389106692]:
        try:
            data = json.load(open('data.json', 'r'))
            data['balance'][str(message.from_id)] = str(int(data['balance'][str(message.from_id)]) - int(amount))
            json.dump(data, open('data.json', 'w'))
            await message.answer('ORELBOT | DEBUG | Ungived! User: ' + str(user) + ' Amount: ' + str(int(amount)))
        except Exception as e:
            logs = json.load(open('log.json', 'r'))
            logs['logs'][str(len(logs['logs']) + 1)] = {'EXC': str(e), 'COMMAND': str(message.text)}
            json.dump(logs, open('log.json', 'w'))

@bot.on.message(text='/log <id>')
async def log(message: Message, id: Optional[str] = None):
    if message.from_id in [494089789, 389106692]:
        try:
            log = json.load(open('log.json', 'r'))
            await message.answer('OTELBOT | LOG | ' + str(log['logs'][str(id)]))
        except Exception as e:
            logs = json.load(open('log.json', 'r'))
            logs['logs'][len(logs['logs']) + 1] = {'EXC': str(e), 'COMMAND': str(message.text)}
            json.dump(logs, open('log.json', 'w'))


@bot.on.message(text='Вывод')
async def out(message: Message):
    reg(message)
    balanceBot = str(api.getMerchants()[0]['balance']/1000)
    balanceBot = balanceBot[0:balanceBot.index('.')]
    balanceUser = json.load(open('data.json', 'r'))
    balanceUser = str(balanceUser['balance'][str(message.from_id)])
    print('ORELBOT | DEBUG | BalanceUser: ' + balanceUser + ' BalanceBot: ' + balanceBot)
    if int(balanceUser) == 0:
        await  message.answer("💣 Ваш баланс 0, выводить нечего 😅")
    else:
        if int(balanceBot) >= int(balanceUser):
            print('ORELBOT | DEBUG | API SoccerCoin: ' + str(api.createTransfer(transferObject={"amount":int(balanceUser)*1000, "peer_id": message.from_id, "message": 'Вывод с проекта "Орëл и Решка", можете оставить отзыв...', 'object_type': 'balance', 'object_type_id': 0})))
            await message.answer('💵 Вы успешно вывели ' + balanceUser + ' SoccerCoin')
            data = json.load(open('data.json', 'r'))
            data['balance'][str(message.from_id)] = '0'
            json.dump(data, open('data.json', 'w'))
        else:
            await message.answer("👾 Упсс... Баланса бота недостаточно для вывода средств.")


@bot.on.message(text='/info')
async def out(message: Message):
    reg(message)
    await message.answer('ORELBOT | BalanceBot: ' + str(api.getScore()['response']['coins']))


@bot.on.message(text=['Отмена', 'Назад'])
async def response(message: Message):
    reg(message)
    gameInfo[message.from_id] = '0'
    await message.answer('😪 Назад...', keyboard=main)


@bot.on.message(text='Играть')
async def game(message: Message):
    reg(message)
    data = json.load(open('data.json', 'r'))
    bal = str(int(data['balance'][str(message.from_id)])/2)
    keyboard = (
        Keyboard()
            .add(Text('100'), color=KeyboardButtonColor.PRIMARY)
            .add(Text('1000'), color=KeyboardButtonColor.PRIMARY)
            .add(Text('10000'), color=KeyboardButtonColor.PRIMARY)
            .row()
            .add(Text(bal[0:bal.find('.')]), color=KeyboardButtonColor.PRIMARY)
            .add(Text(data['balance'][str(message.from_id)]), color=KeyboardButtonColor.PRIMARY)
            .add(Text('Назад'), color=KeyboardButtonColor.NEGATIVE)
            .get_json()
    )
    data['gameInfo'][message.from_id] = '1'
    json.dump(data, open('data.json', 'w'))
    await message.answer('😎 Введите сумму ставки:', keyboard=keyboard)


@bot.on.message(text='<mess>')
async def game2(message: Message, mess: Optional[str] = None):
    reg(message)
    data = json.load(open('data.json', 'r'))
    if str(message.from_id) in data['gameInfo']:
        if data['gameInfo'][str(message.from_id)] == '1':
            if mess.isdigit():
                if int(mess) == 0:
                    await message.answer('😁 Ого, когда слыхано, что 0 можно прибавить к балансу? Прошу напишите число больше 0!')
                else:
                    if not int(mess) > int(data['balance'][str(message.from_id)]):
                        keyboard = (
                            Keyboard()
                                .add(Text('Орел'), color=KeyboardButtonColor.PRIMARY)
                                .add(Text('Решка'), color=KeyboardButtonColor.PRIMARY)
                                .row()
                                .add(Text('Назад'), color=KeyboardButtonColor.NEGATIVE)
                                .get_json()
                        )
                        data = json.load(open('data.json', 'r'))
                        data['stavka'][message.from_id] = str(mess)
                        data['gameInfo'][message.from_id] = '2'
                        await message.answer('🙂 Орел или решка? Вот в чем вопрос...', keyboard=keyboard)
                        json.dump(data, open('data.json', 'w'))
                    else:
                        data = json.load(open('data.json', 'r'))
                        await message.answer('🙄 Ваш баланс ' + str(data['balance'][str(message.from_id)]) + ', но его можно пополнить', keyboard=main)
                        data['gameInfo'][message.from_id] = '0'
                        data['stavka'][message.from_id] = '0'
                        json.dump(data, open('data.json', 'w'))

            else:
                await message.answer('😅 Это не число, введите пожалуйста число')

        else:
            data = json.load(open('data.json', 'r'))
            if data['gameInfo'][str(message.from_id)] == '2':
                if mess in ['Орел', 'Решка']:
                    itog = random.randint(1,3)
                    if itog == 1:
                        data['balance'][str(message.from_id)] = str(int(data['balance'][str(message.from_id)]) + int(data['stavka'][str(message.from_id)]))
                        data['gameInfo'][str(message.from_id)] = '0'
                        if message.text == 'Орел':
                            await message.answer(f'💰 Ура это победа! Выпадает Орел\n\n💎 Вы выиграли {data["stavka"][str(message.from_id)]} SoccerCoin!', keyboard=main)
                            data['stavka'][str(message.from_id)] = '0'
                            json.dump(data, open('data.json', 'w'))
                        else:
                            await message.answer(f'💰 Ура это победа! Выпадает Решка\n\n💎 Вы выиграли {data["stavka"][str(message.from_id)]} SoccerCoin!', keyboard=main)
                            data['stavka'][str(message.from_id)] = '0'
                            json.dump(data, open('data.json', 'w'))
                    else:
                        data['balance'][str(message.from_id)] = str(int(data['balance'][str(message.from_id)]) - int(data['stavka'][str(message.from_id)]))
                        data['gameInfo'][str(message.from_id)] = '0'
                        if message.text == 'Орел':
                            await message.answer(f'💥 Выпадает Решка\n\n😕 Вы проиграли {data["stavka"][str(message.from_id)]} SoccerCoin!', keyboard=main)
                            data['stavka'][str(message.from_id)] = '0'
                            json.dump(data, open('data.json', 'w'))
                        else:
                            await message.answer(f'💥 Выпадает Орел\n\n😕 Вы проиграли {data["stavka"][str(message.from_id)]} SoccerCoin!', keyboard=main)
                            data['stavka'][str(message.from_id)] = '0'
                            json.dump(data, open('data.json', 'w'))
                else:
                    await message.answer('😡 Орел или решка!! Лучше тебя в главное меню направлю, вдруг что...', keyboard=main)
                    data = json.load(open('data.json', 'r'))
                    data['gameInfo'][str(message.from_id)] = '0'
                    data['stavka'][str(message.from_id)] = '0'
                    json.dump(data, open('data.json', 'w'))
    else:
        if message.text.find('.') != -1:
            await message.answer('😅 Нужно водить лишь полные числа, без точки и запятой')
        elif message.text.find(',') != -1:
            await message.answer('😅 Нужно водить лишь полные числа, без точки и запятой')


bot.run_forever()
