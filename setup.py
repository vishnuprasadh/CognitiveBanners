from pylint.__pkginfo__ import install_requires
from setuptools import setup
import os

#packages = ["CognitiveBanners.bannercontext", "CognitiveBanners.bannermodel", "CognitiveBanners.utils", "CognitiveBanners.moduleConfiguration",
#            "CognitiveBanners.setslotconfiguration", "CognitiveBanners.bannerSuggestClassification", "CognitiveBanners.testBannerGenerator"],

setup(name="CognitiveBanners",
      packages=["CognitiveBanners"],
      description="A Reinforcement learning based application used for banners/ads strategy",
      install_requires=["numpy","pandas","scikit-learn","flask","pyspark","requests",
                "configparser","cassandra-driver","jsonify","matplotlib","kafka","kafka-rest"],
      include_package_data=True,
      author="Vishnu Prasad Hari",
      author_email="",
      license="BSD"
      )

