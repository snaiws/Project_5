import psycopg2, time, requests, datetime
from config import config
from api import useAPI

#postgreSQL 연결
def connect(): 

    # Connect to the PostgreSQL database server
    conn = None 
    params = config() # read connection parameters
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(**params) # connect to the PostgreSQL server
    cur = conn.cursor() # create a cursor

    # create table if there is no table
    cur.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';""")
    if cur.fetchall() == []:
        creatTable = (
            """
            CREATE TABLE MATCHID(
                matchId VARCHAR(15) PRIMARY KEY,
                version VARCHAR(15) NOT NULL,
                tier VARCHAR(15) NOT NULL,
                hasMatch BOOL NOT NULL
                FOREIGN KEY (version)
                REFERENCES VERSION (version)
                ON UPDATE CASCADE ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE MATCH(
                id SERIAL PRIMARY KEY,
                matchId VARCHAR(15) NOT NULL,
                summonerName VARCHAR(31) NOT NULL,
                puuid VARCHAR(63) NOT NULL,
                teamPosition VARCHAR(7) NOT NULL,
                participantId INT NOT NULL,
                championName VARCHAR(15) NOT NULL,
                gameDuration INT NOT NULL,
                champExperience INT NOT NULL,
                champLevel INT NOT NULL,
                goldEarned INT8 NOT NULL,
                kills INT NOT NULL,
                deaths INT NOT NULL,
                assists INT NOT NULL,
                totalMinionsKilled INT NOT NULL,
                neutralMinionsKilled INT NOT NULL,
                visionScore INT NOT NULL,
                totalDamageDealtToChampions INT8 NOT NULL,
                totalTimeCCDealt INT NOT NULL,
                timeCCingOthers INT NOT NULL,
                firstBloodAssist BOOL NOT NULL,
                firstBloodKill BOOL NOT NULL,
                firstTowerAssist BOOL NOT NULL,
                firstTowerKill BOOL NOT NULL,
                win BOOL NOT NULL,
                FOREIGN KEY (matchId)
                REFERENCES MATCHID (matchId)
                ON UPDATE CASCADE ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE PUUID(
                summonerName VARCHAR(31) PRIMARY KEY,
                puuid VARCHAR(63),
                hasMatchId BOOL NOT NULL
            """,
            """
            CREATE TABLE VERSION(
                version VARCHAR(15) PRIMARY KEY,
                start_time VARCHAR(15) NOT NULL,
                end_time VARCHAR(15) NOT NULL,
                summoner_name_done BOOL NOT NULL,
                puuid_done BOOL NOT NULL,
                matchlist_done BOOL NOT NULL,
                match_done BOOL NOT NULL
            """)
        for creatTable in creatTable:
            cur.execute(creatTable)
            print('table created')


    #시작
    cur.execute('SELECT * FROM VERSION;')
    versions = cur.fetchall()
    if versions == []:
        print('저장된 데이터 없음')
        version = input('version 입력 ex)11.22처럼 XX.XX\n')
        start_time = input('업데이트 날짜 입력 ex) 2021년 11월 3일 -> 20211103\n')
        y, m, d = int(start_time[:4]), int(start_time[4:6]), int(start_time[6:])
        start_time = str(int((datetime.datetime(y,m,d,11,0) - datetime.datetime(1970,1,1)).total_seconds()))
        end_time = input('수집할 마지막 날짜 입력\n')
        y, m, d = int(end_time[:4]), int(end_time[4:6]), int(end_time[6:])
        end_time = str(int((datetime.datetime(y,m,d,11,0) - datetime.datetime(1970,1,1)).total_seconds()))
        cur.execute(f"INSERT INTO VERSION (version, start_time, end_time, summoner_name_done, puuid_done, matchlist_done, match_done) VALUES({version}, {start_time}, {end_time}, FALSE, FALSE, FALSE, FALSE);")
        conn.commit()
    else:
        for i in versions:
            print(versions)
        version = input('version 입력\n')
        cur.execute(f"SELECT * FROM VERSION WHERE version = '{version}';")
        versions = cur.fetchall()
        start_time = versions[1]
        end_time = version[2]
        summoner_name_done = version[3]
        puuid_done = version[4]
        matchlist_done = version[5]
        match_done = version[6]

    #tier = input('티어 입력(영어 대문자)\n')
    tier = 'DIAMOND'
    getData = useAPI(tier,start_time,end_time)

    

    #getSummonerName
    if not summoner_name_done:
        beforeAPI=0
        afterAPI=0
        n=1
        sList=[]
        while True:
            beforeAPI = len(sList)
            sList = sList + getData.getSummonerName(n)
            n +=1
            print(f'getting summoner name ..({len(sList)}개 수집)')
            afterAPI = len(sList)
            if beforeAPI == afterAPI:
                break
        sList=list(set(sList))
        for i in sList:
            cur.execute(f"INSERT INTO PUUID (puuid, summonerName,hasMatchId) VALUES({i}, null, FALSE);")
        cur.execute(f'UPDATE version SET summoner_name_done = TRUE WHERE version = {version};')
        conn.commit()


    #getPuuid
    if not puuid_done:
        cur.execute(f"SELECT summonerName FROM PUUID where puuid is null;")
        sList = [i[0] for i in cur.fetchall()]
        for i in sList:
            print(f'getting puuid of {(i)}..')
            data = getData.getPuuid(i)
            if data != 404:
                cur.execute(f"UPDATE PUUID SET puuid = {data['puuid']} WHERE summonerName = {i};")
            elif data == 404:
                cur.execute(f"DELETE FROM PUUID WHERE summonerName = {i};")
            conn.commit()
        cur.execute(f'UPDATE version SET puuid_done = TRUE WHERE version = {version};')
        conn.commit()

    #getMatchId
    if not matchlist_done:
        cur.execute(f"SELECT * FROM PUUID where hasMatchList = FALSE;")
        sDict = {}
        for i, j in cur.fetchall():
            sDict[i]=j
        mList=[]
        for i in sDict:
            print(f'getting match IDs of {i}..')
            matchId=getData.getMatchId(sDict[i])
            if matchId == None:
                continue
            for j in matchId:
                if j not in mList:
                    cur.execute(f"INSERT INTO MATCHID (matchId, version, tier, hasMatch) VALUES({j},{version},{tier},FALSE)")
                    cur.execute(f"UPDATE PUUID SET hasMatchList = TRUE WHERE summonerName = {i};")
                    conn.commit()
                    mList.append(j)
        cur.execute(f'UPDATE version SET matchlist_done = TRUE WHERE version = {version};')
        conn.commit()


    #getMatch
    if not match_done:
        cur.execute(f"SELECT matchId FROM MATCHID where hasMatch = FALSE;")
        mList = [i[0] for i in cur.fetchall()]
        for i in mList:
            print(f'getting match {i}..')
            match, gameDuration = getData.getMatch(i)
            gameDuration = match['info']['gameDuration']
            match = match['info']['participants']
            for j in match:
                cur.execute(f"INSERT INTO MATCH (id, matchId, summonerName, puuid, teamPosition, participantId, championName, gameDuration, champExperience, champLevel, goldEarned, kills, deaths, assists, totalMinionsKilled, neutralMinionsKilled, visionScore, totalDamageDealtToChampions, totalTimeCCDealt, timeCCingOthers, firstBloodAssist, firstBloodKill, firstTowerAssist, firstTowerKill, win) VALUES(DEFAULT, {i}, {j['summonerName']}, {j['puuid']}, {j['teamPosition']}, {j['participantId']}, {j['championName']}, {gameDuration}, {j['champExperience']}, {j['champLevel']}, {j['goldEarned']}, {j['kills']}, {j['deaths']}, {j['assists']}, {j['totalMinionsKilled']}, {j['neutralMinionsKilled']}, {j['visionScore']}, {j['totalDamageDealtToChampions']}, {j['totalTimeCCDealt']}, {j['timeCCingOthers']}, {j['firstBloodAssist']}, {j['firstBloodKill']}, {j['firstTowerAssist']}, {j['firstTowerKill']}, {j['win']});")
            cur.execute(f"UPDATE MATCHID SET hasMatch = TRUE WHERE matchId = {i}")
            conn.commit()
        cur.execute(f'UPDATE version SET match_done = TRUE WHERE version = {version};')
        conn.commit()
        

# close the communication with the PostgreSQL
    conn.commit()
    cur.close()

    if conn is not None:
        conn.close()
        print('Database connection closed.')

if __name__ == '__main__':
    connect()