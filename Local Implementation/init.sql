DROP SOURCE IF EXISTS user_events CASCADE;
DROP MATERIALIZED VIEW IF EXISTS latest_user_state CASCADE;

CREATE SOURCE user_events (
    id INT,
    name VARCHAR,
    age INT,
    op VARCHAR,
    event_order BIGINT,
    ts TIMESTAMP
)
WITH (
    connector = 'kafka',
    topic = 'user-events',
    properties.bootstrap.server = 'kafka:9092',
    scan.startup.mode = 'earliest'
)
FORMAT PLAIN ENCODE JSON;

-- Materialized view to maintain only the latest active record
CREATE MATERIALIZED VIEW latest_user_state AS
SELECT e.id, e.name, e.age, e.op, e.ts
FROM user_events e
JOIN (
    SELECT id, MAX(event_order) AS latest_order
    FROM user_events
    GROUP BY id
) latest
ON e.id = latest.id AND e.event_order = latest.latest_order
WHERE e.op != 'delete';
