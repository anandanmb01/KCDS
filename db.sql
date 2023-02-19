CREATE TABLE districts 
    (id INTEGER PRIMARY KEY, 
    name VARCHAR(30));

CREATE TABLE localbodies 
    (
        id INTEGER PRIMARY KEY,
        name VARCHAR(30),
        d_id INTEGER,
        FOREIGN KEY(d_id) REFERENCES districts(id)
    );

CREATE TABLE wards 
    (
        id INTEGER PRIMARY KEY,
        name VARCHAR(30),
        l_id INTEGER,
        FOREIGN KEY(l_id) REFERENCES localbodies(id)
    );

CREATE TABLE polling_stations 
    (
        id INTEGER PRIMARY KEY,
        name VARCHAR(30),
        w_id INTEGER,
        FOREIGN KEY(w_id) REFERENCES wards(id)
    );

CREATE TABLE citizens 
    (
        id INTEGER PRIMARY KEY,
        p_id INTEGER,
        name VARCHAR(30),
        guardian VARCHAR(30),
        house_no VARCHAR(30),
        house_name VARCHAR(30),
        gender VARCHAR(30),
        age VARCHAR(30),
        id_card_no VARCHAR(30),
        FOREIGN KEY(p_id) REFERENCES polling_stations(id)
    );

INSERT INTO districts 
    (name) VALUES
    ("kollam");

INSERT INTO districts (name)
    SELECT 'kollam'
    WHERE NOT EXISTS (SELECT 1 FROM districts WHERE name = "kollam");

INSERT INTO localbodies (name,d_id)
    SELECT 'kundayam',districts.id
    WHERE NOT EXISTS (SELECT * FROM localbodies JOIN districts on districts.id == localbodies.d_id WHERE name = "kundayam" AND districts.name == "kollam");
