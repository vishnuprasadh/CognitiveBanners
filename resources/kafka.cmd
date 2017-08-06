#1.Start zookeeper
zookeeper-server-start.sh ../config/zookeeper-properties
#in the above we can configure the # of zk nodes etc
#2 Start broker
kafka-server-start.sh ../config/server.properties
#again, callout specifics on brokers to start
#Create topic - bannerstream
kafka-topics.sh --create --topic bannerstream --zookeeper localhost:2181 --replication-factor 1 --partitions 1

#curl http://127.0.0.1:5002/adclick/ -d "slot=hero,clicked=True,bannerid=armani,location=bangalore,customerid=1,referral=,platform=ajio" -X Post -V
#curl http://127.0.0.1:5002/adclick/ -d "slot=hero" -X Post -V
#
#