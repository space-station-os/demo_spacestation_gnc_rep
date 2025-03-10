cmake_minimum_required(VERSION 3.5)
project(demo_spacestation_gnc_rep)

find_package(ament_cmake REQUIRED)
find_package(xacro REQUIRED)
find_package(robot_state_publisher REQUIRED)
find_package(rviz2 REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(nlohmann_json REQUIRED)

# Build the test_sdf_loader node
add_executable(test_sdf_loader src/test_sdf_loader.cpp)
ament_target_dependencies(test_sdf_loader rclcpp std_msgs nlohmann_json)

install(TARGETS test_sdf_loader
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY launch urdf rviz
  DESTINATION share/${PROJECT_NAME}/
)

# Correct way to rename multiple executables
install(PROGRAMS
  src/sdf_loader.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME sdf_loader
)

#install(PROGRAMS
#  src/test_sdf_loader.py
#  DESTINATION lib/${PROJECT_NAME}
#  RENAME test_sdf_loader
#)

ament_package()
