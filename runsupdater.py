import requests, json, time
src = "https://www.speedrun.com/api/v1/"

with open("database.json", "r") as f:
    fjson = json.loads(f.readlines()[0])
no, no2 = 0, 0
t = time.time()
for id in fjson:
    allruns = []
    totaltime = 0
    runsIL = 0
    runsFG = 0
    no2 += 1
    lastrun = {"id": "whadohdwao///"}
    breakeverything = False
    deleted = False
    for dir in ["asc", "desc"]:
        offset = 0
        while offset < 10000:
            if time.time() - t < 0.8:
                time.sleep(0.8 - (time.time() - t))
                t = time.time()
            runs = requests.get(src + f"runs?user={id}&direction={dir}&max=200&offset={offset}&orderby=date&status=verified").json()
            no += 1
            if "status" in list(runs.keys()):
                if runs["status"] == 404:
                    deleted = True
                    break
                else:
                    print("We're getting rate limited!")
                    time.sleep(10)
                    continue
            runs = runs["data"]
            for run in runs:
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
    for run in allruns:
        totaltime += run["times"]["primary_t"]
        if run["level"] == None:
            runsFG += 1
        else:
            runsIL += 1
    print(fjson[id][0], len(list(fjson.keys()))-no2, len(allruns), runsFG, runsIL, totaltime, runsFG + runsIL == len(allruns))
    with open("outputs/runsoutput.txt", "a") as output:
        if deleted:
            continue
        else:
            output.writelines(f"{id}, {len(allruns)}, {runsFG}, {runsIL}, {totaltime}\n")

# LEADERBOARDS

def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    
    hours_str = str(hours)
    minutes_str = str(minutes).zfill(2)
    seconds_str = str(seconds).zfill(2)

    time_str = f"{hours_str}h {minutes_str}m {seconds_str}s"
    return time_str

with open("outputs/runsoutput.txt", "r") as o:
    output = "".join(o.readlines())
    rlb, rILlb, rFGlb, ttlb = {}, {}, {}, {}
    for i in output.split("\n")[:-1]:
        rlb.update({i.split(", ")[0]: int(i.split(", ")[1])})
        rFGlb.update({i.split(", ")[0]: int(i.split(", ")[2])})
        rILlb.update({i.split(", ")[0]: int(i.split(", ")[3])})
        ttlb.update({i.split(", ")[0]: round(float(i.split(", ")[4]))})

for file in [["runsfinallb", rlb], ["runsFGfinallb", rFGlb], ["runsILfinallb", rILlb]]:
    with open("outputs/" + file[0] + ".txt", "a") as flb:
        flb.truncate(0)
        nr, no, ibefore = 1, 1, 1
        with open("database.json", "r") as datab:
            database = json.loads(datab.readlines()[0])
            for i in list(dict(sorted(file[1].items(), key=lambda item: item[1], reverse=True)).keys()):
                if ibefore != 1:
                    if not file[1][ibefore] == file[1][i]:
                        no = nr
                flb.writelines(f'`{no}.`{database[i][1]}`{database[i][0]}' + " "*(26-(len(str(file[1][i]))+len(database[i][0])+len(str(no)))) + f'{file[1][i]}`\n')
                nr+=1
                ibefore = i

with open("outputs/totaltimefinallb.txt", "a") as flb:
    flb.truncate(0)
    nr, no, ibefore = 1, 1, 1
    with open("database.json", "r") as datab:
        database = json.loads(datab.readlines()[0])
        for i in list(dict(sorted(ttlb.items(), key=lambda item: item[1], reverse=True)).keys()):
            if ibefore != 1:
                if not ttlb[ibefore] == ttlb[i]:
                    no = nr
            convert = format_time(ttlb[i])
            flb.writelines(f'`{no}.`{database[i][1]}`{database[i][0]}' + " "*(40-(len(convert)+1+len(database[i][0])+len(str(no)))) + convert + '`\n')
            nr+=1
            ibefore = i