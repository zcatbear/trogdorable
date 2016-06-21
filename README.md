## Introduction
This was used by BroEZ labs as we were trying to design an exercise to help train our developers.  
One of the things we needed to do was come up with places for our threat cell to geographically be located, and that needed to tie back to real IP infrastructure to obtain actual training value.  
One of the problems we encountered was that given an IP address you can identify it's geolocation and ASN rather quickly but, finding the reverse takes significantly longer.   
We found that to be an annoyance and time waste. So we invested some time to figuring out how to pass a geolocation and get back all of the IP ranges and associated ASNs within a certain, user defined, area

## Setting up the databases
### Getting the data
IP2Location provides some free *lite* versions of their databases that can be downloaded as either CSVs or binaries. I went with the CSVs of both the ASN [here](https://lite.ip2location.com/database/ip-asn "ASN") and the DB11 databases [here](https://lite.ip2location.com/database/ip-country-region-city-latitude-longitude-zipcode-timezone  "DB11"). I would download them into the same folder so when you unzip them they aren't far off in the directory structure.

### Making the Databases
Unzip the each of the zip files. We are going to import the csv files into their own table, but first the tables need to be created.  
You can just download the createTables.sql file and just run `sqlite3 trogdorable.db < createTables.sql` which will create both tables.   
Next comes the importing of the csv files. while in the `~` directory  
>```sql 
$sqlite3 trogdorable.db
sqlite> .separator ",";
sqlite> .import <location of asn csv file> asn;
sqlite> .import <location of db11 csv file> db11;
```

To check to make sure it all worked you can do:
> ```
sqlite> SELECT * FROM asn;
sqlite> SELECT * FROM db11;
```

Both of those should return results but to get the joined results do  

```
SELECT * FROM asn, db11 WHERE asn.startRange == db11.startRange and asn.endRange == db11.endRange;
```
Which ultimately gives you everything for matching IP ranges. You can narrow it down using SQL by selecting which city/state or country you want to be in. 


## Going Further with Python
For searching within a radius requires the addition of some python though. This helps when dealing with small towns that may not be included by name in the SQL database or when you want to get more specific inside a city like NYC. 

The python script is already set up all it needs is access to your database and some arguments passed to it and it is good to go. 

To invoke the script simply you just have to type python and call it while still giving it the arguments it needs.
`--database` requires the location of your database (***Note:*** add a default and you don't have to pass it in every time)  
`--threshold` is the radius (in miles) you want to search in. This uses haversine formula to calculate distance between two points (Default of 100 Miles)  
`--address` is the address you want to compare against. This can be a nation, city, state, street address, or you can pass a lat and long. 

Example:  
```python trogdorable.py --database /home/username/trogdorable/trogdorable.db --threshold 25 --address "-33.9144821,18.3758797"```  
OR:  
```python trogdorable.py --database /home/user/trogdorable/trogdorable.db --threshold 50 --address "Hometown, WV"```  
***NOTE:*** the address is always wrapped in quotes to stop spaces from causing problems. Use the quotes. 

 

   
