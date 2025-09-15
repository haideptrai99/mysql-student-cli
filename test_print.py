from mysql_highlight import print_query

print_query("SELECT id, name, email FROM users WHERE active = 1;")
print_query("INSERT INTO orders (id, total) VALUES (1, 100);")
print_query("UPDATE users SET active = 0 WHERE id = 10;")
print_query("DELETE FROM logs WHERE created_at < NOW();")
print_query("CREATE TABLE demo (id INT PRIMARY KEY, name VARCHAR(50));")
print_query("ALTER TABLE demo ADD COLUMN email VARCHAR(100);")
print_query("SELECT (u.id, u.name) FROM users u JOIN orders o ON u.id = o.user_id;")
