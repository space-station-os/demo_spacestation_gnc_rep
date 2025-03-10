#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include <iostream>
#include <vector>
#include <sstream>
#include <iomanip>

using std::placeholders::_1;

class SDFTestNode : public rclcpp::Node
{
public:
    SDFTestNode() : Node("test_sdf_loader")
    {
        auto qos = rclcpp::QoS(rclcpp::KeepLast(1)).transient_local();

        // 各トピックの購読
        thruster_sub_ = this->create_subscription<std_msgs::msg::String>(
            "/spacestation/thrusters", qos, std::bind(&SDFTestNode::thruster_callback, this, _1));

        docking_port_sub_ = this->create_subscription<std_msgs::msg::String>(
            "/spacestation/docking_ports", qos, std::bind(&SDFTestNode::docking_port_callback, this, _1));

        sensor_sub_ = this->create_subscription<std_msgs::msg::String>(
            "/spacestation/sensors", qos, std::bind(&SDFTestNode::sensor_callback, this, _1));

        RCLCPP_INFO(this->get_logger(), "Waiting for latched messages...");
    }

private:
    void thruster_callback(const std_msgs::msg::String::SharedPtr msg)
    {
        std::istringstream stream(msg->data);
        std::string line;
        std::vector<std::tuple<std::string, std::string, double>> thrusters;

        while (std::getline(stream, line, '}')) {
            size_t name_pos = line.find("\"name\":");
            size_t pose_pos = line.find("\"pose\":");
            size_t force_pos = line.find("\"force\":");

            if (name_pos != std::string::npos && pose_pos != std::string::npos && force_pos != std::string::npos) {
                std::string name = line.substr(name_pos + 8, line.find(",", name_pos) - (name_pos + 9));
                std::string pose = line.substr(pose_pos + 8, line.find(",", pose_pos) - (pose_pos + 9));
                double force = std::stod(line.substr(force_pos + 8));

                thrusters.push_back(std::make_tuple(name, pose, force));
            }
        }

        // 整形されたリスト形式で出力
        RCLCPP_INFO(this->get_logger(), "\n=== Thruster List ===");
        printf("%-40s | %-30s | %-10s\n", "Name", "Pose", "Force");
        printf("----------------------------------------------------------------------------------------\n");
        for (const auto &thruster : thrusters) {
            printf("%-40s | %-30s | %-10.2f\n",
                   std::get<0>(thruster).c_str(),
                   std::get<1>(thruster).c_str(),
                   std::get<2>(thruster));
        }
        printf("\n");
    }

    void docking_port_callback(const std_msgs::msg::String::SharedPtr msg)
    {
        std::istringstream stream(msg->data);
        std::string line;
        std::vector<std::tuple<std::string, std::string>> docking_ports;

        while (std::getline(stream, line, '}')) {
            size_t name_pos = line.find("\"name\":");
            size_t pose_pos = line.find("\"pose\":");

            if (name_pos != std::string::npos && pose_pos != std::string::npos) {
                std::string name = line.substr(name_pos + 8, line.find(",", name_pos) - (name_pos + 9));
                std::string pose = line.substr(pose_pos + 8, line.find(",", pose_pos) - (pose_pos + 9));

                docking_ports.push_back(std::make_tuple(name, pose));
            }
        }

        // 整形されたリスト形式で出力
        RCLCPP_INFO(this->get_logger(), "\n=== Docking Port List ===");
        printf("%-40s | %-30s\n", "Name", "Pose");
        printf("------------------------------------------------------------------\n");
        for (const auto &port : docking_ports) {
            printf("%-40s | %-30s\n",
                   std::get<0>(port).c_str(),
                   std::get<1>(port).c_str());
        }
        printf("\n");
    }

    void sensor_callback(const std_msgs::msg::String::SharedPtr msg)
    {
        std::istringstream stream(msg->data);
        std::string line;
        std::vector<std::tuple<std::string, std::string>> sensors;

        while (std::getline(stream, line, '}')) {
            size_t name_pos = line.find("\"name\":");
            size_t pose_pos = line.find("\"pose\":");

            if (name_pos != std::string::npos && pose_pos != std::string::npos) {
                std::string name = line.substr(name_pos + 8, line.find(",", name_pos) - (name_pos + 9));
                std::string pose = line.substr(pose_pos + 8, line.find(",", pose_pos) - (pose_pos + 9));

                sensors.push_back(std::make_tuple(name, pose));
            }
        }

        // 整形されたリスト形式で出力
        RCLCPP_INFO(this->get_logger(), "\n=== Sensor List ===");
        printf("%-40s | %-30s\n", "Name", "Pose");
        printf("------------------------------------------------------------------\n");
        for (const auto &sensor : sensors) {
            printf("%-40s | %-30s\n",
                   std::get<0>(sensor).c_str(),
                   std::get<1>(sensor).c_str());
        }
        printf("\n");
    }

    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr thruster_sub_;
    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr docking_port_sub_;
    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr sensor_sub_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<SDFTestNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
