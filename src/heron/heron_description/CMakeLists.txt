cmake_minimum_required(VERSION 3.8)
project(heron_description)

find_package(ament_cmake REQUIRED)

install(DIRECTORY
  launch
  meshes
  urdf
  scripts
  DESTINATION share/${PROJECT_NAME}/
)

ament_package()
