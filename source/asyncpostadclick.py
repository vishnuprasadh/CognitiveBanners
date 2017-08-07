from kafka_rest.client import KafkaRESTClient

import source.utils as utils
from source.bannercontext import BannerContext


class AsyncPostAdClick:

    def postBannerClick(self,banner):

        client = KafkaRESTClient("http://localhost",port=9092)
        avro_schema ={'type':'record','name':'bannerclick',
                      'fields':
                            [{'name': 'platform','type':'string'},
                            {'name': 'slotid', 'type': 'string'},
                            {'name': 'bannerid', 'type': 'string'},
                            {'name': 'clicked', 'type': 'bool'},
                             {'name': 'operationtime', 'type': 'string'},
                             {'name': 'customerid', 'type': 'string'},
                             {'name': 'location', 'type': 'string'},
                             {'name': 'referral', 'type': 'string'}]
                      }
        avro_value = [{banner.getPlatform},
                      {banner.getSlot},
                      {banner.getBannerID},
                      {banner.getBannerClicked},
                      {banner.getOperationTime},
                      {banner.getLocation},
                      {banner.getReferral},
                      ]



if __name__ == "__main__":
    post = AsyncPostAdClick()
    banner = BannerContext('hero','mumbai','armani',utils.currentimeInFormat(),"1",False)
    post.postBannerClick(banner)

