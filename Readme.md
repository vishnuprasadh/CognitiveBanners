<b>Description</b>

I have used Reinforcement learning technique that uses a set of tools given in details below to dynamically display images for a Banner Slot of an ecommerce website.

The additional feature added in the framework is to support multiple locations based on setup that influences dynamically to improve click through rate for banners.

<b>Business Problem</b>

One of the biggest revenue generation stream in Digital commerce is banner based ads and click-through conversion through effective banner strategy. It is important to learn as the customer interacts if a banner is efficient. To some extent A/B testing does but its all post facto. Instead, reinfocement learning can help when the CTR of banners is too low by dynamically finding out the most clicked banners and leverages the same for display. In this program, this has been done with an additional classification by location.

Refer to the emarketer study (https://www.emarketer.com/Article/US-Digital-Display-Ad-Spending-Surpass-Search-Ad-Spending-2016/1013442) and many more forrestor studies which suggest this is  going to be a multibagger market with over $40 Billion revenue by 2020 in US alone.


<b>Features</b>
1. Supports Multitenancy for multiple platforms
2. Supports configuration based approach for banners identified by banner name
3. Supports location based filtering 
4. Supports timewindow so that only fresh trending banners are used.
5. The current model also supports referrer ID(ads or thirdparty) and customerID capture. This can help us in future to do targeted marketing based on users click through rates.


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

NOTE: Just to ease out the pain add the above bin paths to your $PATH file if you are on mac i.e. in your ~/.bash_profile. In case of windows, i guess you would need it in your env_path ??(Check it as i couldnt test on windows)

5. PIP Installs

You can run the following command from the root folder of the application
```
python setup.py install
```
If above yields in any errors, backup option is to run the following

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

6. Setup Cassandra

Under resources folder you have model.cql which has the schema to setup the images and the table to capture banner click stream and render data. 

Run the following command from the bin folder of cassandra and setup yaml configuration under conf to appropriate number of nodes as required before you start.

```
cassandra
```

7. Spark setup

Just run the following command to check if pyspark is properly working. You should get a response of version installed without errors.
```
spark --version
```


<b>. Running the Application</b>

1. Once the above setup is taken care, you are now ready to setup some base data. Download your repo and unzip into any folder.
Run following command to setup the basic data of the slots in cassandra. 
```
python setslotconfiguration.py

```
if you run into issues you can manually copy into spyder or other tools and execute.

2. Run the following command to simulate or enter some data for our coldstart strategy. This should setup data. Check for the code under main method and you can update millions of records as required.

```
python testBannerGenerator.py
```

3. You are now ready to rumble with Thompson sampling technique! Go to the "CognitiveBanners" folder where we got all our *.py files.
Execute the following:
```
export FLASK_APP=AdClickEvents.py
export FLASK_DEBUG=true
flask run -p 5002

```
Note: In case you want to run of any other port, make corresponding changes to the banner.html file where we have used port with 127.0.0.1 IP i.e. loopback IP.


9. Model tuning

I have bannerSuggestClassification.py being used for model tuning purpose. All tests and modeltuning, assessment of the logic in the actual codebase of AdClickEvents.py is done through this. One of the good approach will be tune this data on your live environment and rollout these changes to AdClickEvents.py









