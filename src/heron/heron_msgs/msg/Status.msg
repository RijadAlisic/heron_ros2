# Specific system status data, transmitted by the MCU at 1Hz on status topic.

std_msgs/Header header

# Commit of firmware source.
string hardware_id

# Times since MCU power-on and MCU rosserial connection, respectively.
builtin_interfaces/Duration mcu_uptime
builtin_interfaces/Duration connection_uptime

# Temperature of PCB as measured by internal AVR thermometer,
# reported in degrees centigrade.
float32 pcb_temperature

# Current sense available on platform, in amps.
# Averaged over the message period.
float32 user_current

# Integration of power consumption since MCU power-on, in watt-hours.
float32 user_power_consumed
float32 motor_power_consumed
float32 total_power_consumed
