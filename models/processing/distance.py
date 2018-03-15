#! Python3 
# distance.py - use the google maps api to determine the distance between the place the match was played 
# and the schools that played in the the shorter distance is subtracted from the longer


import googlemaps, pickle, os, time
import psycopg2 as pg


gmaps = googlemaps.Client(key=os.environ["GMAPS"])

def db_connect():
    #connect to DB and return connection instance
    conn = pg.connect(database=os.environ['DB'], user=os.environ['USR'], password=os.environ['PW'], host=os.environ['ENDPNT'] ) 
    return conn
def db_end_session(connection, cursor):
    #commit changes to DB and end session gracefully. TO BE USED AT THE END OF EVERY SESSION
    connection.commit()
    cursor.close()
    connection.close()
    
    
def load_school_list():
    with open('schools.pickle', 'rb') as file:
        school_list = pickle.load(file)
    return list(school_list)
    
def auto_complete(lis):
    address_list = []
    for place in lis:
        query = place + ' University'
        print(query)
        time.sleep(2)
        place_list = gmaps.places(query)
        try:
            address_list.append([place, place_list['results'][0]['formatted_address']])
        except IndexError as e:
            print('Could not find university address')
    return address_list






def main():
    schools = load_school_list()
    school_addresses = auto_complete(schools)
    with open('addressed.pickle', 'wb') as f:
        pickle.dump(school_addresses, f)
    
    
main()