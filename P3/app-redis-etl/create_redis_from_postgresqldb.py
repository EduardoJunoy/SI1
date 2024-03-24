from sqlalchemy import create_engine, text
import redis
import random

DATABASE_TYPE = 'postgresql'
USERNAME = 'alumnodb'
PASSWORD = 'alumnodb'
HOST = 'localhost'
DATABASE_NAME = 'si1'
PORT = '5432'

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

db_engine = create_engine(
    f'{DATABASE_TYPE}://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}')
redis_engine = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)


def get_spanish_customers():
    with db_engine.connect() as conn:
        customers = conn.execute(text("""
            SELECT c.email, c.firstname, c.lastname, c.phone
            FROM   customers c
            WHERE  c.country = 'Spain' 
        """)).fetchall()
        return [{'email': customer[0], 'firstname': customer[1], 'lastname': customer[2], 'phone': customer[3]} for customer in customers]


def transform_and_insert_data(customers):
    for customer in customers:
        email = customer['email']
        name = customer['firstname'] + " " + customer['lastname']
        phone = customer['phone']
        visits = random.randint(1, 99)

        hash_key = f"customers:{email}"
        customer_data = {
            "name": name,
            "phone": phone,
            "visits": visits
        }

        redis_engine.hset(hash_key, mapping=customer_data)


def increment_by_email(email):
    hash_key = f"customers:{email}"
    redis_engine.hincrby(hash_key, "visits", 1)


def customer_most_visits():
    customer_keys = redis_engine.keys('customers:*')

    max_visits = -1
    customer_max_visits = None

    for key in customer_keys:
        visits = int(redis_engine.hget(key, "visits"))
        if visits > max_visits:
            max_visits = visits
            customer_max_visits = key.decode('utf-8').split(':')[1]

    return customer_max_visits


def get_field_by_email(email):
    hash_key = f"customers:{email}"

    customer_data = redis_engine.hgetall(hash_key)
    decoded_data = {k.decode('utf-8'): v.decode('utf-8')
                    for k, v in customer_data.items()}
    name = decoded_data.get("name", "Not found")
    phone = decoded_data.get("phone", "Not found")
    visits = decoded_data.get("visits", "Not found")
    return {"name": name, "phone": phone, "visits": visits}


def main():
    try:
        transform_and_insert_data(get_spanish_customers())
        increment_by_email('swiss.clamor@potmail.com')
        print(customer_most_visits())
        print(get_field_by_email('swiss.clamor@potmail.com'))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db_engine.dispose()


if __name__ == "__main__":
    main()
