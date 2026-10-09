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

"""Test command selection without initializing ROS or starting a simulator."""

from patrol.control import command_from_pose
from patrol.pose_type import Pose


def components(command):
    """Return all six velocity components in their message order."""
    return (command.linear.x, command.linear.y, command.linear.z,
            command.angular.x, command.angular.y, command.angular.z)


def test_no_pose_stops_all_axes():
    """Missing input must produce an entirely zero command."""
    assert components(command_from_pose(None)) == (0.0,) * 6


def test_pose_produces_required_arc_without_changing_input():
    """A received pose enables the exact required velocities."""
    pose = Pose(x=5.5, y=4.0, theta=-1.0)
    before = (pose.x, pose.y, pose.theta,
              pose.linear_velocity, pose.angular_velocity)
    assert components(command_from_pose(pose)) == (0.5, 0.0, 0.0, 0.0, 0.0, 0.3)
    assert (pose.x, pose.y, pose.theta,
            pose.linear_velocity, pose.angular_velocity) == before


def test_origin_pose_is_valid_input():
    """A zero-valued pose is present data, not an absent message."""
    assert components(command_from_pose(Pose())) == (0.5, 0.0, 0.0, 0.0, 0.0, 0.3)


def test_commands_do_not_share_mutable_state():
    """Mutating one result must not affect future commands or stop output."""
    first = command_from_pose(Pose())
    first.linear.y = 12.0
    first.angular.z = -8.0
    assert components(command_from_pose(Pose())) == (0.5, 0.0, 0.0, 0.0, 0.0, 0.3)
    assert components(command_from_pose(None)) == (0.0,) * 6
