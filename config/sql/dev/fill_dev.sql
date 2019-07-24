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