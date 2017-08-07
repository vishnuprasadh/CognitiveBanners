from setuptools import setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name="CognitiveBanners",
      packages=['source.bannercontext','source.bannermodel','source.utils','source.moduleConfiguration',
          'source.setslotconfiguration','source.bannerSuggestClassification','source.testBannerGenerator'],
      description="A Reinforcement learning based application used for banners/ads strategy",
      requires=['numpy','pandas','scikit-learn','flask','pyspark',
                'configparser','cassandra-driver','jsonify','matplotlib','kafka','kafka-rest'],
      include_package_data=True,
      author='Vishnu Prasad Hari',
      author_email="",
      license="BSD",
      long_description=read('Readme.cmd'),
      keywords='Cognitivebanners,adclick,adbanners,reinforcementlearning,thompson,thompsonsampling'
      )

