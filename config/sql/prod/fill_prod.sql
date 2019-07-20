/* admin user with password admin */
INSERT INTO lbox_production.public.users (id, name, phone, login, passhash) VALUES (1, NULL, NULL, 'admin', '$5$rounds=535000$6ZAPJ6wjd5wjDfd5$r4CIofx1ff1zj5VgGkBrPNE1mqFoJOCNV5Yw6j0SkF/');
INSERT INTO lbox_production.public.roles (id, name) VALUES (1, 'superrole');
INSERT INTO lbox_production.public.user_roles (id, user_id, role_id) VALUES (1, 1, 1);

/* add roles */
INSERT INTO lunchbox.public.roles (name) VALUES ('user manager'), ('product manager'),
                                                ('lunchbox manager'), ('order manager'),
                                                ('client');