from flask import Flask,Request,render_template,url_for,request
#from flask_restful import Resource,Api,reqparse
from source.bannermodel import BannerModel
from source.bannercontext import BannerContext
import source.utils as utils
from pyspark.context import SparkContext,SparkConf
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
import  pandas as pd
import random
import json


app = Flask(__name__)

@app.route('/adclick/',methods=['POST'])
def postAds():
    '''
    Used for posting of ads.
    key elements to pass are - location, clicked, bannerid,customerid
    Other elements to pass for context are platform, slot, referral
    :return: Json 200 response for any success. Also gets a Errorcode and description in case of issue
    '''
    json_data=""
    try:
        if request.args:
            referral =""
            platform="ajio"
            slot="hero"
            customerid =""
            bannerid= ""
            clicked = False
            location=""

            if request.args.get("referral"): referral = request.args.get("referral")
            if request.args.get("slot"): slot =request.args.get("slot")
            if request.args.get("location"): location = request.args.get("location")
            if request.args.get("customerid"): customerid = request.args.get("customerid")
            if request.args.get("clicked"): clicked = _convert_to_bool(request.args.get("clicked"))
            if request.args.get("platform"): platform = request.args.get("platform")
            if request.args.get("bannerid"): bannerid = request.args.get("bannerid")

            banners = []

            if not (bannerid == "" or clicked == "" or location == ""):
                banner = BannerContext(slot.lower(),
                                       location.lower(),
                                       bannerid.lower(),
                                       utils.currentimeInFormat(),
                                       customerid,
                                       clicked,
                                       referral.lower(),
                                       platform.lower())
                banners.append(banner)
                bmodel = BannerModel()
                result = bmodel.saveBanners(banners)
                json_data = {"key": "200", "value": "Record updated successfully"}

        if json_data == "":
            json_data = {"key": "200", "value": "No Record to update"}
    except Exception as ex:
        print(ex)
        json_data = {"key": "200", "value":"", "errorcode": "401", "errordesc":"{}".format(ex)}

    return json.dumps(json_data)

def _convert_to_bool(value):
    """
       Converts 'something' to boolean. Raises exception for invalid formats
           Possible True  values: 1, True, "1", "TRue", "yes", "y", "t"
           Possible False values: 0, False, None, [], {}, "", "0", "faLse", "no", "n", "f", 0.0, ...
    """
    if str(value).lower() in ("yes", "y", "true",  "t", "1"): return True
    if str(value).lower() in ("no",  "n", "false", "f", "0", "0.0", "", "none", "[]", "{}"): return False
    raise Exception('Invalid value for boolean conversion: ' + str(value))


@app.route('/adclick/',methods=['GET'])
@app.route('/adclick/<string:platform>',methods=['GET'])
@app.route('/adclick/<string:platform>/<string:slot>',methods=['GET'])
@app.route('/adclick/<string:platform>/<string:slot>/<string:location>',methods=['GET'])
@app.route('/adclick/<string:platform>/<string:slot>/<string:location>/<string:pastmin>',methods=['GET'])
def getAds(platform='ajio',slot='hero',location='bangalore',pastmin=720):
    '''
    Provided the platform, slot and location details the API returns the image/ad.
    :param platform:
    :param slot:
    :param location:
    :param pastmin:
    :return: Returns a json structure with key and value. The value has the name of image.
     In case of error the errorcode and description is returned.
    '''
    bmodel  = BannerModel()
    images = bmodel.getSlotBanners(platform, slot, utils.currentimeInFormat())
    rowresult = bmodel.getBanners(platform,slot,pastmin)

    json_data = json.dumps({})

    #if location not in any of this, default to Mumbai.
    if not (location.lower() in ["mumbai","bangalore","pune"]):
        location = "mumbai"

    if rowresult:
        #Initialize Spark context
        SparkConf.setMaster = "local[2]"
        SparkConf.setAppName = "banners"
        sc = SparkContext.getOrCreate()
        rows = rowresult.current_rows
        rdd = sc.parallelize(rows)
        #filter by location
        keys = rdd.filter(lambda X: location in X[0])
        #collect the filtered values to list.
        values = keys.collect()
        #get a dataframe
        adclicks = pd.DataFrame(values)

        adname = _normalizeandReturnAd(adclicks,images=images)

        json_data = {"key": adname[1], "value": "{0}.png".format(adname[1])}

        #We will also post an entry for this banner which will be clicked as false.
        banner = BannerContext(slot,
                               location,
                               adname[1],
                               utils.currentimeInFormat(),
                               "-1",
                               _convert_to_bool('false'),
                               "",
                               platform)
        #also add an entry with assumption people may not click
        banners=[]
        banners.append(banner)
        result = bmodel.saveBanners(banners)

    else:
        json_data = {"key" :"", "errorcode":"401", "errordesc":"No object found!"}

    return json.dumps(json_data)


def _normalizeandReturnAd(df,images):
    #get count of dataframe
    samples = len(df)
    data = df.iloc[:, [1, 2]].values
    labelencodeImage = LabelEncoder()
    labelencodecity = LabelEncoder()
    data[:, 0] = labelencodeImage.fit_transform(data[:, 0])
    #data[:, 1] = labelencodecity.fit_transform(data[:, 1])

    onehotencoderimage = OneHotEncoder(categorical_features=[0])
    data = onehotencoderimage.fit_transform(data).toarray()


    #Initialize the images
    adimages=[]
    for slot in images:
        adimages.append(slot[4])

    # Depending on number of images for the slot we will initialize
    numberofrewards_1 = [0] * len(adimages)
    numberofrewards_0 = [0] * len(adimages)


    #now based on variate analysis return the ads.
    for sample in range(0, samples):
        selectedad = 0
        # this is required as we take the max random draw from each ads
        max_random = 0

        # for each ad image, calculate the randombeta
        for ad in range(0, len(adimages)):
            randombeta = random.betavariate(numberofrewards_1[ad] + 1,
                                            numberofrewards_0[ad] + 1)
            # as per the thompsonsampling, we need to take the maximum of the beta dist and set the ad which needs to showup.
            if randombeta > max_random:
                max_random = randombeta
                selectedad = ad

        #now boost the values of reward count if its correctly or wrongly selected so that it can influence future betavariate values
        reward = data[sample, selectedad]
        if reward == 1:
            numberofrewards_1[selectedad] = numberofrewards_1[selectedad] + 1
        else:
            numberofrewards_0[selectedad] = numberofrewards_0[selectedad] + 1


    return selectedad, adimages[selectedad]


if __name__=='__main__':
    app.run(host="127.0.0.1", port=int(5002),debug=True)