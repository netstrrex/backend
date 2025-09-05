# backend


### Описание

Тестовое задание в компанию Aiti Guru.
Бекенд написан на python3.13 + fastapi. Работает на gunicorn с uvicorn воркерами. Для простоты в качестве драйвера для БД использовался asyncpg.
Код отформатирован и проверен ruff и mypy. А в качестве пакетного менеджера использовался UV.

### Установка

```bash
$ git clone https://github.com/netstrrex/backend
$ cd backend
$ uv sync
$ pre-commit install
```

### Настройка

Создайте .env файл в корне проекта и заполните его следующими значениями:

| Ключ | Значение                                                                                    |
| --- |---------------------------------------------------------------------------------------------|
| `GUNICORN__HOST` | Хост на котором будет работать gunicorn, по умолчанию укажите 0.0.0.0                       
| `GUNICORN__PORT` | Порт, который будет слушать gunicorn, по умолчанию укажите 8000                             |
| `GUNICORN__WORKERS` | Количество gunicorn воркеров                                                                |
| `POSTGRES__HOST` | Хост на котором работает postgres. Если запускаете через docker compose укажите - postgres. |
| `POSTGRES__PORT` | Порт на котором работает postgres, по умолчанию укажите 5432                                |
| `POSTGRES__DATABASE` | Название базы данных                                                                        |
| `POSTGRES__USER` | Имя пользователя                                                                            |
| `POSTGRES__PASSWORD` | Пароль                                                                                      |
| `POSTGRES_PORT` | Порт на котором будет работать postgres, по умолчанию укажите 5432                          |
| `POSTGRES_DB` | Название базы данных                                                                        |
| `POSTGRES_USER` | Имя пользователя                                                                            |
| `POSTGRES_PASSWORD` | Пароль                                                                                      |

### Запуск

```bash
$ docker compose up -d --build
```

### Даталогическая схема данных

<div align="center">
  <img src="https://sun9-60.userapi.com/s/v1/ig2/2zeKFRqLJ12y3iivckPODdCNHy4gdwkHF1d8vufKmJXdFQrjjKj_dbH1C52yx4e0aRuNdRjEguG6l8-2_g6BZPVm.jpg?quality=95&as=32x36,48x54,72x82,108x123,160x182,240x272,360x409,480x545,540x613,640x726,674x765&from=bu&cs=674x0" width="500">
</div>

Так же она доступна в виде файла с именем backend_db_schema.pgerd в кроне проекта.


### SQL запросы

Пункт 2.1 получение информации о сумме товаров заказанных под каждого клиента 
```sql
SELECT
    c.id,
    c.name AS client_name,
    COALESCE(SUM(oi.quantity * p.price), 0)::NUMERIC(12,2) AS total_amount
FROM clients c
LEFT JOIN orders o
       ON o.client_id = c.id
LEFT JOIN order_items oi
       ON oi.order_id = o.id
LEFT JOIN products p
       ON p.id = oi.product_id
GROUP BY c.id, c.name
ORDER BY total_amount DESC, client_name;
```

Пункт 2.2 нахождение количества дочерних элементов первого уровня вложенности для категорий номенклатуры
```sql
SELECT
    parent.id        AS category_id,
    parent.name      AS category_name,
    COUNT(child.id)  AS direct_children_count
FROM categories parent
LEFT JOIN categories child
       ON child.parent_id = parent.id
GROUP BY parent.id, parent.name
ORDER BY parent.name;
```

Пункт 2.3.1 текст запроса для отчета (view) «Топ-5 самых покупаемых товаров за последний месяц» (по количеству штук в заказах)

```sql
CREATE OR REPLACE VIEW top_5_products_last_month AS
WITH RECURSIVE cat_anc AS (
    SELECT
        c.id,
        c.name,
        c.parent_id,
        c.id   AS top_id,
        c.name AS top_name
    FROM categories c
    WHERE c.parent_id IS NULL

    UNION ALL

    SELECT
        c.id,
        c.name,
        c.parent_id,
        ca.top_id,
        ca.top_name
    FROM categories c
    JOIN cat_anc ca ON c.parent_id = ca.id
),
sales AS (
    SELECT
        oi.product_id,
        SUM(oi.quantity) AS total_qty
    FROM order_items oi
    JOIN orders o ON o.id = oi.order_id
    WHERE o.order_date >= now() - INTERVAL '30 days'
    GROUP BY oi.product_id
)
SELECT
    p.id                        AS product_id,
    p.name                      AS product_name,
    COALESCE(ca.top_name, 'Без категории') AS top_level_category,
    s.total_qty                 AS total_sold_qty
FROM sales s
JOIN products p
  ON p.id = s.product_id
LEFT JOIN cat_anc ca
  ON ca.id = p.category_id
ORDER BY s.total_qty DESC, p.name
LIMIT 5;
```

Пункт 2.3.2 Проанализировать написанный в п. 2.3.1 запрос и структуру БД. Предложить варианты оптимизации этого запроса и общей схемы данных для повышения производительности системы в условиях роста данных.

Создать индексы
```sql
CREATE INDEX IF NOT EXISTS idx_orders_order_date ON orders(order_date);
CREATE INDEX IF NOT EXISTS idx_orders_client_id ON orders(client_id);
CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_order_items_prod ON order_items(product_id);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_categories_parent ON categories(parent_id);
```

Также чтобы не выполнять рекурсивный проход каждый раз:

Можно хранить в products столбец top_category_id и обновлять его триггером при изменении category_id или структуры categories;

Либо использовать расширение ltree, где заранее хранить пары (ancestor_id, descendant_id, depth).