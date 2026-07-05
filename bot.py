import random, requests

TOKEN, CHAT_ID, TARGET = "8663455110:AAGPYTF2qNqMdSBN3rM6q9t4lG0EwXKhWKk", "701442500", 7

def send_signal(game, market, val):
    url = f"https://telegram.org{TOKEN}/sendMessage"
    text = f"⚠️ *{game.upper()}*: СЕРИЯ {TARGET} РАЗ!\n📌 *Маркет*: {market}\n📈 *Выпало*: {val}\n👉 *СТАВКА*: ПРОТИВОПОЛОЖНОЕ!"
    try: requests.post(url, json={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}, timeout=10)
    except: pass

def get_markets(gname, balls):
    nums = [int(b['num']) for b in balls if b['num'].isdigit()]
    if not nums: return {}
    tot, ev, od = sum(nums), sum(1 for n in nums if n % 2 == 0), sum(1 for n in nums if n % 2 != 0)
    m = {"Сумма Чет/Нечет": "Сумма ЧЕТНАЯ" if tot % 2 == 0 else "Сумма НЕЧЕТНАЯ", "Преобладание Чет/Нечет": "Больше ЧЕТНЫХ" if ev > od else "Больше НЕЧЕТНЫХ"}
    
    if gname == "Lucky 5":
        m["Тотал 92.5"] = "Сумма < 92.5" if tot < 92.5 else "Сумма > 92.5"
    elif gname == "Lucky 6" and len(balls) >= 6:
        sr, sb = sum(int(b['num']) for b in balls if b['color'] == 'red'), sum(int(b['num']) for b in balls if b['color'] == 'blue')
        sa, sb_z, sc = sum(nums[:2]), sum(nums[2:4]), sum(nums[4:6])
        m.update({"Красные 13.5": "Красные < 13.5" if sr < 13.5 else "Красные > 13.5", "Синие 12.5": "Синие < 12.5" if sb < 12.5 else "Синие > 12.5", "Зона A 9.5": "A < 9.5" if sa < 9.5 else "A > 9.5", "Зона A Чет/Нечет": "A ЧЕТ" if sa % 2 == 0 else "A НЕЧЕТ", "Зона B 9.5": "B < 9.5" if sb_z < 9.5 else "B > 9.5", "Зона B Чет/Нечет": "B ЧЕТ" if sb_z % 2 == 0 else "B НЕЧЕТ", "Зона C 9.5": "C < 9.5" if sc < 9.5 else "C > 9.5", "Зона C Чет/Нечет": "C ЧЕТ" if sc % 2 == 0 else "C НЕЧЕТ", "Тотал 26.5": "Сумма > 26.5" if tot > 26.5 else "Сумма < 26.5"})
    elif gname == "Lucky 7" and len(balls) >= 7:
        sy, sbl = sum(int(b['num']) for b in balls if b['color'] == 'yellow'), sum(int(b['num']) for b in balls if b['color'] == 'black')
        cy, cbl = sum(1 for b in balls if b['color'] == 'yellow'), sum(1 for b in balls if b['color'] == 'black')
        m.update({"Желтые тотал 73.5": "Желтые < 73.5" if sy < 73.5 else "Желтые > 73.5", "Черные тотал 73.5": "Черные < 73.5" if sbl < 73.5 else "Черные > 73.5", "Тотал 150.5": "Сумма < 150.5" if tot < 150.5 else "Сумма > 150.5", "Желтые кол-во 3.5": "Желтых < 3.5" if cy < 3.5 else "Желтых > 3.5", "Черные кол-во 3.5": "Черных < 3.5" if cbl < 3.5 else "Черных > 3.5", "1-й шар Чет/Нечет": "1-й ЧЕТ" if nums % 2 == 0 else "1-й НЕЧЕТ", "Посл. шар Чет/Нечет": "Посл. ЧЕТ" if nums[-1] % 2 == 0 else "Посл. НЕЧЕТ", "1-й шар Цвет": "1-й ЖЕЛТЫЙ" if balls['color'] == 'yellow' else "1-й ЧЕРНЫЙ", "Посл. шар Цвет": "Посл. ЖЕЛТЫЙ" if balls[-1]['color'] == 'yellow' else "Посл. ЧЕРНЫЙ", "Преобладание цвета": "Больше ЖЕЛТЫХ" if cy > cbl else "Больше ЧЕРНЫХ"})
    return m

def parse():
    for gn in ["Lucky 5", "Lucky 6", "Lucky 7"]:
        draws = [{"draw": str(i), "balls": [{"num": str(random.randint(1, 36 if gn == "Lucky 5" else 9 if gn == "Lucky 6" else 42)), "color": random.choice(["white", "blue", "green", "red"] if gn == "Lucky 5" else ["red", "blue"] if gn == "Lucky 6" else ["yellow", "black"])} for _ in range(5 if gn == "Lucky 5" else 6 if gn == "Lucky 6" else 7)]} for i in range(20)]
        
        hist = {}
        for d in draws[:TARGET]:
            for k, v in get_markets(gn, d["balls"]).items(): hist.setdefault(k, []).append(v)
        for mk, out in hist.items():
            if len(out) == TARGET and len(set(out)) == 1: send_signal(gn, mk, out)

if __name__ == "__main__":
    parse()
