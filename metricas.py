import csv
import psutil
import time
import argparse
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


def criar_metricas(nomes):
    metricas = []

    if "cpu" in nomes:
        metricas.append(CpuMetrica())

    if "memoria" in nomes:
        metricas.append(MemoriaMetrica())

    if "disco" in nomes:
        metricas.append(DiscoMetrica())

    return metricas


def salvar_metricas(metricas, arquivo):
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for metrica in metricas:
        metrica.coletar()

        escritor = csv.writer(arquivo)

        escritor.writerow([
            agora,
            metrica.__class__.__name__.replace("Metrica", ""),
            round(metrica.valor, 2),
            metrica.unidade
        ])


def main():
    parser = argparse.ArgumentParser(
        description="Coletor de métricas do sistema"
    )

    parser.add_argument(
        "--metricas",
        nargs="+",
        choices=["cpu", "memoria", "disco"],
        default=["cpu", "memoria", "disco"],
        help="Métricas que serão coletadas"
    )

    parser.add_argument(
        "--intervalo",
        type=int,
        default=5,
        help="Intervalo entre as coletas em segundos"
    )

    parser.add_argument(
        "--iteracoes",
        type=int,
        default=10,
        help="Quantidade de vezes que as métricas serão coletadas"
    )

    parser.add_argument(
        "--saida",
        default="metricas.csv",
        help="Nome do arquivo CSV de saída"
    )

    args = parser.parse_args()

    metricas = criar_metricas(args.metricas)

    with open(args.saida, mode="w", newline="") as arquivo:
        escritor = csv.writer(arquivo)

        escritor.writerow([
            "datetime",
            "metrica",
            "valor",
            "unidade"
        ])

        for i in range(args.iteracoes):
            salvar_metricas(metricas, arquivo)

            print(
                f"Coleta {i + 1}/{args.iteracoes} realizada."
            )

            if i < args.iteracoes - 1:
                time.sleep(args.intervalo)

    print(f"\nMétricas salvas em: {args.saida}")


if __name__ == "__main__":
    main()