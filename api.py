import requests
from urllib import parse
import time


def requestLimit_statusCase(func):
    def wrapper(self,*args,**kwargs):
        time.sleep(1.21)

        data=func(self,*args,**kwargs)

        while self.status_code == 429: #정상 응답, 요청횟수추가
            print('error 429 요청횟수초과')
            print('1분 후 재실행')
            time.sleep(60)
            data = func(self, *args, **kwargs)
        if self.status_code == 200:
            pass
        elif self.status_code == 400: #bad request(입력이 잘못됨)
            print('error 400 잘못된 요청')
            print(f'{args}, {kwargs}')
            exit()
        elif self.status_code == 404: #데이터 없음(닉변이나 계삭)
            print('error 404 데이터 없음, 닉변 혹은 계삭..')
            return self.status_code
        elif self.status_code == 403: #API키 끝남
            print('KEY 유통기한 지남')
            self.KEY=input('type riot API KEY\n')
            data = func(self, *args, **kwargs)
        else:
            print(self.status_code)
        return data
    return wrapper



class useAPI:
    def __init__(self,tier,start_time, end_time, KEY=input('type riot API KEY\n')):
        self.tier = tier
        self.KEY = KEY
        self.start_time = start_time
        self.end_time = end_time
        self.status_code = 200


    #티어를 입력하면 해당 티어 2등급구간의 활동중인 서모너네임 205개가량(한 페이지)를 가져오는 함수
    @requestLimit_statusCase
    def getSummonerName(self,page): # II구간 get
        APIURL = f"https://kr.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/{self.tier}/II?page={page}&api_key={self.KEY}"
        res = requests.get(APIURL)
        self.status_code = res.status_code
        data = res.json()
        data = [x['summonerName'] for x in data if x['inactive'] == False]
        return data

    #get puuid
    @requestLimit_statusCase
    def getPuuid(self,summonerName): 
        encodedSummonerName = parse.quote(summonerName)
        APIURL = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{encodedSummonerName}?api_key={self.KEY}"
        res = requests.get(APIURL)
        self.status_code = res.status_code
        data = res.json()
        return data
        

    #get MatchId
    @requestLimit_statusCase
    def getMatchId(self,puuid): 
        APIURL = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?startTime={self.start_time}&endTime={self.end_time}&type=ranked&start=0&count=100&api_key={self.KEY}"
        res = requests.get(APIURL)
        self.status_code = res.status_code
        data = res.json()
        return data


    #getMatch
    @requestLimit_statusCase
    def getMatch(self,matchId):
        APIURL = f"https://asia.api.riotgames.com/lol/match/v5/matches/{matchId}?api_key={self.KEY}"
        res = requests.get(APIURL)
        self.status_code = res.status_code
        data = res.json()
        return data
