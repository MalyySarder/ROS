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

"""Resolve the Pose interface in the two course-supported ROS distributions."""

from importlib import import_module
import os

# Jazzy kept Pose in turtlesim; Lyrical moved interfaces to turtlesim_msgs.
_pose_package = 'turtlesim' if os.environ.get('ROS_DISTRO') == 'jazzy' else 'turtlesim_msgs'
Pose = import_module(_pose_package + '.msg').Pose
