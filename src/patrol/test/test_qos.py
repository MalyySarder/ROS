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

"""Verify offered/requested reliability independently of the live demo."""

from patrol.pose_relay import sensor_qos
import pytest
from rclpy.qos import DurabilityPolicy, ReliabilityPolicy


def test_sensor_policy():
    """The sensor must offer best effort, volatile, depth ten."""
    qos = sensor_qos('best_effort')
    assert qos.reliability == ReliabilityPolicy.BEST_EFFORT
    assert qos.durability == DurabilityPolicy.VOLATILE
    assert qos.depth == 10


def test_monitor_policy():
    """Reliable is an explicit alternative, not silently coerced."""
    assert sensor_qos('reliable').reliability == ReliabilityPolicy.RELIABLE
    with pytest.raises(ValueError):
        sensor_qos('typo')
