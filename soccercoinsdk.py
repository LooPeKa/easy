import requests

# "613843176": "2800000", "562644673": "222222"
# 💰 Ура это победа! Выпадает Решка 💎 Вы выиграли SoccerCoin!
# 💥 Выпадает Орёл\n\n😕 Вы проиграли SoccerCoin!

class Api:
    def __init__(self, token, user_id):
        self.token = str(token)
        self.user_id = str(user_id)
        self.url = 'https://soccercoin.ru/api/'
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'User ' + self.token}

    def getUrl(self, amount, is_locked):
        return 'https://vk.com/app7727936#m' + self.user_id + '_' + str(amount) + '_' + str(is_locked)

    def sendPayment(self, to_id, amount):
        data = {'to_id': int(to_id), 'amount': int(amount)}
        response = requests.post(url=self.url + 'sendPayment', json=data, headers=self.headers).json()
        return response

    def getHistory(self, offset=0, limit=100):
        data = {'offset': int(offset), 'limit': int(limit)}
        response = requests.post(url=self.url + 'getHistory', json=data, headers=self.headers).json()
        return response

    def getScore(self):
        response = requests.post(url=self.url + 'getScore', headers=self.headers).json()
        return response

    def getScoreById(self, user_ids):
        data = {'user_ids': user_ids}
        response = requests.post(url=self.url + 'getScoreById', headers=self.headers, json=data).json()
        return response
