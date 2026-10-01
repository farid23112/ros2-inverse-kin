import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64


class InverseKinematics(Node):
    def __init__(self):
        super().__init__('inverse_kinematics')

        self.wheel_radius = 0.10
        self.wheel_separation = 0.45

        self.create_subscription(
            Twist, '/input_ik', self.velocity_callback, 10
        )

        self.left_publisher = self.create_publisher(
            Float64, '/left_wheel/command', 10
        )
        self.right_publisher = self.create_publisher(
            Float64, '/right_wheel/command', 10
        )
        self.cmd_vel_publisher = self.create_publisher(
            Twist, '/cmd_vel', 10
        )

        self.get_logger().info('Inverse Kinematics aktif.')
        self.get_logger().info(
            f'wheel_radius={self.wheel_radius} m, '
            f'wheel_separation={self.wheel_separation} m'
        )

    def velocity_callback(self, msg):
        v = msg.linear.x
        omega = msg.angular.z

        left_velocity = (
            v - omega * self.wheel_separation / 2.0
        ) / self.wheel_radius
        right_velocity = (
            v + omega * self.wheel_separation / 2.0
        ) / self.wheel_radius

        left_msg = Float64()
        left_msg.data = left_velocity

        right_msg = Float64()
        right_msg.data = right_velocity

        self.left_publisher.publish(left_msg)
        self.right_publisher.publish(right_msg)

        # Robot Gazebo dikendalikan melalui /cmd_vel
        self.cmd_vel_publisher.publish(msg)

        self.get_logger().info(
            f'Input: v={v:.3f} m/s, omega={omega:.3f} rad/s | '
            f'Left={left_velocity:.3f} rad/s, '
            f'Right={right_velocity:.3f} rad/s'
        )


def main(args=None):
    rclpy.init(args=args)
    node = InverseKinematics()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.cmd_vel_publisher.publish(Twist())
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
