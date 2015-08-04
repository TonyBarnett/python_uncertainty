from celery import Celery, task

app = Celery("fun", broker='amqp://guest@localhost//')


@app.task
def add(x, y):
    return x + y


if __name__ == '__main__':
    result = add.delay(4, 4)
    # APP.start()
    print(result.get())
