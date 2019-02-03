FROM python:3.6-slim-jessie as builder

COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt --target /build/

FROM python:3.6-slim-jessie

WORKDIR /srv

COPY --from=builder /build/ ./vendor/
COPY ./offer_search/ ./offer_search/
COPY ./resources/ ./resources/
COPY ./run.py ./run.py

ENV PYTHONPATH=/srv/vendor

CMD ["python", "run.py"]