class BannerContext:
    '''
    @Bannercontext is an object which contains the location, customerid,  bannerid, the clicked event, referral id from where it was clicked and for which platform.
    This simple object will be saved in backend to accumulate the streaming event.

    '''
    def __init__(self,slotid,location,bannerid, operationtime, customerid="",
                 bannerclicked=False,referral="",platform='ajio'):
        self._slotid = slotid
        self._location = location
        self._customerid = customerid
        self._referral = referral
        self._bannerid = bannerid
        self._platform = platform
        self._bannerclicked = bannerclicked
        self._operationtime =  operationtime

    @property
    def getSlot(self):
        return self._slotid

    @property
    def getLocation(self):
        return self._location

    @property
    def getCustomerID(self):
        return self._customerid

    @property
    def getPlatform(self):
        return self._platform

    @property
    def getBannerID(self):
        return self._bannerid

    @property
    def getBannerClicked(self):
        return self._bannerclicked

    @property
    def getOperationTime(self):
        return self._operationtime

    @property
    def getReferral(self):
        return self._referral
