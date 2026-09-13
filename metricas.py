import csv
import psutil
from datetime import datetime


class Metrica:
    def __init__(self):
        self.unidade = ""
        self.valor = 0

    def coletar(self):
        raise NotImplementedError


class CpuMetrica(Metrica):
    def __init__(self):
        super().__init__()
        self.unidade = "%"

    def coletar(self):
        self.valor = psutil.cpu_percent(interval=1)
        return self.valor


class MemoriaMetrica(Metrica):
    def __init__(self):
        super().__init__()
        self.unidade = "MB"

    def coletar(self):
        self.valor = psutil.virtual_memory().used / (1024 * 1024)
        return self.valor


class DiscoMetrica(Metrica):
    def __init__(self):
        super().__init__()
        self.unidade = "MB"

    def coletar(self):
        self.valor = psutil.disk_usage('/').free / (1024 * 1024)
        return self.valor


metricas = [
    CpuMetrica(),
    MemoriaMetrica(),
    DiscoMetrica()
]

with open("metricas.csv", mode="w", newline="") as arquivo:
    escritor = csv.writer(arquivo)

    escritor.writerow(["datetime", "metrica", "valor", "unidade"])

    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for metrica in metricas:
        metrica.coletar()

        escritor.writerow([
            agora,
            metrica.__class__.__name__.replace("Metrica", ""),
            round(metrica.valor, 2),
            metrica.unidade
        ])

print("Métricas coletadas com sucesso!")