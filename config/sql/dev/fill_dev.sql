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
('0:00', '0:30', 20), ('0:30', '1:00', 20), ('1:00', '1:30', 20), ('1:30', '2:00', 20),
('2:00', '2:30', 20), ('2:30', '3:00', 20), ('3:00', '3:30', 20), ('3:30', '4:00', 20),
('4:00', '4:30', 20), ('4:30', '5:00', 20), ('5:00', '5:30', 20), ('5:30', '6:00', 20),
('6:00', '6:30', 20), ('6:30', '7:00', 20), ('7:00', '7:30', 20), ('7:30', '8:00', 20),
('8:00', '8:30', 20), ('8:30', '9:00', 20), ('9:00', '9:30', 20), ('9:30', '10:00', 20),
('10:00', '10:30', 20), ('10:30', '11:00', 20), ('11:00', '11:30', 20), ('11:30', '12:00', 20),
('12:00', '12:30', 20), ('12:30', '13:00', 20), ('13:00', '13:30', 20), ('13:30', '14:00', 20),
('14:00', '14:30', 20), ('14:30', '15:00', 20), ('15:00', '15:30', 20), ('15:30', '16:00', 20),
('16:00', '16:30', 20), ('16:30', '17:00', 20), ('17:00', '17:30', 20), ('17:30', '18:00', 20),
('18:00', '18:30', 20), ('18:30', '19:00', 20), ('19:00', '19:30', 20), ('19:30', '20:00', 20),
('20:00', '20:30', 20), ('20:30', '21:00', 20), ('21:00', '21:30', 20), ('21:30', '22:00', 20),
('22:00', '22:30', 20), ('22:30', '23:00', 20), ('23:00', '23:30', 20), ('23:30', '23:59', 20);

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

/* add client */
INSERT INTO lunchbox.public.users (name, phone, login, passhash) VALUES
(NULL, NULL, 'client', '$5$rounds=535000$Gn9hSqaTjm4Tk0/O$umXkcrrfhJb7qPglkjmE3rRZ0X3kXfjFRf3wg.8kABD');

INSERT INTO lunchbox.public.user_roles (user_id, role_id) VALUES
(2, 6);

INSERT INTO lunchbox.public.orders (client_id, status_id, created_at, timeslot_id) VALUES
(2, 3, '2019-07-21 13:23:12', 5), (2, 3, '2019-07-25 13:23:12', 14), (2, 2, '2019-08-01 9:33:16', 16);

INSERT INTO lunchbox.public.order_items (order_id, lunchbox_id, quantity) VALUES
(1, 1, 1), (2, 2, 1), (3, 2, 1);