import numpy as np

cpu_columns = [
    "cpu_total_load",
    "cpu_core_max_load",
    "cpu_core_max_temp",
    "cpu_core_avg_temp",
    "cpu_avg_core_clock",
    "cpu_bus_speed_clock",
    "cpu_package_power",
    "cpu_cores_power",
    "cpu_memory_power",
    "cpu_core_voltage",
]
mem_columns = [
    "cpu_total_load",
    "cpu_core_max_temp",
    "cpu_core_avg_temp",
    "cpu_avg_core_clock",
    "memory_load",
    "memory_available",
    "memory_used",
]
disk_columns = [
    "avg_used_space",
    "avg_read",
    "avg_write",
    "avg_activity",
    "max_used_space",
    "max_read",
    "max_write",
    "max_activity",
]
