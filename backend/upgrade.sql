CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> 8a1fba5148ea

CREATE TABLE dictmap (
    id INTEGER NOT NULL, 
    name VARCHAR(255) NOT NULL, 
    code VARCHAR(255) NOT NULL, 
    status INTEGER NOT NULL, 
    remark VARCHAR(255), 
    create_time DATETIME NOT NULL, 
    update_time DATETIME NOT NULL, 
    is_deleted INTEGER NOT NULL, 
    PRIMARY KEY (id), 
    UNIQUE (code)
);

CREATE TABLE dictmapitem (
    id INTEGER NOT NULL, 
    dict_id INTEGER, 
    label VARCHAR(255) NOT NULL, 
    value VARCHAR(255) NOT NULL, 
    status INTEGER NOT NULL, 
    sort INTEGER NOT NULL, 
    remark VARCHAR(255), 
    create_time DATETIME NOT NULL, 
    update_time DATETIME NOT NULL, 
    PRIMARY KEY (id)
);

CREATE INDEX ix_dictmapitem_dict_id ON dictmapitem (dict_id);

CREATE TABLE groupperms (
    id INTEGER NOT NULL, 
    name VARCHAR(50) NOT NULL, 
    code VARCHAR(50) NOT NULL, 
    sort INTEGER NOT NULL, 
    status INTEGER NOT NULL, 
    permissions VARCHAR(10240) NOT NULL, 
    create_time DATETIME NOT NULL, 
    PRIMARY KEY (id)
);

CREATE TABLE logfreq (
    id INTEGER NOT NULL, 
    module VARCHAR(255) NOT NULL, 
    log_time INTEGER NOT NULL, 
    times INTEGER NOT NULL, 
    create_time DATETIME NOT NULL, 
    PRIMARY KEY (id), 
    UNIQUE (module, log_time)
);

CREATE TABLE logsread (
    id INTEGER NOT NULL, 
    store VARCHAR(255) NOT NULL, 
    name VARCHAR(255) NOT NULL, 
    project VARCHAR NOT NULL, 
    status INTEGER NOT NULL, 
    sort INTEGER NOT NULL, 
    table_name VARCHAR(255), 
    table_ext VARCHAR(255), 
    create_time DATETIME NOT NULL, 
    connect_url VARCHAR(255) NOT NULL, 
    PRIMARY KEY (id)
);

CREATE TABLE logsstore (
    id INTEGER NOT NULL, 
    store VARCHAR(255) NOT NULL, 
    name VARCHAR(255) NOT NULL, 
    project VARCHAR NOT NULL, 
    status INTEGER NOT NULL, 
    sort INTEGER NOT NULL, 
    table_name VARCHAR(255), 
    table_ext VARCHAR(255), 
    create_time DATETIME NOT NULL, 
    connect_url VARCHAR(255) NOT NULL, 
    PRIMARY KEY (id)
);

CREATE TABLE menus (
    id INTEGER NOT NULL, 
    belong VARCHAR(20) NOT NULL, 
    type VARCHAR(20) NOT NULL, 
    name VARCHAR(255) NOT NULL, 
    icon VARCHAR(255), 
    params VARCHAR(1024), 
    component VARCHAR(1024), 
    pid INTEGER NOT NULL, 
    path VARCHAR(1024) NOT NULL, 
    redirect VARCHAR(1024), 
    sort INTEGER, 
    status INTEGER NOT NULL, 
    groups VARCHAR(4096) NOT NULL, 
    create_time DATETIME NOT NULL, 
    PRIMARY KEY (id)
);

CREATE TABLE perms (
    id INTEGER NOT NULL, 
    pid INTEGER NOT NULL, 
    name VARCHAR(50) NOT NULL, 
    route VARCHAR(255) NOT NULL, 
    codename VARCHAR(50) NOT NULL, 
    status INTEGER NOT NULL, 
    sort INTEGER NOT NULL, 
    create_time DATETIME NOT NULL, 
    PRIMARY KEY (id)
);

CREATE INDEX ix_perms_pid ON perms (pid);

CREATE TABLE sysconfig (
    id INTEGER NOT NULL, 
    name VARCHAR(255) NOT NULL, 
    "key" VARCHAR(255) NOT NULL, 
    value VARCHAR(255) NOT NULL, 
    status INTEGER NOT NULL, 
    sort INTEGER NOT NULL, 
    remark VARCHAR(255), 
    create_time DATETIME NOT NULL, 
    update_time DATETIME NOT NULL, 
    is_deleted INTEGER NOT NULL, 
    PRIMARY KEY (id), 
    UNIQUE ("key"), 
    UNIQUE (value)
);

CREATE TABLE syslog (
    id INTEGER NOT NULL, 
    module VARCHAR(20) NOT NULL, 
    content VARCHAR(10240) NOT NULL, 
    request_uri VARCHAR(255) NOT NULL, 
    ip VARCHAR(255), 
    province VARCHAR(255), 
    city VARCHAR(255), 
    execution_time INTEGER, 
    browser VARCHAR(255), 
    browser_version VARCHAR(255), 
    os VARCHAR(255), 
    create_by INTEGER, 
    create_time DATETIME NOT NULL, 
    PRIMARY KEY (id)
);

CREATE TABLE user (
    email VARCHAR(255), 
    username VARCHAR(255) NOT NULL, 
    nickname VARCHAR(255), 
    status INTEGER NOT NULL, 
    is_superuser BOOLEAN NOT NULL, 
    gender INTEGER, 
    user_type VARCHAR(15) NOT NULL, 
    avatar VARCHAR(255), 
    mobile VARCHAR(15), 
    create_time DATETIME NOT NULL, 
    create_by INTEGER, 
    update_time DATETIME NOT NULL, 
    update_by INTEGER, 
    is_deleted INTEGER NOT NULL, 
    group_pem INTEGER, 
    id INTEGER NOT NULL, 
    real_name VARCHAR(255), 
    hashed_password VARCHAR NOT NULL, 
    PRIMARY KEY (id), 
    UNIQUE (mobile), 
    UNIQUE (username)
);

CREATE INDEX ix_user_email ON user (email);

INSERT INTO alembic_version (version_num) VALUES ('8a1fba5148ea') RETURNING version_num;

