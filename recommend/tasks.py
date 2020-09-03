from backend.celery import app


@app.task(bind=True, autoretry_for=(), retry_backoff=True, max_retries=None)
def execute_recommendation(self):  # pylint: disable=unused-argument
    print("foo")
