INSERT INTO users (username, password) VALUES
    ('admin', 'admin'),
    ('Елена_Смирнова', 'хэшированный_пароль'),
    ('Алексей_Петров', 'хэшированный_пароль');

INSERT INTO states (state_name) VALUES
    ('в ожидании'),
    ('в работе'),
    ('выполнено');

INSERT INTO responsible (responsible_name, user_id) VALUES
    ('Администратор', 1),
    ('Электрик', 1),
    ('Паяльщик', 1);

INSERT INTO clients(client_name, phone_number) VALUES
    ('Иванов Иван', '+795131351321'),
    ('Маслов Иван', '+795131351321');

INSERT INTO requests(client_id, state_id, responsible_id, equipment, type_of_fault, description) VALUES
    (1, 1, 1, 'процессор', 'замена процессора', 'нужно заменить процессор на более новый'),
    (2, 1, 2, 'материнская плата', 'не работает оперативная память', 'проверить работоспособность материнской платы');
