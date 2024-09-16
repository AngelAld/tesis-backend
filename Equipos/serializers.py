from rest_framework.serializers import ModelSerializer, IntegerField
from Equipos.models import (
    EstadoEquipo,
    EstadoAlerta,
    EstadoHardware,
    Area,
    Equipo,
    Cpu,
    Memory,
    Disk,
)
from django.utils.timezone import now
from django.db.transaction import atomic


estadoEquipoDefault, _ = EstadoEquipo.objects.get_or_create(nombre="Bueno")
estadoAlertaDefault, _ = EstadoAlerta.objects.get_or_create(nombre="Sin alerta")
estadoHardwareDefault, _ = EstadoHardware.objects.get_or_create(nombre="Bueno")


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
    class Meta:
        model = Cpu
        fields = [
            "id",
            "nombre",
            "estado",
            "fecha_registro",
        ]
        read_only_fields = ["id", "fecha_registro", "estado"]

    @atomic
    def create(self, validated_data):
        equipo = validated_data.get("equipo")
        nombre = validated_data.get("nombre")
        estado = estadoHardwareDefault
        fecha_registro = now()

        cpu, _ = Cpu.objects.get_or_create(
            equipo=equipo,
            nombre=nombre,
            defaults={"estado": estado, "fecha_registro": fecha_registro},
        )

        return cpu


class MemorySerializer(ModelSerializer):
    class Meta:
        model = Memory
        fields = [
            "id",
            "nombre",
            "fecha_registro",
        ]
        read_only_fields = ["id", "fecha_registro"]

    @atomic
    def create(self, validated_data):
        equipo = validated_data.get("equipo")
        nombre = validated_data.get("nombre")
        estado = estadoHardwareDefault
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
    class Meta:
        model = Disk
        fields = [
            "id",
            "nombre",
            "fecha_registro",
        ]
        read_only_fields = ["id", "fecha_registro"]

    @atomic
    def create(self, validated_data):
        equipo = validated_data.get("equipo")
        nombre = validated_data.get("nombre")
        estado = estadoHardwareDefault
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
            ip=ip,
            area=area,
            defaults={
                "estado": estado,
                "last_update": last_update,
                "estado_equipo": estado_equipo,
                "estado_alerta": estado_alerta,
            },
        )
        if not created:
            equipo.last_update = last_update
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
