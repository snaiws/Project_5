# Project_5
딥러닝 기반 롤 닷지 웹 어플리케이션   

개발자모드   
op.gg 혹은 라이엇api로 특정 버전의 티어별 데이터 받기   
데이터 전처리   

입력층   
우리팀챔피언5개+우리팀 해당챔피언판수+우리팀 해당챔피언승률(없을 시 50%)+우리팀 최근5판전적+적팀챔피언5개   

출력층   
우리팀이 이기는가 지는가   

이러면 한 경기당 데이터가 2개 생김   

딥러닝 후 학습된 모델을 업데이트   

웹어플리케이션에서 수동으로 우리팀 닉네임 입력   
우리팀 선택 챔피언 입력, 적팀 챔피언 입력   

run 버튼 클릭시 우리팀 정보를 검색하고 딥러닝모델에 입력해서 결과도출, 출력   

------------------------------------------   
이미지 딥러닝 너무 공부해야할게 많아서 이걸 코드스테이츠 마지막 개인프로젝트로 하기로 함   

우선 시간이 없으니 버전을 나누기로 함   

버전1 : 챔피언 조합으로만 딥러닝   

버전1.5 : 웹어플리케이션 연결

버전2 : 유저의 전적을 추가하여 딥러닝   

버전 2.5 : 어제의 학습 이후 쌓인 데이터로 오늘 추가 학습하는 코드로 작성   

버전3 : 유저 전적의 트렌드로 딥러닝   

이 후 프로젝트2에 접목   

#프로젝트5 v1.0   
인풋으로 우리팀 챔프와 적챔프를 넣으면 승패 예측   
예상되는 문제점 : 승패예측을 하고 모델의 예측률을 보여주게될것이다. 그런데, 인풋이 어떤가에 따라 예측률이 높아질 수 있고 낮아질 수 있는것 아닌가? 예를들어 예측정확도 0.85인데, 우리팀 조합이 티모 니달리 럭스 케이틀린 유미일때랑 티모 리신 리산드라 잔나 케이틀린일때랑 똑같이 진다는 예측이 나오더라도 그 확률이 다른것 아닌가?   


progress   
API 시도   
최근버전의 모든전적데이터 받기(챔피언, 승패여부만)   
딥러닝 돌리기   
예측정확도 계산해보고 파라미터 조절   
웹어플리케이션 적용   

----------------------------------   

라이엇 API의 기능이 매우 제한됨. op.gg는 그 제한된 기능으로 차곡차곡 데이터를 모아서 통계를 낸것. 즉 롤 api로 과거 매치데이터를 얻기는 힘듬. 일단 라이엇데이터스키마를 그려보자. 
나도 데이터를 축적하면 좋겠다만 용량이 상당히 클거같다. 그리고 과거데이터 접근이 불가능한거같은데 달리 방법이 없는지 더 찾아봐야한다   
근데 진짜 이런거 너무 싫다. 그 웹만드는 템플릿사이트도 기능이 있나없나 찾느라 시간 엄청보냈는데, 차라리 자스랑 css를 공부를하지, 어떤사람은 플젝2주짜리 기간동안 여기에 몰입햇더만. 라이엇 api도 있는지 없는지 되는지 안되는지 직접 하나하나찾아야해서 시간 버리네   
------------------------------------
라이엇피셜:   
Very unlikely. Again, we do not own this service, so it's not up to us. However, I can tell you that the amount of game data that has to be stored across all regions and shards for 3 years is insanely massive, and there is a huge resource and operational cost to Riot to store all that. Thus, it is very unlikely. Also note that 1) any trends on game data older than 3 years is unlikely to be very relevant given how much League changes each season and 2) you are welcome to store all the data you fetch, so that as time passes you will build up many more years worth of data that you have stored and can run trends on.   
결국 opgg를 해킹하거나 최근데이터만 사용해야함

----------------------------------------
직접 유저를 뽑아서 유저의 최근 전적을 모아 일회성 데이터로 활용하기로 했다.   
그런데 또 문제가 발생했다.   
챔프+아군의 챔프전적으로 딥러닝하려했는데, 어떤 경기 시작 직전 아군의 챔프 전적을 못구한다.   
그래서 최근1~5경기 전 이기고 졌는가를 고려하기로 했다.   
이 db를 그대로 프로젝트2에 써먹기 위해 RDBMS를 쓰기로 했다.   
postgresql이 mysql보다 insert가 빠르다하여 이걸 쓰기로 했다.   
