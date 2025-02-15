cmake_minimum_required(VERSION 3.5)
project(demo_spacestation_gnc_rep)

find_package(ament_cmake REQUIRED)
find_package(xacro REQUIRED)
find_package(robot_state_publisher REQUIRED)
find_package(rviz2 REQUIRED)

install(DIRECTORY launch urdf rviz
  DESTINATION share/${PROJECT_NAME}/
)

ament_package()
