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

"""Test validation and preservation of active state on rejected updates."""

import math

from patrol.control import command_from_pose
from patrol.parameters import validate_settings
from patrol.patrol import Patrol
from patrol.pose_type import Pose
import pytest
import rclpy
from rclpy.parameter import Parameter


@pytest.mark.parametrize('hz', [1.0, 5.0, 10.0, 30.0])
def test_valid_frequency(hz):
    """Boundary and ordinary frequencies are accepted."""
    validate_settings({'linear_speed': 0.5, 'turn_rate': 0.3, 'publish_hz': hz})


@pytest.mark.parametrize('name,value', [
    ('publish_hz', 0.0), ('publish_hz', -1.0), ('publish_hz', math.nan),
    ('publish_hz', math.inf), ('publish_hz', 31.0), ('publish_hz', True),
    ('linear_speed', -0.1), ('linear_speed', 1.1), ('linear_speed', math.nan),
    ('turn_rate', -1.1), ('turn_rate', 1.1), ('turn_rate', math.inf),
])
def test_invalid_values(name, value):
    """Bad settings cannot reach the active timer or velocity state."""
    settings = {'linear_speed': 0.5, 'turn_rate': 0.3, 'publish_hz': 10.0}
    settings[name] = value
    with pytest.raises(ValueError):
        validate_settings(settings)


def test_parameterized_command():
    """The pure function uses requested speeds, but requires a pose."""
    command = command_from_pose(Pose(), 0.8, -0.4)
    assert (command.linear.x, command.angular.z) == (0.8, -0.4)
    stopped = command_from_pose(None, 0.8, -0.4)
    assert (stopped.linear.x, stopped.angular.z) == (0.0, 0.0)


def test_atomic_update_and_single_timer():
    """Rejection preserves state; valid frequency replaces exactly one timer."""
    rclpy.init()
    node = Patrol()
    try:
        old_timer = node.command_timer
        result = node.set_parameters_atomically([
            Parameter('linear_speed', value=0.9), Parameter('publish_hz', value=0.0)])
        assert not result.successful
        assert node.settings['linear_speed'] == 0.5
        assert node.get_parameter('publish_hz').value == 10.0
        assert node.command_timer is old_timer
        assert len(list(node.timers)) == 1
        result = node.set_parameters_atomically([Parameter('publish_hz', value=5.0)])
        assert result.successful
        assert node.command_timer is not old_timer
        assert node.command_timer.timer_period_ns == 200000000
        assert len(list(node.timers)) == 1
    finally:
        node.destroy_node()
        rclpy.shutdown()
