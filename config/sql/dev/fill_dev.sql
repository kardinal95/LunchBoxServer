/* admin user with password admin */
INSERT INTO lunchbox.public.users (name, phone, login, passhash)
 VALUES (NULL, NULL, 'admin', '$5$rounds=535000$6ZAPJ6wjd5wjDfd5$r4CIofx1ff1zj5VgGkBrPNE1mqFoJOCNV5Yw6j0SkF/');
INSERT INTO lunchbox.public.roles (name) VALUES ('superrole');
INSERT INTO lunchbox.public.user_roles (user_id, role_id) VALUES (1, 1);

/* add roles */
INSERT INTO lunchbox.public.roles (name) VALUES ('user manager'), ('product manager'),
                                                ('lunchbox manager'), ('order manager'),
                                                ('client');

/* add demo */
INSERT INTO lunchbox.public.products (name, description) VALUES
('Картофель фри малый', NULL), ('Картофель фри большой', NULL),
('Гамбургер', 'Сочный и питательный'), ('Чизбургер', 'Как гамбургер но с сыром'),
('Мороженое', NULL), ('Кола 0.5', NULL), ('Кола 1.0', NULL);

INSERT INTO lunchbox.public.lunchboxes (name, price) VALUES
('Дешёвый ланчбокс', 100), ('Средний ланчбокс', 200),
('Дорогой ланчбокс', 300);

INSERT INTO lunchbox.public.lunchbox_products (lunchbox_id, product_id) VALUES
(1, 1), (1, 3), (1, 5), (2, 2), (2, 4), (2, 7), (3, 2), (3, 3), (3, 4), (3, 5), (3, 7);