#!python3
#load_db.py - loads scraped data into postgres for better access


import os, pickle, re, hashlib
import psycopg2 as pg


def db_connect():
    #connect to DB and return connection instance
    conn = pg.connect(database=os.environ['DB'], user=os.environ['USR'], password=os.environ['PW'], host=os.environ['ENDPNT'] ) 
    return conn
    
def db_end_session(connection, cursor):
    #commit changes to DB and end session gracefully. TO BE USED AT THE END OF EVERY SESSION
    connection.commit()
    cursor.close()
    connection.close()
    
def create_tables():
    conn =  db_connect()
    cur = conn.cursor()
    #cur.execute("CREATE TABLE matches (id serial PRIMARY KEY, year int, region varchar(20), round int, winner varchar(30), loser varchar(30), location varchar(30));")
    cur.execute("CREATE TABLE teams (id bytea, year int, team_name varchar(30), win_loss float, pnts_per_game float, opp_pnts_per_game float, sos float);")
    db_end_session(conn, cur)
# # Data base schema can be seen above two tables one with teams one with matches details are:
# #   matches - id serial Primary key, year int(year the match took place), round int (the round number 1-6, 6 is national championship), winner varchar(20)(winning team name),
# #             loser varchar(20)(losing team name)
# #   teams - id bytea PRIMARY KEY(a hash of the team name and the year played for easier lookup), year int (year played), team_name varchar(20)(name of the team)
# #           win_loss float (the teams win loss percentage), pnts_per_game float(the average points scored per game by this team), opp_pnts_per_game float
# #           (the average points scored by this teams opponents), sos float (this teams strength of shcedule)

def load_in_pickle(file_path):
    with open(file_path, 'rb') as f:
        data = pickle.load(f)
    return data
    

        
def tablize_winner_data(data):
    master_list = []
    for key in data.keys():
        year = key
        for key1 in data[key].keys():
            region = key1
            for rnd in data[key][key1]:
                if(key1 == 'national'):
                    level =  int(rnd) + 4
                else:
                    level = int(rnd)
                for match in data[key][key1][rnd]:
                    if len(match)  == 1:
                        continue
                    match_list = [0 for i in range(6)]
                    match_list[0] = year
                    match_list[1] = region
                    match_list[2] = level
                    winner_reg = re.compile(r'[(][^)]+[)]')
                    for item in match:
                        if 'at ' in item:
                            loc = item.replace('at ', '')
                            match_list[5] = loc
                        elif winner_reg.match(item) != None:
                            winner = winner_reg.match(item).group(0).strip('(').strip(')')
                            match_list[3] = winner
                        else:
                            loser = item
                            match_list[4] = loser
                    master_list.append(tuple(match_list))
    return master_list
    
def tablize_teams_data(data):
    table_data = []
    for year in data.keys():
        date = year
        for conf in data[year].keys():
            for team in data[year][conf].keys():
                instance = data[year][conf][team]
                school = str.lower(team).replace('-', ' ').replace('(', '').replace(')', '')
                hasher = hashlib.sha256()
                encoded_str = (date + school).encode()
                hasher.update(encoded_str)
                _id = hasher.digest()
                table_data.append([_id, year, school, instance['Win-Loss'],  instance['pts_per_g'], instance['opp_pts_per_g'], instance['Str_of-Sched']])
    return table_data
                
def drop_tables():
    con = db_connect()
    cur = con.cursor()
    try:
        
        cur.execute('DROP TABLE teams;')
        
    except pg.ProgrammingError as e:
        print('table: teams  does not exisit')
        
    try:
        cur.execute('DROP TABLE matches;')
    except pg.ProgrammingError as e:
        print('table: matches does not not exist')
    db_end_session(con, cur)
     
        
def main():
    #drop_tables()
    #create_tables()
    data =  load_in_pickle('./pickles/new_winners.pickle')
    data1 = load_in_pickle('./pickles/years.pickle')
    del data['1939']
    del data1 ['1939']
    winner_list = tablize_winner_data(data)
    teams_list = tablize_teams_data(data1)
    conn = db_connect()
    cur = conn.cursor()
    for item in winner_list:
        if item[1] == 'bracket':
            continue
        print(item)
        cur.execute("INSERT INTO matches (year, region, round, winner, loser, location) VALUES(%s, %s, %s, %s, %s, %s);", item)
    for item in teams_list:
        print(item)
        for i, stat in enumerate(item):
            if stat == '':
                item[i] = 0.0
        cur.execute('INSERT INTO teams (id, year, team_name, win_loss, pnts_per_game, opp_pnts_per_game, sos) VALUES(%s, %s, %s, %s, %s, %s, %s);', item)
    db_end_session(conn, cur)
    
main()
