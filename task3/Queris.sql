--1.Вывести количество фильмов в каждой категории, отсортировать по убыванию.
SELECT COUNT(film_id)
FROM film_category
GROUP BY (category_id)
ORDER BY COUNT(film_id) DESC

--2.Вывести 10 актеров, чьи фильмы большего всего арендовали, отсортировать по убыванию.
SELECT first_name, last_name, COUNT(*)
FRON rental JOIN inventory ON rental.inventory_id = inventory.inventory_id
JOIN film ON inventory.film_id = film.film_id
JOIN film_actor ON film.film_id = film_actor.film_id
JOIN actor ON film_actor.actor_id = actor.actor_id
GROUP BY first_name, last_name
ORDER BY COUNT(*) DESC
LIMIT 10

--3. Вывести категорию фильмов, на которую потратили больше всего денег.
SELECT name, sum(replacement_cost)
FROM film JOIN film_category ON film.film_id = film_category.film_id
JOIN category ON film_category.category_id = category.category_id
GROUP BY name
ORDER BY sum(replacement_cost) DESC
LIMIT 1

-- Вывести названия фильмов, которых нет в inventory. Написать запрос без использования оператора IN.
SELECT title
FROM film
LEFT JOIN inventory ON inventory.film_id  = film.film_id
WHERE inventory.film_id IS NULL

-- Вывести топ 3 актеров, которые больше всего появлялись в фильмах в категории “Children”.
--  Если у нескольких актеров одинаковое кол-во фильмов, вывести всех.
SELECT first_name, last_name, count(film_category.category_id )
FROM actor
JOIN film_actor ON film_actor.actor_id = actor.actor_id
JOIN film_category ON film_category.film_id = film_actor.film_id
JOIN category ON category.category_id = film_category.category_id
WHERE category.name = 'Children'
GROUP BY actor.actor_id
ORDER BY  count(film_category.category_id ) DESC
LIMIT 6

--6 Вывести города с количеством активных и неактивных клиентов (активный — customer.active = 1).
-- Отсортировать по количеству неактивных клиентов по убыванию.
SELECT city.city , count(customer.active) FILTER (WHERE active = 1) as active,
		count(customer.active) FILTER (WHERE active = 0) as notactive
FROM address
JOIN customer ON address.address_id = customer.address_id
JOIN city ON address.city_id = city.city_id
GROUP BY city.city
ORDER BY notactive desc

-- 7.Вывести категорию фильмов, у которой самое большое кол-во часов суммарной аренды в
-- городах (customer.address_id в этом city), и которые начинаются на букву “a”. То же самое сделать для городов в которых
-- есть символ “-”. Написать все в одном запросе.

WITH ACM AS (select ((return_date-rental_date)/3600) as rent, title, city, name
FROM category
    JOIN film_category ON category.category_id = film_category.category_id
    JOIN film ON film_category.film_id = film.film_id
    JOIN inventory on film.film_id = inventory.film_id
    JOIN rental ON inventory.inventory_id = rental.inventory_id
    JOIN customer ON rental.customer_id = customer.customer_id
    JOIN address ON customer.address_id = address.address_id
    JOIN city ON address.city_id = city.city_id
)
(SELECT SUM(rent) AS sum_rent,
		name FROM acm
		WHERE  title LIKE 'A%'
GROUP BY name
ORDER BY sum_rent DESC
limit 1)

UNION

(SELECT SUM(rent) AS sum_rent,
		name FROM acm
        WHERE city LIKE '%-%'
GROUP BY name
ORDER BY sum_rent DESC
limit 1);

