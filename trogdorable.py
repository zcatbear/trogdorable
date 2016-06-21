import sqlite3
from haversine import haversine
import geopy
#from geopy.distance import great_circle, vincenty
import argparse

parser = argparse.ArgumentParser(description="This script finds the ASNs within the surrounding area provided the threshold")
parser.add_argument("-d", "--database", help="This is the name and location of the database")
parser.add_argument("-t", "--threshold", help="This is the radius of the surrounding area you would like to search within", default=100)
parser.add_argument("-a", "--address", help="This is the address that you want to leave from, can be country, state, city or street address", required=True)


args = parser.parse_args()
#Give it the location of your database
connection = sqlite3.connect(args.database)

#Area limits, Default 100
threshold = int(args.threshold)

#THis is to connect to opensourcemaps nominatim data
#nom = geopy.geocoders.Nominatim()

#This connects to google
geo = geopy.geocoders.GoogleV3()

#coord technically stores all of the things associated with the location
coord = geo.geocode(args.address)

#This just makes a tuple of the lat and long
home = (coord.latitude, coord.longitude)

#Cursor can return the results of a query
cursor = connection.cursor()


RadiusQuery = "select cidr, asn, owner, countryCode, region, city, lat, long from asn_db11;"

#stores the result
RadiusResult = cursor.execute(RadiusQuery)


#grabs the entire returned result
for row in RadiusResult.fetchall():
    #row is a list, and lat and long are the last two elements
    rowLoc = (row[-2], row[-1])

    #geopy has a way to calculate distance, but this library was about twice as fast on average
    h = haversine(home, rowLoc, miles=True)

    #This returns all results within the threshold
    if  h <=threshold:
        print("IP Range: {} ASN: {} Owner: {} Country Code: {} State: {} City: {} Distance: {}").format(row[0], row[1], row[2], row[3], row[4], row[5], h)
