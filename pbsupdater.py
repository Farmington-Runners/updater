import requests, json, time
src = "https://www.speedrun.com/api/v1/"
with open("database.json", "r") as f:
    fjson = json.loads(f.readlines()[0])
no, no2 = 0, 0

def most_frequent(List):
    try:
        counter = 0
        num = List[0]
        
        for i in List:
            curr_frequency = List.count(i)
            if(curr_frequency> counter):
                counter = curr_frequency
                num = i
    
        return num
    except Exception:
        return 0

no2 = 0
t = time.time()
for id in fjson:
    alllevels, allcategories, allgames, allgameswithwrs, gamesmostwrs  = [], [], [], [], []
    allpodiums, allwrs, allILwrs, allFGwrs= 0, 0, 0, 0
    deleted = False
    if (no % 50 == 0 and no != 0) and time.time() - t < 40:
        time.sleep(40 - (time.time() - t))
        t = time.time()
    no2 += 1
    while True:
        try:
            pbs = requests.get(src + f"users/{id}/personal-bests").json()
        except Exception:
            continue
        no += 1
        if "status" in list(pbs.keys()):
            if pbs["status"] == 404:
                deleted = True
                break
            else:
                print("We're getting rate limited!")
                time.sleep(10)
                continue
        pbs = pbs["data"]
        for run in pbs:
            if run["run"]["level"] != None and not (run["run"]["level"] in alllevels):
                alllevels.append(run["run"]["level"])
            if run["run"]["category"] != None and not (run["run"]["category"] in allcategories):
                allcategories.append(run["run"]["category"])
            if not (run["run"]["game"] in allgames):
                allgames.append(run["run"]["game"])
            if run["place"] == 1:
                allwrs += 1
                if run["run"]["level"] == None:
                    allFGwrs += 1
                else:
                    allILwrs += 1
                gamesmostwrs.append(run["run"]["game"])
                if not run["run"]["game"] in allgameswithwrs:
                    allgameswithwrs.append(run["run"]["game"])
            if run["place"] <= 3:
                allpodiums += 1
        break
    print(fjson[id][0], len(list(fjson.keys()))-no2, len(pbs), len(alllevels), len(allcategories), len(allgames), allwrs, allFGwrs, allILwrs, allpodiums, len(pbs), len(allgameswithwrs))
    with open("outputs/pbsoutput.txt", "a") as p:
        if deleted:
            continue
        else:
            p.writelines(f"{id}, {len(alllevels)}, {len(allcategories)}, {len(allgames)}, {allwrs}, {allFGwrs}, {allILwrs}, {allpodiums}, {len(pbs)}, {len(allgameswithwrs)}, {gamesmostwrs.count(most_frequent(gamesmostwrs))}\n")

# LEADERBOARD

with open("outputs/pbsoutput.txt", "r") as o:
    output = "".join(o.readlines())
    # alllevels, allcats, allgames, allwrs, wrsFG, wrsIL, podiums, pbs, gameswithwrs, obsoletes, ratiodata
    lbs = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}]
    for i in output.split("\n"):
        if i == "":
            continue
        for it in range(len(lbs)):
            lbs[it].update({i.split(", ")[0]: int(i.split(", ")[it+1])})
    ratio = {}
    with open("database.json", "r") as datab:
        database = json.loads(datab.readlines()[0])
    for i in output.split("\n"):
        if i == "":
            continue
        userid = i.split(", ")[0]
        if lbs[3][userid] == 0:
            continue
        ratio.update({userid: (lbs[3][userid]/lbs[7][userid])*100})
    lbs.append(ratio)
    with open("outputs/runsoutput.txt", "r") as r:
        runso = r.readlines()
        obsoletes = {}
        for stat in range(len("".join(runso).split("\n"))):
            if "".join(runso).split("\n")[stat] == "":
                continue
            st = "".join(runso).split("\n")[stat].split(", ")
            obsoletes.update({st[0]: int(st[1])-int(output.split("\n")[stat].split(", ")[8])})
    lbs.append(obsoletes)

allcats = ["levels", "category", "games", "wrs", "wrsFG", "wrsIL", "podiums", "pbs", "gameswithwrs", "gameswithmostwrs", "ratiodata",  "obsoletes"]
for cat in allcats:
    with open(f"outputs/{cat}finallb.txt", "a") as flb:
        flb.truncate(0)
        nr, no, ibefore = 1, 1, 1
        for i in list(dict(sorted(lbs[allcats.index(cat)].items(), key=lambda item: item[1], reverse=True)).keys()):
            if not ibefore == 1:
                if not lbs[allcats.index(cat)][ibefore] == lbs[allcats.index(cat)][i]:
                    no = nr
            if cat != "ratiodata":
                flb.writelines(f'`{no}.`{database[i][1]}`{database[i][0]}' + " "*(26-(len(str(lbs[allcats.index(cat)][i]))+len(database[i][0])+len(str(no)))) + f'{lbs[allcats.index(cat)][i]}`\n')
            else:
                ratiod = f'{round(lbs[allcats.index(cat)][i], 2)}%`'
                flb.writelines(f'{database[i][1]}`{database[i][0]}' + " "*(32-(len(ratiod)+1+len(database[i][0])+len(str(no)))) + ratiod + '\n')
            nr+=1
            ibefore = i
