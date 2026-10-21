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

"""Contract boundaries for the course Ackermann model, in simulation time."""

from copy import deepcopy
import math

from ackermann_msgs.msg import AckermannDriveStamped
from geometry_msgs.msg import TransformStamped, Twist
from nav_msgs.msg import Odometry
import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster


def stamp_seconds(stamp):
    return stamp.sec + stamp.nanosec * 1e-9


def to_twist(command, now):
    """Return a fresh Twist and a rejection reason; never reuse an old command."""
    result = Twist()
    v, delta = command.drive.speed, command.drive.steering_angle
    if not all(math.isfinite(x) for x in (v, delta)):
        return result, 'non_finite'
    age = now - stamp_seconds(command.header.stamp)
    if age > 0.25:
        return result, 'stale'
    if age < -0.01:
        return result, 'future_stamp'
    v = min(max(v, 0.0), 1.2)
    delta = min(max(delta, -0.45), 0.45)
    result.linear.x = v
    result.angular.z = v * math.tan(delta) / 0.8
    return result, ''


def normalize_odometry(message):
    """Validate raw frames/numbers and copy all values except the two frame IDs."""
    if (message.header.frame_id != 'course_ackermann/odom' or
            message.child_frame_id != 'course_ackermann/base_link'):
        raise ValueError('unexpected_frames')
    p, q = message.pose.pose.position, message.pose.pose.orientation
    v, w = message.twist.twist.linear, message.twist.twist.angular
    values = [p.x, p.y, p.z, q.x, q.y, q.z, q.w,
              v.x, v.y, v.z, w.x, w.y, w.z,
              *message.pose.covariance, *message.twist.covariance]
    if not all(math.isfinite(x) for x in values):
        raise ValueError('non_finite')
    result = deepcopy(message)
    result.header.frame_id = 'odom'
    result.child_frame_id = 'base_link'
    transform = TransformStamped()
    transform.header = deepcopy(result.header)
    transform.child_frame_id = result.child_frame_id
    transform.transform.translation.x = p.x
    transform.transform.translation.y = p.y
    transform.transform.translation.z = p.z
    transform.transform.rotation = deepcopy(q)
    return result, transform


class DriveAdapter(Node):
    def __init__(self):
        super().__init__('ackermann_adapter')
        incoming = self.declare_parameter('input_topic', '/drive/safe').value
        outgoing = self.declare_parameter('output_topic', '/vehicle/gz_cmd_vel').value
        self.publisher = self.create_publisher(Twist, outgoing, 10)
        self.subscription = self.create_subscription(
            AckermannDriveStamped, incoming, self.receive, 10)
        self.last_stamp = None
        self.stopped = True
        self.timer = self.create_timer(0.02, self.watchdog)

    def receive(self, message):
        command, reason = to_twist(message, self.get_clock().now().nanoseconds * 1e-9)
        self.publisher.publish(command)
        self.last_stamp = stamp_seconds(message.header.stamp) if not reason else None
        self.stopped = bool(reason) or (command.linear.x == 0.0)
        if reason:
            self.get_logger().warning('Command rejected: ' + reason, throttle_duration_sec=1)

    def watchdog(self):
        now = self.get_clock().now().nanoseconds * 1e-9
        if self.last_stamp is not None and not self.stopped:
            if now - self.last_stamp > 0.25 or now < self.last_stamp - 0.01:
                self.publisher.publish(Twist())
                self.stopped = True
                self.get_logger().warning('Command timeout: zero Twist')


class OdomAdapter(Node):
    def __init__(self):
        super().__init__('odom_adapter')
        incoming = self.declare_parameter('input_topic', '/vehicle/odom_gz').value
        outgoing = self.declare_parameter('output_topic', '/vehicle/odom').value
        self.publisher = self.create_publisher(Odometry, outgoing, 10)
        self.tf = TransformBroadcaster(self)
        self.subscription = self.create_subscription(Odometry, incoming, self.receive, 10)

    def receive(self, message):
        try:
            normalized, transform = normalize_odometry(message)
        except ValueError as error:
            self.get_logger().warning('Odometry rejected: ' + str(error), throttle_duration_sec=1)
            return
        self.publisher.publish(normalized)
        self.tf.sendTransform(transform)


def run(node_class, args=None):
    rclpy.init(args=args)
    node = node_class()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


def drive_main(args=None):
    run(DriveAdapter, args)


def odom_main(args=None):
    run(OdomAdapter, args)
