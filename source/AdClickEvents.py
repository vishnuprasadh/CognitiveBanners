from flask import Flask,Request,render_template,url_for,request
#from flask_restful import Resource,Api,reqparse
from source.bannermodel import BannerModel
from source.bannercontext import BannerContext
import source.utils as utils

from pyspark.context import SparkContext,SparkConf

app = Flask(__name__)
#api = Api(app)
#parser = reqparse.RequestParser()

@app.route('/adclick/',methods=['POST'])
def postAds():
    if Request.args:
        arguments = Request.args
        banner = BannerContext(arguments["slot"],
                               arguments["location"],
                               arguments["bannerid"],
                               utils.currentimeInFormat(),
                           arguments["customerid"],
                           arguments["clicked"],
                           arguments["referral"],
                           arguments["platform"])

@app.route('/adclick/',methods=['GET'])
@app.route('/adclick/<string:platform>',methods=['GET'])
@app.route('/adclick/<string:platform>/<string:slot>',methods=['GET'])
@app.route('/adclick/<string:platform>/<string:slot>/<string:location>',methods=['GET'])
@app.route('/adclick/<string:platform>/<string:slot>/<string:location>/<string:pastmin>',methods=['GET'])
def getAds(platform='ajio',slot='hero',location='bangalore',pastmin=720):
    bmodel  = BannerModel()
    rows = bmodel.getBanners(platform,slot,pastmin)

    #load the recs and send the right value through spark
    SparkConf.setMaster= "local[2]"
    SparkConf.setAppName ="banners"
    sc = SparkContext.getOrCreate()






#api.add_resource(AdClickEvents,'/adclick/<platform>/<slot>/<location>')


if __name__=='__main__':
    app.run(host="127.0.0.1", port=int(5002),debug=True)