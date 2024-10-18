import datetime
from django.core.management.base import BaseCommand, CommandError
from Sensores.models import SensorStats
from Equipos.models import Equipo
from django.db.models.query import QuerySet
from csv import writer as csv_writer
from datetime import datetime


class Command(BaseCommand):
    help = "Dumps the sensors stats in a csv"

    def add_arguments(self, parser):
        parser.add_argument("id", type=int)

    def handle(self, *args, **options):
        try:
            computer_id = options["id"]
            self.stdout.write(
                self.style.WARNING(
                    f"Searching for computer with ID [{computer_id}] to dump sensors stats"
                )
            )
            computer = Equipo.objects.get(id=computer_id)

            self.stdout.write(
                self.style.WARNING(
                    f"Found computer [{computer.hostname} - {computer.area.nombre}]"
                )
            )
            sensors: QuerySet[SensorStats] = SensorStats.objects.filter(equipo=computer)

            self.stdout.write(
                self.style.WARNING(f"Dumping {len(sensors)} sensors stats")
            )

            with open(
                f"{computer.hostname}_{datetime.today().strftime('%Y-%m-%d')}_sensors.csv",
                "w",
            ) as f:
                csv = csv_writer(f)
                csv.writerow(
                    [
                        "fecha_registro",
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
                        "memory_load",
                        "memory_available",
                        "memory_used",
                        "avg_used_space",
                        "avg_read",
                        "avg_write",
                        "avg_activity",
                        "max_used_space",
                        "max_read",
                        "max_write",
                        "max_activity",
                    ]
                )
                for sensor in sensors:
                    csv.writerow(
                        [
                            sensor.fecha_registro,
                            sensor.cpu_total_load,
                            sensor.cpu_core_max_load,
                            sensor.cpu_core_max_temp,
                            sensor.cpu_core_avg_temp,
                            sensor.cpu_avg_core_clock,
                            sensor.cpu_bus_speed_clock,
                            sensor.cpu_package_power,
                            sensor.cpu_cores_power,
                            sensor.cpu_memory_power,
                            sensor.cpu_core_voltage,
                            sensor.memory_load,
                            sensor.memory_available,
                            sensor.memory_used,
                            sensor.avg_used_space,
                            sensor.avg_read,
                            sensor.avg_write,
                            sensor.avg_activity,
                            sensor.max_used_space,
                            sensor.max_read,
                            sensor.max_write,
                            sensor.max_activity,
                        ]
                    )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Dumped sensors stats for computer [{computer.hostname} - {computer.area.nombre}]"
                )
            )
        except:
            self.stdout.write(self.style.ERROR("Error dumping sensors stats"))
