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

"""Relay a best-effort pose stream and monitor it with explicit QoS."""

from patrol.pose_type import Pose
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile, ReliabilityPolicy


def sensor_qos(reliability):
    """Build a bounded volatile profile; reject misspelled reliability."""
    policies = {'reliable': ReliabilityPolicy.RELIABLE,
                'best_effort': ReliabilityPolicy.BEST_EFFORT}
    if reliability not in policies:
        raise ValueError('subscriber_reliability must be reliable or best_effort')
    return QoSProfile(depth=10, reliability=policies[reliability],
                      durability=DurabilityPolicy.VOLATILE)


class PoseRelay(Node):
    """Offer best-effort samples on a relative sensor_pose topic."""

    def __init__(self):
        super().__init__('pose_relay')
        self.publisher = self.create_publisher(Pose, 'sensor_pose', sensor_qos('best_effort'))
        self.subscription = self.create_subscription(
            Pose, 'pose', self.publisher.publish, sensor_qos('best_effort'))


class PoseMonitor(Node):
    """Count delivered samples using the requested subscription policy."""

    def __init__(self):
        super().__init__('pose_monitor')
        self.declare_parameter('subscriber_reliability', 'reliable')
        reliability = self.get_parameter('subscriber_reliability').value
        self.count = 0
        self.subscription = self.create_subscription(
            Pose, 'sensor_pose', self.on_pose, sensor_qos(reliability))
        self.timer = self.create_timer(1.0, self.log_count)

    def on_pose(self, message):
        """Count only messages actually delivered to this subscriber."""
        self.count += 1

    def log_count(self):
        """Expose absence or presence of delivery in the launch log."""
        self.get_logger().info(f'received={self.count}')


def run(node_type, args=None):
    """Run a relay or monitor with orderly SIGINT cleanup."""
    rclpy.init(args=args)
    node = node_type()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


def relay_main(args=None):
    """Start the best-effort relay."""
    run(PoseRelay, args)


def monitor_main(args=None):
    """Start the configurable subscriber."""
    run(PoseMonitor, args)
