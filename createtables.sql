create table db11(
startRange bigint,
endRange bigint,
countryCode varchar(2),
countryName varchar2(50),
region varchar2(50),
city varchar2(50),
lat float(10,6),
long float(10,6),
zip varchar2(15),
timeZone varchar2(10));

create table asn(
startRange bigint,
endRange bigint,
cidr varchar2(18),
asn varchar2(10),
owner varchar2(30));
