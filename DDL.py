import psycopg2
from config import config

def connect(): 
    conn = None
    params = config()
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    
    def showTable():
        print('------------------------------------------------------------------------------')
        cur.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';""")
        for i in cur.fetchall():
            cur.execute(f"""SELECT * FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '{i[0]}';""")
            table = cur.fetchall()
            print(f'table : {table[0][2]}')
            print(f'col name | DATATYPE')
            for i in range(len(table)):
                print(f'{table[i][3]} : {table[i][27]}')
            print('...')
        print('------------------------------------------------------------------------------')

    def confirm(SQL):
        print('...')
        print(SQL)
        proceed = input('go? (y/n)\n')
        if proceed == 'y':
            print('3')
            cur.execute(SQL)
            print('2')
            conn.commit()
            print('1')
            print('DONE!')
        showTable()
    showTable()
    work = ''
    while work != 'END':
        work = input('TABLE : CREATE ALTERCOL DROP RENAME TRUNCATE END\n')
        if work =='CREATE':
            table = input('table name ? ')
            SQL = f'''CREATE TABLE {table}(
                temp SERIAL PRIMARY KEY
            );'''

            print('ALTER 기능으로 columns 추가하세요')
            confirm(SQL)
            
        if work =='ALTERCOL':
            alter = ''
            while alter != 'END':
                alter = input('ALTER : ADDCOL, COLNAME, DATATYPE, DEFAULT, NOTNULL, DROP, END\n')

                if alter == 'ADDCOL':
                    keyType = input('KEY : P, aP, F, N (primary, auto increment, foreign, none)\n')
                    if keyType == 'P':
                        print(r'ex) ALTER TABLE {table name} ADD COLUMN {column name} {data type} PRIMARY KEY;')
                    elif keyType == 'aP':
                        print(r'ex) ALTER TABLE {table name} ADD COLUMN {column name} serial PRIMARY KEY;')
                    elif keyType == 'F':
                        print(r'ex) ALTER TABLE {table name} ADD COLUMN {column name} REFERENCES {table}({col});')
                    elif keyType == 'N':
                        print(r'ex) ALTER TABLE {table name} ADD COLUMN {column name} {data type} {NOT NULL} {DEFAULT} {default value};')
                    SQL = input('type SQL')
                    confirm(SQL)
                        
                if alter == 'COLNAME':
                    table = input('which table ?\n')
                    old = input('old col name ?\n')
                    new = input('new col name ?\n')
                    SQL = f'ALTER TABLE {table} RENAME COLUMN {old} TO {new};'
                    confirm(SQL)
                    
                if alter == 'DATATYPE':
                    table = input('which table ?\n')
                    col = input('which col ?\n')
                    dType = input('new data type ?\n')
                    SQL = f'ALTER TABLE {table} ALTER COLUMN {col} TYPE {dType};'
                    confirm(SQL)

                if alter == 'DEFAULT':
                    sORd = input('DERAULT : SET / DROP ?\n')
                    table = input('which table ?\n')
                    col = input('which col ?\n')
                    if sORd == 'SET':
                        sORd = input('default value ?\n')
                        SQL = f'ALTER TABLE {table} ALTER COLUMN {col} SET DEFAULT {sORd};'
                    elif sORd == 'DROP':
                        SQL = f'ALTER TABLE {table} ALTER COLUMN {col} DROP DEFAULT;'
                    confirm(SQL)

                if alter == 'NOTNULL':
                    sORd = input('NOT NULL : SET / DROP ?\n')
                    table = input('which table ?\n')
                    col = input('which col ?\n')
                    SQL = f'ALTER TABLE {table} ALTER COLUMN {col} {sORd} NOT NULL;'
                    confirm(SQL)

                if alter == 'DROP':
                    table = input('which table ?\n')
                    col = input('which col ?\n')
                    SQL = f'ALTER TABLE {table} DROP COLUMN {col};'
                    confirm(SQL)

        if work =='DROP':
            table = input('which table ?\n')
            cascade = input('cascade ? (y/n)\n')
            if cascade == 'y':
                cascade = ' CASCADE'
            else:
                cascade = ''
            SQL = f'DROP TABLE {table}{cascade};'
            confirm(SQL)

        if work =='RENAME':
            old = input('old table name ?\n')
            new = input('new table name ?\n')
            SQL = f'ALTER TABLE {old} RENAME TO {new};'
            confirm(SQL)

        if work =='TRUNCATE':
            table = input('which table ?\n')
            SQL = f'TRUNCATE TABLE {table};'
            confirm(SQL)
    
    conn.commit()
    cur.close()
    if conn is not None:
        conn.close()
        print('Database connection closed.')

if __name__ == '__main__':
    connect()