
import random, json, time, uuid, datetime as dt, faker
fake = faker.Faker()

def gen_txn():
    return {
        "txn_id": str(uuid.uuid4()),
        "ts_utc": dt.datetime.utcnow().isoformat(),
        "merchant": fake.company(),
        "amount": round(random.expovariate(1/75), 2),
        "card_id": fake.credit_card_number()
    }

while True:
    print(json.dumps(gen_txn()))
    time.sleep(0.1)
