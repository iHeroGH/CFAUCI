CREATE TABLE IF NOT EXISTS guild_settings(
    guild_id BIGINT PRIMARY KEY,
    prefix TEXT
);
-- A default guild settings table.
-- This is required for VBU and should not be deleted.
-- You can add more columns to this table should you want to add more guild-specific
-- settings.


CREATE TABLE IF NOT EXISTS user_settings(
    user_id BIGINT PRIMARY KEY,
    user_name TEXT,
    duration INT DEFAULT 6,
    last_sent TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    is_sent BOOLEAN DEFAULT True
);

-- A default guild settings table.
-- This is required for VBU and should not be deleted.
-- You can add more columns to this table should you want to add more user-specific
-- settings.
-- This table is not suitable for member-specific settings as there's no
-- guild ID specified.


-- CREATE TABLE IF NOT EXISTS role_list(
--     guild_id BIGINT,
--     role_id BIGINT,
--     key TEXT,
--     value TEXT,
--     PRIMARY KEY (guild_id, role_id, key)
-- );
-- A list of role: value mappings should you need one.
-- This is not required for VBU, so is commented out by default.


-- CREATE TABLE IF NOT EXISTS channel_list(
--     guild_id BIGINT,
--     channel_id BIGINT,
--     key TEXT,
--     value TEXT,
--     PRIMARY KEY (guild_id, channel_id, key)
-- );
-- A list of channel: value mappings should you need one.
-- This is not required for VBU, so is commented out by default.

CREATE TABLE IF NOT EXISTS osat_scores(
    osat INTEGER,
    clean INTEGER,
    taste INTEGER,
    ace INTEGER,
    speed INTEGER,
    accuracy INTEGER,
    nsurvey INTEGER
);

CREATE TABLE IF NOT EXISTS osat_over_time(
    osat_date DATE[],
    osat_score INTEGER[]
);