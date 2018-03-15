import psycopg2 as pg
import hashlib, os, random, pickle
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
import numpy as np


def db_connect():
    #connect to DB and return connection instance
    conn = pg.connect(database=os.environ['DB'], user=os.environ['USR'], password=os.environ['PW'], host=os.environ['ENDPNT'] ) 
    return conn
    
def db_end_session(connection, cursor):
    #commit changes to DB and end session gracefully. TO BE USED AT THE END OF EVERY SESSION
    connection.commit()
    cursor.close()
    connection.close()
    
def get_match_list():
    conn = db_connect()
    cur = conn.cursor()
    cur.execute('SELECT * FROM matches')
    matches = cur.fetchall()
    db_end_session(conn, cur)
    return matches
    
    
def make_arrays():
    vector_list = []
    results = []
    matches = get_match_list()
    for match in matches:
       data = vectorize(match)
       if data == None:
           continue
       vector_list.append(data[0])
       results.append(data[1])
    vectors = np.array(vector_list)
    return (vectors, results)
        
        
def vectorize(match):
    year = match[1]
    schools = [match[4], match[5]]
    winner = match[4]
    team1 = schools.pop(round(random.random()))
    team2 = schools[0]
    parameters1 = get_team_data(str(year), team1)
    parameters2 = get_team_data(str(year),team2 )
    if parameters1 == None or parameters2 == None:
        return None
    vector = [(param - parameters2[i]) for i, param in enumerate(parameters1)]
    result = 1 if winner == team1 else 0
    print(vector)
    return (vector, result)
    
   
    
def get_team_data(year, team):
    team = team.replace('-', ' ')
    hasher = hashlib.sha256()
    byte_str = (year + team).encode()
    hasher.update(byte_str)
    _id = hasher.digest()
    conn = db_connect()
    cur = conn.cursor()
    cur.execute('SELECT win_loss, pnts_per_game, opp_pnts_per_game, sos FROM teams WHERE id=%s;', (_id,)) 
    params = cur.fetchone()
    print(team, year)
    print('params: ', params)
    db_end_session(conn, cur)
    return params
    
#data = make_arrays()  

# with open('vectors.pickle', 'wb') as f:
#     pickle.dump(data, f)

def get_data():
    with open('./pickles/vectors.pickle', 'rb') as f:
        data = pickle.load(f)
    vectors = data[0]
    results = data[1]
    X_train, X_test, y_train,  y_test = train_test_split(vectors, results, test_size=0.05, random_state=9)
    
    scaler = preprocessing.StandardScaler()
    scaler.fit(vectors)
    
    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    with open('scale.pickle', 'wb') as scale:
        pickle.dump(scaler, scale)
    
    return (X_train_scaled, y_train, X_test_scaled, y_test)

    
