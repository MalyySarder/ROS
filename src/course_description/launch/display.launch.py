"""Expand Xacro and display the robot without a joint_state_publisher dependency."""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.conditions import IfCondition
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    share = FindPackageShare('course_description')
    description = Command([
        FindExecutable(name='xacro'), ' ',
        PathJoinSubstitution([share, 'urdf', 'vehicle.urdf.xacro']),
        ' wheelbase:=', LaunchConfiguration('wheelbase'),
        ' track:=', LaunchConfiguration('track'),
        ' wheel_radius:=', LaunchConfiguration('wheel_radius')])
    return LaunchDescription([
        DeclareLaunchArgument('wheelbase', default_value='0.8'),
        DeclareLaunchArgument('track', default_value='0.62'),
        DeclareLaunchArgument('wheel_radius', default_value='0.12'),
        DeclareLaunchArgument('rviz', default_value='true'),
        DeclareLaunchArgument('show_wheels', default_value='false'),
        Node(package='robot_state_publisher', executable='robot_state_publisher',
             parameters=[{'robot_description': ParameterValue(description, value_type=str)}],
             output='screen'),
        Node(package='rviz2', executable='rviz2',
             arguments=['-d', PathJoinSubstitution([share, 'config', 'vehicle.rviz'])],
             output='screen', condition=IfCondition(LaunchConfiguration('rviz'))),
        ExecuteProcess(cmd=[
            'ros2', 'topic', 'pub', '-r', '10', '/joint_states', 'sensor_msgs/msg/JointState',
            '{header: auto, name: [front_left_steering_joint, front_right_steering_joint, '
            'front_left_wheel_joint, front_right_wheel_joint, rear_left_wheel_joint, '
            'rear_right_wheel_joint], position: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}'],
            output='log', condition=IfCondition(LaunchConfiguration('show_wheels'))),
    ])
