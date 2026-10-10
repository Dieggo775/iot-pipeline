"""Lê o CSV do Kaggle, trata os dados e carrega no PostgreSQL."""
from pathlib import Path
import pandas as pd
from db import get_engine

BASE = Path(__file__).resolve().parent.parent
CSV_PATH = BASE / "data" / "IOT-temp.csv"


def extract() -> pd.DataFrame:
    print(f"Lendo {CSV_PATH} ...")
    return pd.read_csv(CSV_PATH)


def transform(df: pd.DataFrame) -> pd.DataFrame:
    # Padroniza nomes de colunas
    df = df.rename(columns={
        "id": "reading_id",
        "room_id/id": "device_id",
        "noted_date": "noted_at",
        "temp": "temperature",
        "out/in": "location",
    })
    # Converte data (formato dd-mm-aaaa HH:MM)
    df["noted_at"] = pd.to_datetime(df["noted_at"], format="%d-%m-%Y %H:%M")
    # Remove duplicados e nulos
    df = df.drop_duplicates(subset="reading_id").dropna()
    print(f"{len(df)} linhas após limpeza.")
    return df


def load(df: pd.DataFrame) -> None:
    engine = get_engine()
    # Cria a tabela e limpa os dados (permite rodar o script várias vezes)
    with engine.begin() as conn:
        conn.exec_driver_sql((BASE / "sql" / "schema.sql").read_text())
        conn.exec_driver_sql("TRUNCATE TABLE temperature_readings;")
    df.to_sql("temperature_readings", engine, if_exists="append",
              index=False, chunksize=5000, method="multi")
    # Cria as views
    with engine.begin() as conn:
        conn.exec_driver_sql((BASE / "sql" / "views.sql").read_text())
    print("Dados carregados e views criadas com sucesso.")


if __name__ == "__main__":
    load(transform(extract()))
