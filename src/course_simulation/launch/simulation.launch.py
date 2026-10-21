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

"""Start one model, one bridge, and both contract adapters."""

import os
from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import xacro


def start(context):
    share = Path(get_package_share_directory('course_simulation'))
    description = Path(get_package_share_directory('course_description'))
    world = LaunchConfiguration('world').perform(context)
    config = LaunchConfiguration('bridge_config').perform(context)
    namespace = LaunchConfiguration('namespace').perform(context)
    headless = LaunchConfiguration('headless').perform(context).lower() == 'true'
    resources = str(share / 'models')
    if os.environ.get('GZ_SIM_RESOURCE_PATH'):
        resources += os.pathsep + os.environ['GZ_SIM_RESOURCE_PATH']
    robot = xacro.process_file(str(description / 'urdf/vehicle.urdf.xacro')).toxml()
    command = ['gz', 'sim', '-r', world]
    if headless:
        command += ['-s', '--headless-rendering']
    return [
        ExecuteProcess(cmd=command, output='screen',
                       additional_env={'GZ_SIM_RESOURCE_PATH': resources}),
        Node(package='robot_state_publisher', executable='robot_state_publisher',
             namespace=namespace, parameters=[{'use_sim_time': True, 'robot_description': robot}]),
        Node(package='ros_gz_bridge', executable='parameter_bridge', name='bridge',
             namespace=namespace, output='screen',
             parameters=[{'use_sim_time': True, 'config_file': config}]),
        Node(package='course_simulation', executable='ackermann_adapter',
             namespace=namespace, output='screen', parameters=[{'use_sim_time': True}]),
        Node(package='course_simulation', executable='odom_adapter',
             namespace=namespace, output='screen', parameters=[{'use_sim_time': True}]),
    ]


def generate_launch_description():
    share = Path(get_package_share_directory('course_simulation'))
    return LaunchDescription([
        DeclareLaunchArgument('world', default_value=str(share / 'worlds/mcity-minimal.sdf')),
        DeclareLaunchArgument('bridge_config', default_value=str(share / 'config/bridge.yaml')),
        DeclareLaunchArgument('namespace', default_value='robot_a'),
        DeclareLaunchArgument('headless', default_value='true', choices=['true', 'false']),
        OpaqueFunction(function=start),
    ])
