create TABLE users (
    user_id SERIAL PRIMARY KEY UNIQUE,
    username VARCHAR(250) NOT NULL UNIQUE,
    password VARCHAR(250) NOT NULL
);

CREATE TABLE states(
    state_id SERIAL PRIMARY KEY UNIQUE,
    state_name VARCHAR(250) NOT NULL
);

CREATE TABLE responsible (
    responsible_id SERIAL PRIMARY KEY UNIQUE,
    responsible_name VARCHAR(250) NOT NULL,
    user_id INT NOT NULL,

    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE clients (
    client_id SERIAL PRIMARY KEY UNIQUE,
    client_name VARCHAR(250) NOT NULL,
    phone_number VARCHAR(50) -- optional
);

CREATE TABLE requests (
    request_id SERIAL PRIMARY KEY UNIQUE,  --Number of request
    client_id INT NOT NULL,
    state_id INT,
    responsible_id INT,
    equipment VARCHAR(250), -- equipment that needs to fix
    type_of_fault VARCHAR(250),
    description VARCHAR(250),
    created_at TIMESTAMP default NOW(),

    FOREIGN KEY (client_id) REFERENCES clients(client_id),
    FOREIGN KEY (state_id) REFERENCES states(state_id),
    FOREIGN KEY (responsible_id) REFERENCES responsible(responsible_id)
)
