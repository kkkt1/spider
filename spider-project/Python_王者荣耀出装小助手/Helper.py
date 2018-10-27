import requests
import time


class Spider():
    def __init__(self):
        self.headers = {
            'Accept-Charset': 'UTF-8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'Keep-Alive'
        }
        self.weapon_url = "http://gamehelper.gm825.com/wzry/equip/list?game_id=7622"
        self.heros_url = "http://gamehelper.gm825.com/wzry/hero/list?game_id=7622"
        self.hero_url = "http://gamehelper.gm825.com/wzry/hero/detail?hero_id={}"
        print('*' * 60)
        print('*********王者荣耀查询助手********')
        print('********输入英雄id查询信息********')
        print('*' * 60)

    # 外部调用函数
    def run(self):
        heroId_exist = self._Get_HeroId()
        heroId = input('\n输入你要查询的英雄id:')
        if heroId not in heroId_exist:
            print('该英雄id不存在')
            return
        weapon_info = self._Get_WeaponInfo()
        self._Get_HeroInfo(weapon_info, heroId)

    # 获得英雄ID
    def _Get_HeroId(self):
        res = requests.get(url=self.heros_url, headers=self.headers)
        heros = res.json()['list']
        num = 0
        heroId_list = []
        for hero in heros:
            num += 1
            print('%sID: %s' % (hero['name'], hero['hero_id']), end='\t\t\t')
            heroId_list.append(hero['hero_id'])
            if num == 3:
                num = 0
                print('')
        return heroId_list

    # 获取武器信息
    def _Get_WeaponInfo(self):
        res = requests.get(url=self.weapon_url, headers=self.headers)
        weapon_info = res.json()['list']
        return weapon_info

    # 获得出装信息
    def _Get_HeroInfo(self, weapon_info, heroId):
        def seek_weapon(equip_id, weapon_info):
            for weapon in weapon_info:
                if weapon['equip_id'] == str(equip_id):
                    return weapon['name'], weapon['price']
            return None

        res = requests.get(url=self.hero_url.format(heroId), headers=self.headers).json()
        print('[%s 历史背景]: %s' % (res['info']['name'], res['info']['history_intro']))
        num = 0
        for choice in res['info']['equip_choice']:
            num += 1
            print('\n[%s]:\n  %s' % (choice['title'], choice['description']))
            total_price = 0
            for weapon in choice['list']:
                weapon_name, weapon_price = seek_weapon(weapon['equip_id'], weapon_info)
                print('[%s 价格]: %s' % (weapon_name, weapon_price))
                if num == 3:
                    print('')
                    num = 0
                total_price += int(weapon_price)
            print('[装备总价格]: %d' % total_price)


if __name__ == '__main__':
    while True:
        Spider().run()
        time.sleep(5)
