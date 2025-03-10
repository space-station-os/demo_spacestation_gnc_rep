#!/usr/bin/env python3
import rclpy
import json
import xml.etree.ElementTree as ET
from rclpy.node import Node
from std_msgs.msg import String
from rclpy.qos import QoSProfile, QoSDurabilityPolicy

class SDFLoader(Node):
    def __init__(self):
        super().__init__('sdf_loader')

        # ROS2 の QoS 設定（Latched Topic）
        latched_qos = QoSProfile(depth=1, durability=QoSDurabilityPolicy.TRANSIENT_LOCAL)

        # パラメータの読み込み
        self.declare_parameter('sdf_file', 'sdf/spacestation_all.sdf')
        sdf_file = self.get_parameter('sdf_file').value

        # ROS2 トピックの定義
        self.thruster_pub = self.create_publisher(String, '/spacestation/thrusters', latched_qos)
        self.docking_port_pub = self.create_publisher(String, '/spacestation/docking_ports', latched_qos)
        self.sensor_pub = self.create_publisher(String, '/spacestation/sensors', latched_qos)

        # SDF ファイルのロードと解析
        thrusters, docking_ports, sensors = self.load_sdf(sdf_file)

        # データをトピックに発行
        self.publish_data(thrusters, docking_ports, sensors)

        self.get_logger().info("SDF data loaded and published successfully.")

    def load_sdf(self, sdf_file):
        """ spacestation_all.sdf を解析し、スラスター、ドッキングポート、センサーの情報を取得 """
        try:
            tree = ET.parse(sdf_file)
            root = tree.getroot()
            model = root.find("model")

            thrusters, docking_ports, sensors = [], [], []

            for joint in model.findall(".//joint"):
                child_name = joint.find("child").text
                pose = joint.find("pose").text

                if "thruster" in child_name:
                    thrusters.append({"name": child_name, "pose": pose, "force": 30.0})
                elif "docking_port" in child_name:
                    docking_ports.append({"name": child_name, "pose": pose})
                elif "sensor" in child_name:
                    sensors.append({"name": child_name, "pose": pose})

            return thrusters, docking_ports, sensors

        except Exception as e:
            self.get_logger().error(f"Failed to load SDF file {sdf_file}: {e}")
            return [], [], []

    def publish_data(self, thrusters, docking_ports, sensors):
        """ 取得した SDF データを ROS2 のトピックに発行 """
        self.thruster_pub.publish(String(data=json.dumps(thrusters)))
        self.docking_port_pub.publish(String(data=json.dumps(docking_ports)))
        self.sensor_pub.publish(String(data=json.dumps(sensors)))

        self.get_logger().info("Published thruster, docking port, and sensor data.")

def main(args=None):
    rclpy.init(args=args)
    node = SDFLoader()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
