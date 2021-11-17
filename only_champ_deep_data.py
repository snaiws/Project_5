import psycopg2
from config import config
import os
import pandas as pd

#postgreSQL 연결
def connect(): 
    """ Connect to the PostgreSQL database server """
    conn = None
    # read connection parameters
    params = config()

    # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(**params)
    
    # create a cursor
    cur = conn.cursor()

    cur.execute("SELECT * FROM matchid;")
    data = cur.fetchall()
    df = pd.DataFrame()
    df['matchId'] =[i[0] for i in data]
    for i in range(1,11):
        df[f'champ{i}'] = None
    df.set_index('matchId',inplace=True)
    df['win']=None
    print(df)

    cur.execute("SELECT * FROM MATCH;")
    data = cur.fetchall()
    for i in data:
        df[f'champ{i[5]}'][i[1]] = i[6]
        if not df['win'][i[1]]:
            if i[5]<6:
                df['win'][i[1]] = int(i[24])
            else:
                df['win'][i[1]] = int(not i[24])

    df1=df[:]
    df1=df1.reset_index()
    df1['matchId'] = df1['matchId']+'R'
    df1=df1.set_index('matchId')
    df1=df1.rename(columns={'champ1':'champ6','champ2':'champ7','champ3':'champ8','champ4':'champ9','champ5':'champ10','champ6':'champ1','champ7':'champ2','champ8':'champ3','champ9':'champ4','champ10':'champ5'})
    df1['win'] = abs(df1['win']-1)
    df=pd.concat([df,df1])
    df.to_csv(os.path.join(os.getcwd(),r'ocdd.csv'), encoding='utf-8')

# close the communication with the PostgreSQL
    conn.commit()
    cur.close()
    if conn is not None:
        conn.close()
        print('Database connection closed.')
    return df

if __name__ == '__main__':
    connect()