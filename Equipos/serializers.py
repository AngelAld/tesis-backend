from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from Equipos.models import (
    EstadoEquipo,
    EstadoAlerta,
    Area,
    Equipo,
    Cpu,
    Memory,
    Disk,
    Modelo,
)
from django.utils.timezone import now
from django.db.transaction import atomic
from Sensores.models import SensorStats

estadoEquipoDefault, _ = EstadoEquipo.objects.get_or_create(nombre="Bueno")
estadoAlertaDefault, _ = EstadoAlerta.objects.get_or_create(nombre="Sin alerta")
# estadoHardwareDefault, _ = EstadoHardware.objects.get_or_create(nombre="Bueno")


def validateAreaIp(area: Area, ip):
    if splitAreaIp(ip) == area.ip:
        return True
    return False


def splitAreaIp(ip: str):
    area_ip = ip.split(".")
    area_ip = area_ip[0] + "." + area_ip[1] + "." + area_ip[2] + ".0"
    return area_ip


def getAreaByIp(ip: str):
    area = Area.objects.filter(ip=splitAreaIp(ip)).first()
    if not area:
        new_area = Area.objects.create(
            nombre="Area autogenerada",
            ip=splitAreaIp(ip),
        )
        return new_area
    return area


class CpuSerializer(ModelSerializer):
    estado = serializers.CharField(source="estado.nombre", read_only=True)

    class Meta:
        model = Cpu
        fields = [
            "id",
            "nombre",
            # "estado",
            "fecha_registro",
            "estado",
        ]
        read_only_fields = ["id", "fecha_registro"]

    @atomic
    def create(self, validated_data):
        equipo = validated_data.get("equipo")
        nombre = validated_data.get("nombre")
        estado = estadoAlertaDefault
        fecha_registro = now()

        cpu, _ = Cpu.objects.get_or_create(
            equipo=equipo,
            nombre=nombre,
            defaults={"estado": estado, "fecha_registro": fecha_registro},
        )

        return cpu


class MemorySerializer(ModelSerializer):
    estado = serializers.CharField(source="estado.nombre", read_only=True)

    class Meta:
        model = Memory
        fields = [
            "id",
            "nombre",
            "fecha_registro",
            "estado",
        ]
        read_only_fields = ["id", "fecha_registro"]

    @atomic
    def create(self, validated_data):
        equipo = validated_data.get("equipo")
        nombre = validated_data.get("nombre")
        estado = estadoAlertaDefault
        fecha_registro = now()

        memory, created = Memory.objects.get_or_create(
            equipo=equipo,
            nombre=nombre,
            defaults={"estado": estado, "fecha_registro": fecha_registro},
        )

        if not created:
            memory.estado = estado
            memory.fecha_registro = fecha_registro
            memory.save()

        return memory


class DiskSerializer(ModelSerializer):
    estado = serializers.CharField(source="estado.nombre", read_only=True)

    class Meta:
        model = Disk
        fields = [
            "id",
            "nombre",
            "fecha_registro",
            "estado",
        ]
        read_only_fields = ["id", "fecha_registro"]

    @atomic
    def create(self, validated_data):
        equipo = validated_data.get("equipo")
        nombre = validated_data.get("nombre")
        estado = estadoAlertaDefault
        fecha_registro = now()

        disk, created = Disk.objects.get_or_create(
            equipo=equipo,
            nombre=nombre,
            defaults={"estado": estado, "fecha_registro": fecha_registro},
        )
        if not created:
            disk.estado = estado
            disk.fecha_registro = fecha_registro
            disk.save()

        return disk


# este es para los agentes
class EquipoSerializer(ModelSerializer):

    cpu_set = CpuSerializer(
        many=True,
        read_only=False,
    )
    memory_set = MemorySerializer(many=True, read_only=False)
    disk_set = DiskSerializer(many=True, read_only=False)

    class Meta:
        model = Equipo
        fields = [
            "id",
            "hostname",
            "ip",
            "area",
            "estado",
            "fecha_registro",
            "last_update",
            "estado_equipo",
            "estado_alerta",
            "cpu_set",
            "memory_set",
            "disk_set",
        ]
        read_only_fields = [
            "id",
            "estado",
            "area",
            "fecha_registro",
            "last_update",
            "estado_equipo",
            "estado_alerta",
        ]
        extra_kwargs = {
            "area_id": {"write_only": True},
        }

    @atomic
    def create(self, validated_data):
        hostname = validated_data.get("hostname")
        ip = validated_data.get("ip")
        estado = True
        last_update = now()
        estado_equipo = estadoEquipoDefault
        estado_alerta = estadoAlertaDefault
        area = getAreaByIp(ip)
        # hardware

        cpus = validated_data.pop("cpu_set", [])
        memorys = validated_data.pop("memory_set", [])
        disks = validated_data.pop("disk_set", [])

        equipo, created = Equipo.objects.get_or_create(
            hostname=hostname,
            defaults={
                "ip": ip,
                "estado": estado,
                "area": area,
                "last_update": last_update,
                "estado_equipo": estado_equipo,
                "estado_alerta": estado_alerta,
            },
        )
        if not created:
            equipo.last_update = last_update
            equipo.ip = ip
            equipo.area = area
            equipo.save()

        for cpu in cpus:
            cpu["equipo"] = equipo
            CpuSerializer().create(cpu)

        for memory in memorys:
            memory["equipo"] = equipo
            MemorySerializer().create(memory)
        for disk in disks:
            disk["equipo"] = equipo
            DiskSerializer().create(disk)

        return equipo


class SensoresSerializer(serializers.Serializer):
    cpu = serializers.SerializerMethodField()
    memoria = serializers.SerializerMethodField()
    disco = serializers.SerializerMethodField()

    def get_cpu(self, obj):
        if obj["current"].cpu_core_avg_temp > 60:
            print("Alerta de temperatura")
        return {
            "temperatura": obj["current"].cpu_core_avg_temp,
        }

    def get_memoria(self, obj):
        return {
            "usada": obj["current"].memory_load,
        }

    def get_disco(self, obj):
        return {
            "usado": obj["current"].avg_activity,
        }


# este es para la api


class EquipoListSerializer(serializers.ModelSerializer):
    estado_equipo = serializers.CharField(source="estado_equipo.nombre")
    estado_alerta = serializers.CharField(source="estado_alerta.nombre")
    sensores = serializers.SerializerMethodField()

    class Meta:
        model = Equipo
        fields = [
            "id",
            "hostname",
            "ip",
            "last_update",
            "estado_equipo",
            "estado_alerta",
            "sensores",
        ]

    def get_sensores(self, obj):
        try:
            latest_stats = SensorStats.objects.filter(equipo=obj).order_by(
                "-fecha_registro"
            )[:2]
            if len(latest_stats) < 2:
                return None
            stats_data = {"current": latest_stats[0], "previous": latest_stats[1]}
            return SensoresSerializer(stats_data).data
        except SensorStats.DoesNotExist:
            return None


class EquipoDetalleSerializer(serializers.ModelSerializer):
    estado_equipo = serializers.CharField(source="estado_equipo.nombre")
    estado_alerta = serializers.CharField(source="estado_alerta.nombre")
    cpu_set = CpuSerializer(many=True)
    memory_set = MemorySerializer(many=True)
    disk_set = DiskSerializer(many=True)
    area = serializers.CharField(source="area.nombre")

    class Meta:
        model = Equipo
        fields = [
            "id",
            "hostname",
            "ip",
            "area",
            "modelo",
            "estado",
            "fecha_registro",
            "last_update",
            "estado_equipo",
            "estado_alerta",
            "cpu_set",
            "memory_set",
            "disk_set",
        ]
        read_only_fields = [
            "id",
            "hostname",
            "ip",
            "area",
            "estado",
            "fecha_registro",
            "last_update",
            "cpu_set",
            "memory_set",
            "disk_set",
        ]

    @atomic
    def update(self, instance, validated_data):
        validated_data.pop("cpu_set", None)
        validated_data.pop("memory_set", None)
        validated_data.pop("disk_set", None)
        instance.modelo = validated_data.get("modelo", instance.modelo)
        instance.save()
        return instance


class ModeloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modelo
        fields = "__all__"
