<b>Description</b>

This is a simple Reinforcement learning technique which uses a set of tools given below to dynamically display images for a Banner Slot of an ecommerce website.
The additional feature used is the framework can support multiple locations based on setup and dynamically improves click through rate for banners.

<b>Business Problem</b>

One of the biggest revenue generation stream in Digital commerce is banner based ads and click-through conversion through effective banner strategy. It is important to learn as the customer interacts if a banner is efficient. To some extent A/B testing does but its all post facto. Instead, reinfocement learning can help when the CTR of banners is too low by dynamically finding out the most clicked banners and leverages the same for display. In this program, this has been done with an additional classification by location.

Refer to the emarketer study (https://www.emarketer.com/Article/US-Digital-Display-Ad-Spending-Surpass-Search-Ad-Spending-2016/1013442) and many more forrestor studies which suggest this is  going to be a multibagger market with over $40 Billion revenue by 2020 in US alone.


The current model also supports referrer ID(ads or thirdparty) and customerID capture. This can help us in future to do targeted marketing based on users click through rates.

Further the model also supports multitenancy by ensuring the platform, slotID for images are inherantly embedded in the design.


<b>Improvements & TODOs</b>

There is lot of improvements through weightage and clustering to be added here but this is a very base "no-frills" extensible framework.


<b>Technology Used</b>

1. Python 3, Flask/REST
The core technology which will basically run the entire framework.
The flask REST GET and POST methods are used for posting of clicked banner data and retrieved image data.

2. skilearn and machine learning libraries
Used for preprocessing of data and label & onehotencoding
The reinforcement problem picked up is the multiarmed-bandit problem and is being resolved using Thompson sampling i.e. Betavariate analysis.
A reward of 1 points and a noreward of 0 points used for this betavariate analysis

3. Cassandra drivers
A basic slotconfiguration with 10images has been considered for one slot.
Also on click, banner clicked data is stored in backend schema.

4. Pandas, Numpy,time,datetime
Heavily used for dataframe activities.
Intrinsic support of IST = Indian Standard time with all formatting consdiered

5. Reinforcement learning
In this case a supervised set of data is used to provide for coldstart strategy
Once the above is used, then we would not be leveraging the realtime clickstream for probability analysis.
We are using Thompson sampling for the same.

8. Spark, PySpark
PySpark framework is used for usage of filters across cities and also for any future streaming functions.
It is not used for ML or any other purpose which we can easily leverage once we also adopt Kafka.

7. Kafka - TBD
For large scale clickstream, it is best to use this technology.
The framework coding has started but not yet completed.


<b>Installation</b>


Before you can proceed, the following has to be installed for sure. Note that there is no installation package created as of now but the following steps shoudl get you up and started easily.

1.Python 3.6 - https://www.python.org/downloads/release/python-360/
Once done, ensure you have right $ENVPATH or $HOME set in your bashprofile(mac) and env in windows.
Note: I prefer using https://www.continuum.io/downloads which is anaconda distribution which has been used for this program.

2.Cassandra - Any community or datastax community edition would do. https://academy.datastax.com/downloads?destination=downloads or http://cassandra.apache.org/ 

3. Spark - Minimal of 2.X edition from https://spark.apache.org/  is required. Install community for apache hadoop 2.7 prebuilt edition and proceed.

4. Kafka - At the moment the entire implementation is not yet done but download and have the kafka from https://kafka.apache.org/ ready for future compatibility. This would in turn be using Kafka REST & AVRO binary serializer for all topic messaging.

5. PIP Installs
```
pip install cassandra-driver
pip install numpy
pip install pandas
pip install scikit-learn
pip install json
pip install pyspark
pip install csv
pip install kafka-python
pip install flask
pip install kafka
pip install kafka_Rest
pip install configparser
```












