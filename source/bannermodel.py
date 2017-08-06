#core application modules
from source.modelConfiguration import ModelConfiguration
from source.bannercontext import BannerContext

#needed for cassandra authorization,connection and roundrobin policy
from cassandra.cluster import Cluster
from cassandra.policies import DCAwareRoundRobinPolicy
from cassandra.connection import Connection
from cassandra.auth import PlainTextAuthProvider

#need for generation of timeUUID and conversions
from cassandra.util import uuid_from_time
from cassandra.util import datetime_from_uuid1

from cassandra.cqltypes import UUID
from cassandra.cqltypes import TimestampType
from cassandra.cqltypes import BooleanType

#batch statement execution supports
from cassandra.query import BatchStatement
from cassandra.query import SimpleStatement
from cassandra.query import BatchType
from cassandra.policies import WriteType
from cassandra import ConsistencyLevel
from cassandra.query import Statement

#Need to parse values from dataframes/pandas.
from pandas import DataFrame
import time
import math


class BannerModel:
    '''
    @Bannermodel is used to save the banner datamodel in cassandra and also query the same based on the ask.
    '''
    _session = ""
    def __init__(self):
        '''
        Initializes the database conifguration and sets the cassandra cluster.
        Internally uses @ModelConfiguration module to load all the configuration parameters for cassandra.
        '''
        dbconfig = ModelConfiguration()
        self._cluster = dbconfig.getClusterName
        self._keyspace = dbconfig.getKeyspace
        self._port = dbconfig.getPort
        self._username = dbconfig.getUserName
        self._password = dbconfig.getPassword
        authprovider = PlainTextAuthProvider(username=self._username,password=self._password)
        self.cluster = Cluster(contact_points=str(self._cluster).split(","),
                               port=self._port,auth_provider=authprovider,
                          load_balancing_policy=DCAwareRoundRobinPolicy(),
                          connect_timeout=5, idle_heartbeat_interval=60, idle_heartbeat_timeout=45)


    def __setsession(self):
        if self._session =="":
            self._session = self.cluster.connect(keyspace=self._keyspace)

    def  saveBanners(self, bannercontexts,timezone="IST"):
        '''
        For given list of bannercontext objects the method iterates through and saves
        the same in bannerclickstream backend schema
        :param bannercontexts: the instance of @BannerContext
        :param timezone: Default is IST
        :return: Any positive output means successful else error.
        '''
        result = -1
        try:
            self.__setsession()
            statement = " Insert into bannerclickstream (platform,operationdate,adreferrer,slotname,bannerid,createddate, customerid, location,clicked) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            for item in bannercontexts:
                banner = item
                ctime = time.time()

                if timezone == "IST":
                    ctime += 19800  # note 19800 corresponds to 5hr30mins in seconds
                ctime = math.ceil(ctime)

                #click = 'false'
                #if banner.getBannerID:
                #    click = 'true'



                self._session.execute(query=statement,
                                      parameters=
                                        (banner.getPlatform,
                                            self._getUUIDFromTime(banner.getOperationTime),
                                            banner.getReferral,
                                            banner.getSlot,
                                            banner.getBannerID,
                                            ctime,
                                            str(banner.getCustomerID),
                                            banner.getLocation,
                                            banner.getBannerClicked
                                          ))

            result = 1
        except Exception as ex:
            print(ex)
            result =-1
        finally:
            return result


    def getBanners(self,platform='ajio',slot='hero', forpastMinutes=720,timezone="IST"):
        '''
        Returns all the clickstreams forpastMinutes for given platform and slot.
        :param platform: Default used is ajio and is the platform to review
        :param slot: Default is the hero slot
        :param forpastMinutes: 15mins is default. You can increase this further but keep it low to avoid perf issues.
        :param timezone: default is IST. If you are on GMT, do nothing.
        :return: Rows of all the results matching the query from bannerclickstream schema in backend
        '''
        self.__setsession()

        curtime = time.time() - forpastMinutes*60
        if timezone =="IST":
            curtime +=19800 # we need to add 530hrs for gmt

        statement = "Select location,bannerid, clicked,customerid from bannerclickstream where platform = %s and slotname =%s and operationdate > %s "
        rows = self._session.execute(query=statement,
                                     parameters=(platform, slot, uuid_from_time(curtime)))
        return rows


    def setSlotBanners(self,df,timezone="IST"):
        '''
        This method is used to upload the dataframe object with
        @platform, @slotname, @imageid, @imagename, @validfrom,@validto values into the
        slotconfiguration schema
        :param df: The dataframe which is taken as input
        :param timezone: the timezone. Currently assumes all timezone needs to be converted to IST. If its GMT, just callout GST as value.
        :return: numberic value which will be equal to number of records affected, if successful else returns -1.
        '''
        results = -1

        try:
            self.__setsession()
            statement = "insert into slotconfiguration (platform, slotname, imagekey, imagename,validfrom,validto,datemodified) values " \
                        "(%s,%s,%s,%s,%s,%s,%s)"

            #batchinsert = BatchStatement()


            if type(df) is DataFrame:
                for index,row in df.iterrows():

                    ctime = time.time()

                    if timezone =="IST":
                       ctime+= 19800 # note 19800 corresponds to 5hr30mins in seconds

                    '''batchinsert.add(SimpleStatement(statement,(row["platform"],
                                                     row["slotname"],
                                                     row["imageid"],
                                                     row["imagename"],
                                                     isactive,
                                                     self._getUUIDFromTime( row["validfrom"],timeZone=timezone),
                                                     self._getUUIDFromTime( row["validto"],timeZone=timezone),
                                                     uuid_from_time(ctime)
                                                     )))

                    '''
                    results = self._session.execute(statement,
                                         parameters=(row["platform"],
                                                     row["slotname"],
                                                     row["imageid"],
                                                     row["imagename"],
                                                     self._getEpochFromTime( row["validfrom"],timeZone=timezone),
                                                     self._getEpochFromTime( row["validto"],timeZone=timezone),
                                                     uuid_from_time(ctime)
                                                     )
                                        )


                    results = 1


        except Exception as ex:
            print(ex)
            results = -1

        return results

    def getSlotBanners(self,platform='ajio',slotname='hero',validdateasof="",timezone='IST' ):
        '''
        Gets the list of configured SlotBanners for given platform, banner and the time
        :param platform:
        :param banner:
        :param validdateasof:
        :return: List of slotconfigurations
        '''
        try:
            banners = list()
            self.__setsession()
            if validdateasof == "":
                validdateasof = math.floor(time.time())
            else:
                validdateasof = self._getEpochFromTime(validdateasof,timezone)


            statement = "select * from slotconfiguration where platform = %s and slotname = %s and validto > %s"
            results = self._session.execute(query=statement,
                                  parameters=(platform,slotname,validdateasof))

            for row in results:
                banners.append([row.slotname,row.platform,row.validfrom,row.validto,row.imagekey,row.imagename])


        except Exception as ex:
            print(ex)
        finally:
            return banners


    def _getEpochFromTime(self,timetoConvert,timeZone="IST"):
        '''
                Takes a time and returns the UUID which is used in cassandra
                :param timetoConvert: Current time in 20-Jul-2012 13:00:23 format.
                :return: UUIDTime
                '''
        date = time.strptime(timetoConvert, "%d-%b-%y %H:%M:%S")
        # by default it assumes GMT, hence we need to explicitly add
        if timeZone == "IST":
            return  math.floor( time.mktime(date) + 19800)
        else:
            return math.floor( time.mktime(date))

    def _getTimeFromEpoch(self,epoch):
        return time.localtime(epoch)

    def _getUUIDFromTime(self,timetoConvert,timeZone="IST"):
        '''
        Takes a time and returns the UUID which is used in cassandra
        :param timetoConvert: Current time in 20-Jul-2012 13:00:23 format.
        :return: UUIDTime
        '''
        date = time.strptime(timetoConvert, "%d-%b-%y %H:%M:%S")
        #by default it assumes GMT, hence we need to explicitly add
        if timeZone =="IST":
            return uuid_from_time(time.mktime(date) + 19800)
        else:
            return uuid_from_time(time.mktime(date))

    def _getTimeFromUUID(self,UUIDtoConvert):
        '''
        Takes the UUID from the cassandra TimeUUID and returns the actual time.
        :param UUIDtoConvert: Current time in UUID format.
        :return: Time in 20-Jul-2012 13:00:23 format.
        '''
        return datetime_from_uuid1(UUIDtoConvert)



if __name__ == '__main__':
    for index in range(0,10):
        bannerSave = BannerModel()
        bannerSave.getBannerCounts()
        print("index called {} times".format(index))

