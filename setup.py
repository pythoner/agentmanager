from setuptools import find_packages
from setuptools import setup


setup(name="agentmanager",
      version=1.0,
      author="lenovo",
      author_email="example@org.com",
      packages=find_packages(),
      scripts=['bin/agentmanager-api', 'bin/agentmanager-dbsync'],
      url="www.lenovo.com.cn",
      description="Lenovo OI Agent Manager System",
      )
