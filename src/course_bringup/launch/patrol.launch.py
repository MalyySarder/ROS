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

"""Launch one global simulator and a namespaced system with optional recording."""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node


def generate_launch_description():
    """Keep recording conditional at launch evaluation time."""
    ns = LaunchConfiguration('namespace')
    return LaunchDescription([
        DeclareLaunchArgument('namespace', default_value='robot_a'),
        DeclareLaunchArgument('record', default_value='false', choices=['true', 'false']),
        DeclareLaunchArgument('bag_dir', default_value='evidence/pr05/bag'),
        DeclareLaunchArgument('subscriber_reliability', default_value='reliable',
                              choices=['reliable', 'best_effort']),
        Node(package='turtlesim', executable='turtlesim_node', output='screen'),
        Node(package='patrol', executable='patrol', namespace=ns, output='screen',
             remappings=[('turtle1/pose', '/turtle1/pose'),
                         ('cmd_vel', '/turtle1/cmd_vel')]),
        Node(package='patrol', executable='pose_relay', namespace=ns, output='screen',
             remappings=[('pose', '/turtle1/pose')]),
        Node(package='patrol', executable='pose_monitor', namespace=ns, output='screen',
             parameters=[{'subscriber_reliability':
                          LaunchConfiguration('subscriber_reliability')}]),
        ExecuteProcess(
            cmd=['ros2', 'bag', 'record', '-s', 'mcap', '-o', LaunchConfiguration('bag_dir'),
                 '--topics', PathJoinSubstitution(['/', ns, 'sensor_pose'])],
            output='screen', condition=IfCondition(LaunchConfiguration('record'))),
    ])
