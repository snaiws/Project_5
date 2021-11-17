# Project_5
##AI 기반 롤 닷지 웹 어플리케이션   

Riot API로 데이터를 모아 분석을 하여 모델을 만든 후   
아군 챔피언 5개, 적 챔피언 5개를 입력했을 때 승패예측을 하도록 하는게 목표입니다.   
입력으로 아군 유저ID를 입력하여 챔피언숙련도나 최근전적에 따라 승패예측에 도움을 주도록 하려했으나   
Riot API의 제한이 커서 아직 구현하지 못했습니다.   

--------------------------------------------------------------------

[Riot API][Riot API Link]
[Riot API Link]: https://developer.riotgames.com/ "이동"

API KEY : 24시간 제한   
1.2초당 1회 request 권장   

매치데이터 얻는 과정   
1. LEAGUE-EXP-V4(League of Legends)를 통해 summonerName 리스트 얻기   
2. SUMMONER-V4(League of Legends)를 통해 각 summonerName의 puuid 얻기   
3. MATCH-V5(League of Legends)를 통해 puuid마다 matchId 리스트를 얻기   
4. MATCH-V5(League of Legends)를 통해 matchId 마다 match정보를 얻기   

----------------------------------------------------------------------

api.py : api 요청을 하는 클래스가 있습니다.   
config.py : postgresql 파라미터를 적용하는 함수입니다.   
database.ini : postgresql 파라미터입니다.   


DDL.py : postgresql의 data definition language를 제어하는 코드입니다.   
get_data.py : API를 통해 데이터를 받아 postgresql로 저장하는 코드입니다.   
data : api로 얻은 데이터의 postgresql 백업파일입니다.   


only_champ_deep_data.py : postgresql에 저장된 데이터 중 매치당 10개의 챔피언, 승패여부를 불러와 csv로 저장하는 코드입니다.   
ocdd.csv : 위 코드를 통해 저장된 데이터입니다.   
ocdd.ipynb : 위 데이터를 분석하는 코드입니다.   
ocdd_FE.csv : ocdd.ipynb에서 피쳐 엔지리어링 한 데이터입니다.  


wrangle_and_deep_data.py : 챔피언 말고도 여러 특성들을 추가로 불러와 csv로 저장하는 코드입니다.   