from configparser import ConfigParser
import os

def singleton(clsinstance):
    instances={}
    def getinstance():
        if  clsinstance not in instances:
            instances[clsinstance] = clsinstance
            print ('Class {} instantiated'.format(type(clsinstance)))
        return instances[clsinstance]

    return getinstance()

@singleton
class ModelConfiguration:
    '''
    A singleton object used to initiate the configuration of database model.
    Provides an output of the cluster, keyspace and port details.
    This uses the @ConfigParser for loading all the configurations set in config.ini under the section [cassandra].
    '''
    _dbsectionkey = "cassandra"
    _clusterkey = "cluster"
    _keyspacekey = "keyspace"
    _portkey = "port"
    _usernamekey = "username"
    _passwordkey = "password"

    def __init__(self):
        config = ConfigParser()
        config.read(os.path.join(os.path.curdir, "config.ini"))
        self._cluster = config.get(self._dbsectionkey, self._clusterkey)
        self._keyspace = config.get(self._dbsectionkey, self._keyspacekey)
        self._port = config.get(self._dbsectionkey, self._portkey)
        self._password = config.get(self._dbsectionkey,self._usernamekey)
        self._username = config.get(self._dbsectionkey, self._passwordkey)


    @property
    def getClusterName(self):
        return self._cluster

    @property
    def getKeyspace(self):
        return self._keyspace

    @property
    def getPort(self):
        return self._port

    @property
    def getUserName(self):
        return self._username

    @property
    def getPassword(self):
        return self._password
