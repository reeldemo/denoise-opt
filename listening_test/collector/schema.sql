-- Minimal PostgreSQL schema for the HIT collector. Written for Julian's review; nothing has been deployed.
-- GDPR notes: do not log client IP addresses or user agents at the web server or reverse proxy for this endpoint.
-- Prolific IDs live only in `participant`; after payment is approved run:  UPDATE participant SET prolific_pid = NULL, pid_code = <random>;
CREATE TABLE participant (
  participant_id  BIGSERIAL PRIMARY KEY,
  pid_code        TEXT NOT NULL DEFAULT encode(gen_random_bytes(8), 'hex'),  -- random code, safe to publish
  prolific_pid    TEXT UNIQUE,                                                 -- set NULL after payment (retention rule)
  stage           TEXT NOT NULL CHECK (stage IN ('screener','main')),
  study_id        TEXT,
  started_at      TIMESTAMPTZ,
  finished_at     TIMESTAMPTZ,
  sample_rate_hz  INTEGER,
  headphone_correct SMALLINT,
  headphone_passed  BOOLEAN,
  device          TEXT, room TEXT, hearing TEXT, experience_years SMALLINT,
  comment         TEXT                         -- review, delete if it contains personal data, never publish
);
CREATE TABLE answer (
  answer_id      BIGSERIAL PRIMARY KEY,
  participant_id BIGINT NOT NULL REFERENCES participant ON DELETE CASCADE,
  session_index  SMALLINT,
  item_type      TEXT NOT NULL CHECK (item_type IN ('train','dcr','gold','trap','ab')),
  tile           TEXT, system TEXT,
  rating         SMALLINT CHECK (rating BETWEEN 1 AND 5),
  expected       SMALLINT,
  first_system   TEXT, second_system TEXT,
  choice         TEXT CHECK (choice IN ('first','second','none')),
  plays          SMALLINT, rt_ms INTEGER
);
CREATE INDEX answer_participant_idx ON answer(participant_id);
-- Export for scripts/analyze_ratings.py:  columns listener(=pid_code),session,type,tile,system,rating,expected,first,second,choice.
