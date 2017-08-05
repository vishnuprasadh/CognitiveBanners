create keyspace cognitivebanners with replication = {'class':'SimpleStrategy','replication_factor':'2'};

use cognitivebanners;

CREATE TABLE bannerclickstream (
    platform text,
    operationdate timeuuid,
    adreferrer text,
    bannerid text,
    clicked boolean,
    createddate timestamp,
    customerid text,
    location text,
    PRIMARY KEY (platform, operationdate)
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


