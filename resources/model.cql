create keyspace cognitivebanners with replication = {'class':'SimpleStrategy','replication_factor':'2'};

use cognitivebanners;

CREATE TABLE bannerclickstream (
    platform text,
    operationdate timeuuid,
    adreferrer text,
    slotname text,
    bannerid text,
    clicked boolean,
    createddate float,
    customerid text,
    location text,
    PRIMARY KEY ((platform, slotname), operationdate,location)
) WITH CLUSTERING ORDER BY (operationdate DESC);

create table slotconfiguration
(
	platform text,
	slotname text,
	imagekey text,
	imagename text,
	validfrom bigint,
	validto bigint,
	datemodified timeuuid,
	primary key((platform,slotname),validto, imagekey)
) with clustering order by (validto DESC)


 Insert into bannerclickstream (platform,operationdate,adreferrer,slotname,bannerid,createddate, customerid, location,clicked)
 values ('ajio',f6747f80-7ac7-11e7-a231-409152815c5c,'','hero','1',1502038496,'1','mumbai',True)


Select * from bannerclickstream where platform = 'ajio' and slotname = 'hero' and operationdate > 39c35cd8-7ac9-11e7-8ea2-a43489e438f4

Select count(*) from bannerclickstream where platform = 'ajio' and slotname = 'hero' and operationdate > 39c35cd8-7ac9-11e7-8ea2-a43489e438f4