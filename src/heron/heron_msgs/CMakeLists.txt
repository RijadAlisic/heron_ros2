cmake_minimum_required(VERSION 3.8)
project(heron_msgs)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(std_msgs REQUIRED)
find_package(builtin_interfaces REQUIRED)  # ADD THIS LINE

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Course.msg"
  "msg/Drive.msg"
  "msg/Helm.msg"
  "msg/Sense.msg"
  "msg/Status.msg"
  DEPENDENCIES std_msgs builtin_interfaces  # ADD builtin_interfaces HERE
)

ament_package()
