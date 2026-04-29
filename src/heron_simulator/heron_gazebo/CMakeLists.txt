cmake_minimum_required(VERSION 3.8)
project(heron_gazebo)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)

# Install Python scripts
install(PROGRAMS
  scripts/activate_control_service
  scripts/cmd_drive_translate
  scripts/navsat_vel_translate
  scripts/rpy_translator
  scripts/twist_translate
  scripts/vector3_to_magnetic_field
  DESTINATION lib/${PROJECT_NAME}
)

# Install directories
install(DIRECTORY
  config
  launch
  worlds
  urdf
  DESTINATION share/${PROJECT_NAME}/
)

ament_package()
