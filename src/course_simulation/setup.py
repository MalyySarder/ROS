# Copyright 2026 Nikita
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pathlib import Path
from setuptools import find_packages, setup

name = 'course_simulation'
data = [('share/ament_index/resource_index/packages', ['resource/' + name]),
        ('share/' + name, ['package.xml'])]
for folder in ('launch', 'config', 'models', 'worlds'):
    for path in Path(folder).rglob('*'):
        if path.is_file() and '__pycache__' not in str(path):
            data.append(('share/' + name + '/' + str(path.parent), [str(path)]))
setup(name=name, version='0.1.0', packages=find_packages(exclude=['test']),
      data_files=data, install_requires=['setuptools'], zip_safe=True,
      maintainer='Nikita', maintainer_email='niknikivan@gmail.com',
      description='PR07 Gazebo simulation and command/odometry adapters',
      license='Apache-2.0', extras_require={'test': ['pytest']},
      entry_points={'console_scripts': [
          'ackermann_adapter = course_simulation.adapters:drive_main',
          'odom_adapter = course_simulation.adapters:odom_main']})
