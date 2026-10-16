from glob import glob

from setuptools import setup

setup(name='course_bringup', version='0.0.0', packages=['course_bringup'],
      data_files=[('share/ament_index/resource_index/packages', ['resource/course_bringup']),
                  ('share/course_bringup', ['package.xml']),
                  ('share/course_bringup/launch', glob('launch/*.launch.py'))],
      install_requires=['setuptools'], license='Apache-2.0',
      maintainer='Nikita', maintainer_email='niknikivan@gmail.com',
      description='Namespaced patrol, QoS and MCAP recording')
