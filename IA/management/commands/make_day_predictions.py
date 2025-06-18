from django.core.management.base import BaseCommand
from IA.models import ModeloIA, Prediccion, cpu_columns, disk_columns, mem_columns
from Sensores.models import SensorStats
from Equipos.models import Cpu, Disk, Equipo, Memory
from datetime import datetime, timedelta, time
from django.utils import timezone

from IA.util import generarAlerta, predecir
from django.db.models import Avg, Max


class Command(BaseCommand):
    help = "Genera las predicciones del dia para los equipos"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting the prediction process..."))

        # primero obtenemos la data de los sensores del dia
        stats = SensorStats.objects.filter(fecha_registro__date=timezone.now().date())
        self.stdout.write(
            self.style.SUCCESS(f"Found {stats.count()} sensor stats for today.")
        )

        # luego obtenemos un modelo de IA
        modelo = ModeloIA.objects.get(id=14)
        self.stdout.write(self.style.SUCCESS(f"Using AI model with ID {modelo.id}."))  # type: ignore

        variable_objetivo = modelo.variable_objetivo
        componente = modelo.componente

        columns = []
        if componente == "cpu":
            columns = cpu_columns
        elif componente == "ram":
            columns = mem_columns
        elif componente == "disk":
            columns = disk_columns

        equipos = Equipo.objects.all()

        for equipo in equipos:
            today = timezone.localtime(timezone.now()).date()
            start_of_day = timezone.make_aware(datetime.combine(today, time.min))
            end_of_day = timezone.make_aware(datetime.combine(today, time.max))

            interval = timedelta(minutes=20)
            current_time = start_of_day

            while current_time < end_of_day:
                next_time = current_time + interval
                stats = SensorStats.objects.filter(
                    equipo=equipo,
                    fecha_registro__gte=current_time,
                    fecha_registro__lt=next_time,
                )

                if stats.count() == 0:
                    self.stdout.write(
                        self.style.WARNING(
                            f"No stats found for time range {current_time} - {next_time}."
                        )
                    )
                    current_time = next_time
                    continue

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Processing stats for {equipo.hostname} from {current_time} to {next_time}."
                    )
                )

                avg_variables = []
                max_variables = []
                for column in columns:
                    if column != variable_objetivo:
                        avg_value = stats.aggregate(avg_value=Avg(column))["avg_value"]
                        max_value = stats.aggregate(max_value=Max(column))["max_value"]
                        avg_variables.append(avg_value)
                        max_variables.append(max_value)

                avg_expected_value = stats.aggregate(avg_value=Avg(variable_objetivo))[
                    "avg_value"
                ]
                max_expected_value = stats.aggregate(max_value=Max(variable_objetivo))[
                    "max_value"
                ]

                avg_predicted_value = predecir(modelo, avg_variables)
                max_predicted_value = predecir(modelo, max_variables)

                avg_failure_percentage = (
                    abs(avg_expected_value - avg_predicted_value) / avg_expected_value
                    if avg_expected_value
                    else None
                )
                max_failure_percentage = (
                    abs(max_expected_value - max_predicted_value) / max_expected_value
                    if max_expected_value
                    else None
                )

                fecha_registro = current_time

                Prediccion.objects.create(
                    modelo_ia=modelo,
                    modelo_equipo=equipo.modelo,
                    equipo=equipo,
                    cpu_total_load=stats.aggregate(avg_value=Avg("cpu_total_load"))[
                        "avg_value"
                    ],
                    cpu_core_max_load=stats.aggregate(
                        avg_value=Avg("cpu_core_max_load")
                    )["avg_value"],
                    cpu_core_max_temp=stats.aggregate(
                        avg_value=Avg("cpu_core_max_temp")
                    )["avg_value"],
                    cpu_core_avg_temp=stats.aggregate(
                        avg_value=Avg("cpu_core_avg_temp")
                    )["avg_value"],
                    cpu_avg_core_clock=stats.aggregate(
                        avg_value=Avg("cpu_avg_core_clock")
                    )["avg_value"],
                    cpu_bus_speed_clock=stats.aggregate(
                        avg_value=Avg("cpu_bus_speed_clock")
                    )["avg_value"],
                    cpu_package_power=stats.aggregate(
                        avg_value=Avg("cpu_package_power")
                    )["avg_value"],
                    cpu_cores_power=stats.aggregate(avg_value=Avg("cpu_cores_power"))[
                        "avg_value"
                    ],
                    cpu_memory_power=stats.aggregate(avg_value=Avg("cpu_memory_power"))[
                        "avg_value"
                    ],
                    cpu_core_voltage=stats.aggregate(avg_value=Avg("cpu_core_voltage"))[
                        "avg_value"
                    ],
                    memory_load=stats.aggregate(avg_value=Avg("memory_load"))[
                        "avg_value"
                    ],
                    memory_available=stats.aggregate(avg_value=Avg("memory_available"))[
                        "avg_value"
                    ],
                    memory_used=stats.aggregate(avg_value=Avg("memory_used"))[
                        "avg_value"
                    ],
                    avg_used_space=stats.aggregate(avg_value=Avg("avg_used_space"))[
                        "avg_value"
                    ],
                    avg_read=stats.aggregate(avg_value=Avg("avg_read"))["avg_value"],
                    avg_write=stats.aggregate(avg_value=Avg("avg_write"))["avg_value"],
                    avg_activity=stats.aggregate(avg_value=Avg("avg_activity"))[
                        "avg_value"
                    ],
                    max_used_space=stats.aggregate(avg_value=Avg("max_used_space"))[
                        "avg_value"
                    ],
                    max_read=stats.aggregate(avg_value=Avg("max_read"))["avg_value"],
                    max_write=stats.aggregate(avg_value=Avg("max_write"))["avg_value"],
                    max_activity=stats.aggregate(avg_value=Avg("max_activity"))[
                        "avg_value"
                    ],
                    failure_percentage=avg_failure_percentage,
                )

                Prediccion.objects.create(
                    modelo_ia=modelo,
                    modelo_equipo=equipo.modelo,
                    equipo=equipo,
                    cpu_total_load=stats.aggregate(max_value=Max("cpu_total_load"))[
                        "max_value"
                    ],
                    cpu_core_max_load=stats.aggregate(
                        max_value=Max("cpu_core_max_load")
                    )["max_value"],
                    cpu_core_max_temp=stats.aggregate(
                        max_value=Max("cpu_core_max_temp")
                    )["max_value"],
                    cpu_core_avg_temp=stats.aggregate(
                        max_value=Max("cpu_core_avg_temp")
                    )["max_value"],
                    cpu_avg_core_clock=stats.aggregate(
                        max_value=Max("cpu_avg_core_clock")
                    )["max_value"],
                    cpu_bus_speed_clock=stats.aggregate(
                        max_value=Max("cpu_bus_speed_clock")
                    )["max_value"],
                    cpu_package_power=stats.aggregate(
                        max_value=Max("cpu_package_power")
                    )["max_value"],
                    cpu_cores_power=stats.aggregate(max_value=Max("cpu_cores_power"))[
                        "max_value"
                    ],
                    cpu_memory_power=stats.aggregate(max_value=Max("cpu_memory_power"))[
                        "max_value"
                    ],
                    cpu_core_voltage=stats.aggregate(max_value=Max("cpu_core_voltage"))[
                        "max_value"
                    ],
                    memory_load=stats.aggregate(max_value=Max("memory_load"))[
                        "max_value"
                    ],
                    memory_available=stats.aggregate(max_value=Max("memory_available"))[
                        "max_value"
                    ],
                    memory_used=stats.aggregate(max_value=Max("memory_used"))[
                        "max_value"
                    ],
                    avg_used_space=stats.aggregate(max_value=Max("avg_used_space"))[
                        "max_value"
                    ],
                    avg_read=stats.aggregate(max_value=Max("avg_read"))["max_value"],
                    avg_write=stats.aggregate(max_value=Max("avg_write"))["max_value"],
                    avg_activity=stats.aggregate(max_value=Max("avg_activity"))[
                        "max_value"
                    ],
                    max_used_space=stats.aggregate(max_value=Max("max_used_space"))[
                        "max_value"
                    ],
                    max_read=stats.aggregate(max_value=Max("max_read"))["max_value"],
                    max_write=stats.aggregate(max_value=Max("max_write"))["max_value"],
                    max_activity=stats.aggregate(max_value=Max("max_activity"))[
                        "max_value"
                    ],
                    failure_percentage=max_failure_percentage,
                )

                generarAlerta(
                    equipo=equipo,
                    cpu=(
                        Cpu.objects.filter(equipo=equipo)
                        .order_by("-fecha_actualizacion")
                        .first()
                        if componente == "cpu"
                        else None
                    ),
                    memory=(
                        Memory.objects.filter(equipo=equipo)
                        .order_by("-fecha_actualizacion")
                        .first()
                        if componente == "ram"
                        else None
                    ),
                    disk=(
                        Disk.objects.filter(equipo=equipo)
                        .order_by("-fecha_actualizacion")
                        .first()
                        if componente == "disk"
                        else None
                    ),
                    failure_percentage=(
                        avg_failure_percentage
                        if avg_failure_percentage is not None
                        else 0.0
                    ),
                )
                generarAlerta(
                    equipo=equipo,
                    cpu=(
                        Cpu.objects.filter(equipo=equipo)
                        .order_by("-fecha_actualizacion")
                        .first()
                        if componente == "cpu"
                        else None
                    ),
                    memory=(
                        Memory.objects.filter(equipo=equipo)
                        .order_by("-fecha_actualizacion")
                        .first()
                        if componente == "ram"
                        else None
                    ),
                    disk=(
                        Disk.objects.filter(equipo=equipo)
                        .order_by("-fecha_actualizacion")
                        .first()
                        if componente == "disk"
                        else None
                    ),
                    failure_percentage=(
                        max_failure_percentage
                        if max_failure_percentage is not None
                        else 0.0
                    ),
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Predictions saved for {equipo} at {fecha_registro}."
                    )
                )

                current_time = next_time
