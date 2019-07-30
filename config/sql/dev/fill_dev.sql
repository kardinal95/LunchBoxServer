/* admin user with password admin */
INSERT INTO lunchbox.public.users (name, phone, login, passhash)
 VALUES (NULL, NULL, 'admin', '$5$rounds=535000$6ZAPJ6wjd5wjDfd5$r4CIofx1ff1zj5VgGkBrPNE1mqFoJOCNV5Yw6j0SkF/');
INSERT INTO lunchbox.public.roles (name) VALUES ('superrole');
INSERT INTO lunchbox.public.user_roles (user_id, role_id) VALUES (1, 1);

/* add roles */
INSERT INTO lunchbox.public.roles (name) VALUES ('user manager'), ('product manager'),
                                                ('lunchbox manager'), ('order manager'),
                                                ('client');

/* timeslots */
INSERT INTO lunchbox.public.timeslots (time_start, time_end, capacity) VALUES
('9:00', '9:30', 20), ('9:30', '10:00', 20), ('10:00', '10:30', 20), ('10:30', '11:00', 20),
('11:00', '11:30', 20), ('11:30', '12:00', 20), ('12:00', '12:30', 20), ('12:30', '13:00', 20),
('13:00', '13:30', 20), ('13:30', '14:00', 20), ('14:00', '14:30', 20), ('14:30', '15:00', 20),
('15:00', '15:30', 20), ('15:30', '16:00', 20), ('16:00', '16:30', 20), ('16:30', '17:00', 20),
('17:00', '17:30', 20), ('17:30', '18:00', 20), ('18:00', '18:30', 20), ('18:30', '19:00', 20),
('19:00', '19:30', 20), ('19:30', '20:00', 20), ('20:00', '20:30', 20), ('20:30', '21:00', 20);

/* statuses */
INSERT INTO lunchbox.public.order_statuses (name) VALUES
('создан'), ('задерживается'), ('просрочен'), ('отменен'), ('завершен');

/* add demo */
INSERT INTO lunchbox.public.products (name, description, locked, archived) VALUES
('Суп лапша', NULL, TRUE,  FALSE), ('Салат витаминный', NULL, TRUE,  FALSE),
('Гречневая котлета', NULL, TRUE,  FALSE), ('Тефтели', NULL, TRUE,  FALSE),
('Чай', NULL, TRUE,  FALSE), ('Борщ', NULL, TRUE,  FALSE), ('Салат из капусты с огурцами', NULL, TRUE,  FALSE),
('Картофельное пюре', NULL, TRUE,  FALSE), ('Котлета куриная', NULL, TRUE,  FALSE), ('Компот из сухофруктов', NULL, TRUE,  FALSE),
('Рассольник', NULL, TRUE,  FALSE), ('Салат мозаика', NULL, TRUE,  FALSE), ('Рис', NULL, TRUE,  FALSE),
('Рыбная котлета', NULL, TRUE,  FALSE), ('Тушеная капуста', NULL, TRUE,  FALSE);

INSERT INTO lunchbox.public.lunchboxes (name, price, locked, archived, stock) VALUES
('Ланчбокс 1', 200, TRUE,  FALSE, TRUE), ('Ланчбокс 2', 200, TRUE,  FALSE, TRUE),
('Ланчбокс 3', 300, TRUE,  FALSE, TRUE), ('Ланчбокс 4', 322, TRUE,  FALSE, TRUE);

INSERT INTO lunchbox.public.lunchbox_products (lunchbox_id, product_id) VALUES
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10),
(3, 11), (3, 12), (3, 13), (3, 14), (3, 5), (4, 2), (4, 15), (4, 5);