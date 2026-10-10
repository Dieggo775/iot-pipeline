-- View 1: média de temperatura por dispositivo e local (interno/externo)
CREATE OR REPLACE VIEW avg_temp_por_dispositivo AS
SELECT device_id,
       location,
       ROUND(AVG(temperature), 2) AS avg_temp,
       COUNT(*)                   AS total_leituras
FROM temperature_readings
GROUP BY device_id, location;

-- View 2: volume de leituras por hora do dia
CREATE OR REPLACE VIEW leituras_por_hora AS
SELECT EXTRACT(HOUR FROM noted_at)::int AS hora,
       COUNT(*)                         AS contagem
FROM temperature_readings
GROUP BY 1
ORDER BY 1;

-- View 3: temperaturas máxima, mínima e média por dia
CREATE OR REPLACE VIEW temp_max_min_por_dia AS
SELECT noted_at::date             AS data,
       MAX(temperature)           AS temp_max,
       MIN(temperature)           AS temp_min,
       ROUND(AVG(temperature), 2) AS temp_media
FROM temperature_readings
GROUP BY 1
ORDER BY 1;
