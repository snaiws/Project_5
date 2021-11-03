import psycopg2
from config import config

import requests
from urllib import parse
import pandas as pd
import time

#postgreSQL 연결
def connect(): 
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
       
	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally: #여기가 메인 함수인듯
        if conn is not None:
            conn.close()
            print('Database connection closed.')


#버전,티어별 닉넴 뽑기
def getSummonerName(tier,page,KEY): # II구간 get
  APIURL = f"https://kr.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/{tier}/II?page={page}&api_key={KEY}"
  res = requests.get(APIURL)
  data = res.json()
  data = [x['summonerName'] for x in data if x['inactive'] == False]
  return data

  #get puuid
def getPuuid(summonerName,KEY): #나중에 쓸 일 있을 수도 있으니 DB로 저장
  encodedSummonerName = parse.quote(summonerName)
  APIURL = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{encodedSummonerName}?api_key={KEY}"
  res = requests.get(APIURL)
  data = res.json()
  return data['puuid']

  #get MatchId
def getMatchId(puuid,KEY): #나중에 쓸 일 있을 수도 있으니 DB로 저장
  APIURL = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?type=ranked&start=0&count=30&api_key={KEY}"
  res = requests.get(APIURL)
  data = res.json()
  return data

  #getMatch
def getMatch(matchId,KEY): #나중에 쓸 일 있을 수도 있으니 DB로 저장
  APIURL = f"https://asia.api.riotgames.com/lol/match/v5/matches/{matchId}?api_key={KEY}"
  res = requests.get(APIURL)
  data = res.json()
  version = data['info']['gameVersion']
  data = data['info']['participants']
  data = [[x['individualPosition'],x['championName'],x['win']] for x in data]
  return version, data

def getData(tier,version,KEY):
  df = pd.DataFrame()
  while len(df) < 50000:
  summonerList = getSummonerName('DIAMOND','1',KEY)
  summonerList = [getPuuid(x,KEY) for x in summonerList]
  matchList = []
  for i in summonerList:
    matchList = matchList + getMatchId(i,KEY)
  matchList = list(set(matchList))
  for i in matchList:
    getMatch(matchId,KEY)


#최신버전 불러오기
def getRecentVersion(KEY):
  

if __name__ == '__main__':
    KEY = input()
    connect()