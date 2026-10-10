-- Tabela principal com as leituras dos sensores IoT
CREATE TABLE IF NOT EXISTS temperature_readings (
    reading_id   TEXT PRIMARY KEY,
    device_id    TEXT,
    noted_at     TIMESTAMP,
    temperature  INTEGER,
    location     TEXT      -- 'In' (interno) ou 'Out' (externo)
);
