import requests, json, time
src = "https://www.speedrun.com/api/v1/"

database = {}
mods = set()
t = time.time()
delay = 1
step = 100
offset = 0
while True:
    try:
        print(step)
        if step == 0:
            print(f"jumped offset {offset}")
            offset += 1
            step = 100
        r = requests.get(f"{src}games?offset={offset}&max={step}&embed=moderators",timeout = 60)
        now = time.time()
        duration = now - t
        if duration < delay:
            sleep_time = delay - (duration)
            print(f"{step} : {sleep_time}")
            time.sleep(sleep_time)
        t = now
        g = r.json()
        print(g)
        games = g["data"]
        for game in games:
            for mod in game["moderators"]["data"]:
                modID = mod.get("id","")
                if not modID:
                    continue
                if modID in mods:
                    database[modID][2] += 1
                    continue
                mods.add(modID)
                if mod["location"] == None:
                    flag = ":united_nations:"
                else:
                    flag = f':flag_{mod["location"]["country"]["code"][:2]}:'
                print(f'{modID} : {mod["names"]["international"]}, {flag}, 1', offset)
                database[modID] = [mod["names"]["international"], flag, 1]
        offset += step
        if len(games) < step:
            break
    except Exception:
        step = step//2
        continue

with open("vdatabase.json", "a") as vd:
    vd.truncate(0)
    vd.writelines(json.dumps(database))

# LEADERBOARD

with open("outputs/modcountfinallb.txt", "a") as filb:
    filb.truncate(0)
    no, no2, bi = 1, 1, ""
    with open("vdatabase.json", "r") as data:
        datab = json.loads(data.readlines()[0])
        m = {}
        for i in datab:
            m.update({i: datab[i][2]})
        for i in list(dict(sorted(m.items(), key=lambda item: item[1], reverse=True)).keys()):
            if bi != datab[i][2]:
                no2 = no
            filb.writelines(str(f'`{no2}.`{datab[i][1]}`{str(datab[i][0].encode("utf-8"))[2:-1]}{" "*(26-(len(str(datab[i][2]))+len(datab[i][0])))}{datab[i][2]}`\n'))
            no+=1
            bi = datab[i][2]