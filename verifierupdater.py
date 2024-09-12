import requests, json, time
src = "https://www.speedrun.com/api/v1/"

with open("vdatabase.json", "r") as f:
    fjson = json.loads(f.readlines()[0])
#with open("outputs/verifieroutput.txt", "w") as v:
#    v.truncate(0)
no = 0
usersid = ""
t = time.time()
fjsonk = list(fjson.keys())[:] #list(fjson.keys()).index("86n5knqx")
while True:
    if usersid != "":
        fjsonk = list(fjson.keys())[list(fjson.keys()).index(usersid):]
        print(usersid)
    try:
        for user in fjsonk:
            usersid = user
            print(fjson[user][0], len(list(fjson.keys()))-list(fjson.keys()).index(user))
            if fjson[user][0] in ["dha", "1", "Reni", "jensj56"]:
                continue
            allruns = []
            lastrun = {"id": "whadohdwao///"}
            breakeverything = False
            deleted = False
            for dir in ["asc", "desc"]:
                offset = 0
                while offset < 10000:
                    while True:
                        try:
                            if time.time() - t < 0.8:
                                time.sleep(0.8 - (time.time() - t))
                            runs = requests.get(src + f"runs?examiner={user}&direction={dir}&max=200&offset={offset}&orderby=date").json()
                            t = time.time()
                            if "status" in list(runs.keys()):
                                if runs["status"] == 404:
                                    deleted = True
                                    break
                                else:
                                    print("We're getting rate limited!")
                                    time.sleep(10)
                                    continue
                            break
                        except Exception:
                            print("We're getting rate limited!")
                            time.sleep(10)
                            continue
                    if deleted:
                        break
                    runs = runs["data"]
                    for run in runs:
                        if len(run["players"]) > 0:
                            if run["players"][0]["rel"] == "guest":
                                if run["players"][0]["name"].lower() == "n/a" or run["players"][0]["name"].lower() == "n\a":
                                    continue
                        else:
                            continue
                        if run["id"] == lastrun["id"]:
                            breakeverything = True
                            break
                        allruns.append(run)
                    if len(runs) < 200 or breakeverything:
                        break
                    offset += 200
                if offset != 10000:
                    break
                lastrun = allruns[-1]
                print(len(allruns)) 
            with open("outputs/verifieroutput.txt", "a") as f:
                if deleted:
                    continue
                else:
                    f.writelines(f"{user}, {len(allruns)}\n")
        break
    except Exception:
        continue

# 1DHARENI

time.sleep(30)

import onedhareni
            
# LEADERBOARD

with open("outputs/verifieroutput.txt", "r") as o:
    output = "".join(o.readlines())
    lb = {}
    for i in output.split("\n"):
        lb.update({i.split(", ")[0]: int(i.split(", ")[1])})
with open("outputs/verifierfinallb.txt", "a") as flb:
    flb.truncate(0)
    nr, no, ibefore = 1, 1, []
    print(list(dict(sorted(lb.items(), key=lambda item: item[1], reverse=True)).keys()))
    for i in list(dict(sorted(lb.items(), key=lambda item: item[1], reverse=True)).keys()):
        with open("vdatabase.json", "r") as datab:
            if lb[i] != ibefore:
                no = nr
            database = json.loads(datab.readlines()[0])
            flb.writelines(f'`{no}.`{database[i][1]}`{database[i][0]}' + " "*(27-(len(f"{no}"))-(len(str(lb[i]))+len(database[i][0]))) + f'{lb[i]}`\n')
            nr+=1
            ibefore = lb[i]
