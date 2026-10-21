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

"""Behavioral checks at both transport boundaries."""

from copy import deepcopy
import math

from ackermann_msgs.msg import AckermannDriveStamped
from nav_msgs.msg import Odometry
import pytest

from course_simulation.adapters import normalize_odometry, to_twist


def command(speed, angle, stamp=10.0):
    msg = AckermannDriveStamped()
    msg.header.stamp.sec = int(stamp)
    msg.header.stamp.nanosec = round((stamp - int(stamp)) * 1e9)
    msg.drive.speed, msg.drive.steering_angle = float(speed), float(angle)
    return msg


@pytest.mark.parametrize('speed,angle,v,delta', [
    (0.5, 0, 0.5, 0), (0.6, 0.2, 0.6, 0.2), (0, 0.4, 0, 0.4),
    (2, 0.9, 1.2, 0.45), (0.6, -0.9, 0.6, -0.45), (-1, 0.2, 0, 0.2)])
def test_kinematics(speed, angle, v, delta):
    result, reason = to_twist(command(speed, angle), 10.1)
    assert not reason
    assert result.linear.x == pytest.approx(v)
    assert result.angular.z == pytest.approx(v * math.tan(delta) / 0.8)
    assert result.linear.y == result.linear.z == result.angular.x == result.angular.y == 0


@pytest.mark.parametrize('speed,angle', [
    (math.nan, 0), (math.inf, 0), (-math.inf, 0),
    (0.5, math.nan), (0.5, math.inf), (0.5, -math.inf)])
def test_non_finite_stop(speed, angle):
    result, reason = to_twist(command(speed, angle), 10.1)
    assert reason == 'non_finite'
    assert result.linear.x == result.angular.z == 0


@pytest.mark.parametrize('now,reason', [(10.25, ''), (10.251, 'stale'), (9.9, 'future_stamp')])
def test_stamp_boundary(now, reason):
    result, actual = to_twist(command(0.5, 0.2), now)
    assert actual == reason
    assert (result.linear.x == 0) == bool(reason)


def raw_odom():
    msg = Odometry()
    msg.header.frame_id = 'course_ackermann/odom'
    msg.child_frame_id = 'course_ackermann/base_link'
    msg.header.stamp.sec, msg.header.stamp.nanosec = 123, 456789
    msg.pose.pose.position.x, msg.pose.pose.position.y = 1.2, -0.3
    msg.pose.pose.orientation.z, msg.pose.pose.orientation.w = math.sin(0.2), math.cos(0.2)
    msg.twist.twist.linear.x, msg.twist.twist.angular.z = 0.4, -0.1
    msg.pose.covariance = [i * 0.01 for i in range(36)]
    msg.twist.covariance = [i * 0.02 for i in range(36)]
    return msg


def test_odom_preserves_everything_except_frames_and_matches_tf():
    raw = raw_odom()
    before = deepcopy(raw)
    result, tf = normalize_odometry(raw)
    expected = deepcopy(before)
    expected.header.frame_id, expected.child_frame_id = 'odom', 'base_link'
    assert result == expected
    assert raw == before
    assert tf.header == result.header
    assert tf.child_frame_id == result.child_frame_id
    assert tf.transform.translation.x == result.pose.pose.position.x
    assert tf.transform.translation.y == result.pose.pose.position.y
    assert tf.transform.translation.z == result.pose.pose.position.z
    assert tf.transform.rotation == result.pose.pose.orientation


@pytest.mark.parametrize('field,value', [
    ('header.frame_id', 'odom'), ('child_frame_id', 'base_link'),
    ('header.frame_id', 'other/odom'), ('child_frame_id', 'other/base_link'),
    ('pose.pose.position.x', math.nan), ('pose.pose.orientation.w', math.inf),
    ('twist.twist.linear.x', math.inf), ('twist.twist.angular.z', math.nan)])
def test_reject_bad_odometry(field, value):
    raw = raw_odom()
    obj = raw
    parts = field.split('.')
    for key in parts[:-1]:
        obj = getattr(obj, key)
    setattr(obj, parts[-1], value)
    with pytest.raises(ValueError):
        normalize_odometry(raw)


@pytest.mark.parametrize('field', ['pose', 'twist'])
def test_reject_bad_covariance(field):
    raw = raw_odom()
    getattr(raw, field).covariance[35] = math.nan
    with pytest.raises(ValueError, match='non_finite'):
        normalize_odometry(raw)
