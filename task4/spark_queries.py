from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


spark = SparkSession \
    .builder \
    .appName("Python Spark SQL") \
    .config("spark.jars", "postgresql-42.2.14.jar") \
    .getOrCreate()

jdbcReader = spark.read.format("jdbc"). \
    options(
    url='jdbc:postgresql://localhost:5432/pagila',  # jdbc:postgresql://<host>:<port>/<database>
    user='postgres',
    password='secret',
    driver='org.postgresql.Driver')


def table_read(table_name):
    return jdbcReader.option("dbtable", table_name).load()


actor = table_read('actor')
address = table_read('address')
category = table_read('category')
city = table_read('city')
country = table_read('country')
customer = table_read('customer')
film = table_read('film')
film_actor = table_read('film_actor')
film_category = table_read('film_category')
inventory = table_read('inventory')
language = table_read('language')
payment = table_read('payment')
rental = table_read('rental')
staff = table_read('staff')
store = table_read('store')

#FirstQuery = category.join(film_category, on="category_id")\
#                        .select(F.col('film_id'), F.col('name'))\
 #                       .groupBy('name')\
 #                       .agg(F.count(F.col('film_id')))\
 #                       .orderBy(F.col('count(film_id)').desc()).show()

#2. Вывести 10 актеров, чьи фильмы большего всего арендовали, отсортировать по убыванию.

# SecondQuery = actor.join(film_actor, on='actor_id')\
#                     .join(inventory, on='film_id')\
#                     .join(rental, on='inventory_id')\
#                     .select(F.col('first_name'), F.col('actor_id'), F.col('last_name'),\
#                             F.col('inventory_id'))\
#                     .groupBy(F.col('first_name'), F.col('last_name'))\
#                     .agg(F.count(F.col('inventory_id')))\
#                     .orderBy(F.col('count(inventory_id)').desc()).show(10)

#Вывести категорию фильмов, на которую потратили больше всего денег.
#
# ThirdQuery = category.join(film_category, on='category_id')\
#                 .join(film, on='film_id')\
#                 .select(F.col('name'), F.col('title'), F.col('replacement_cost'))\
#                 .groupBy(F.col('name'))\
#                 .agg(F.sum(F.col('replacement_cost')))\
#                 .orderBy(F.col(('sum(replacement_cost)')).desc()).show(1)

#4. Вывести названия фильмов, которых нет в inventory.

# FourthQuery = film.join(inventory, 'film_id', 'left')\
#                     .select(F.col('title'))\
#                     .filter(F.col('inventory_id').isNull()).show()

#5.Вывести топ 3 актеров, которые больше всего появлялись в фильмах в категории “Children”.
# Если у нескольких актеров одинаковое кол-во фильмов, вывести всех..

# FifthQuery = film_category.join(category, 'category_id')\
#                             .join(film_actor, 'film_id')\
#                             .join(actor, 'actor_id')\
#                             .groupBy('actor_id', 'name', 'first_name', 'last_name')\
#                             .agg(F.count('film_id').alias('children_films'))\
#                             .filter(F.col('name') == 'Children')\
#                             .select(F.col('first_name'), F.col('last_name'), F.col('children_films'))\
#                             .orderBy(F.col('children_films').desc()).show(5)

#6.Вывести города с количеством активных и неактивных клиентов (активный — customer.active = 1).
# Отсортировать по количеству неактивных клиентов по убыванию.

# Sixth_query = city.join(address, 'city_id')\
#                     .join(customer, 'address_id')\
#                     .groupBy('city')\
#                     .agg(F.sum('active').alias('active_users'), F.count('active').alias('all_users'))\
#                     .select('city', 'active_users', (F.col('all_users') - F.col('active_users')).alias('inactive_users'))\
#                     .orderBy(F.col('inactive_users').desc()).show()

#7. Вывести категорию фильмов, у которой самое большое кол-во часов суммарной аренды в городах
# (customer.address_id в этом city), и которые начинаются на букву “a”.
# Тоже самое сделать для городов в которых есть символ “-”.

# w = Window.partitionBy("city").orderBy(F.desc("sum(rent_time)"))
#
# QuerySeventh = city.filter(F.col("city").like("%-%"))\
#     .join(address, 'city_id')\
#     .join(customer, 'address_id')\
#     .join(rental, 'customer_id')\
#     .where(F.col('rental_date').isNotNull() & F.col('return_date').isNotNull())\
#     .join(inventory, 'inventory_id')\
#     .join(film_category, 'film_id')\
#     .join(film.where(F.col("title").like("a%") | F.col("title").like("A%")), 'film_id')\
#     .join(category, 'category_id' )\
#     .withColumn("rent_time", (F.unix_timestamp('return_date') - F.unix_timestamp("rental_date")))\
#     .select('city', category.name.alias('category'), 'rent_time')\
#     .groupby('city', 'category')\
#     .agg(F.sum(F.col('rent_time')))\
#     .withColumn("row_number", F.row_number().over(w))\
#     .where(F.col('row_number') == 1)\
#     .select('city', 'category')\
#     .sort('city')\
#     .show()


