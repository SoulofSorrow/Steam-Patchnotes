FROM docker.io/library/python:alpine AS base
RUN apk update && apk upgrade


FROM base AS builder

COPY requirements.txt /tmp/
RUN mkdir /build && pip install --prefix=/build -r /tmp/requirements.txt

FROM base AS final
ENV LANG en
ENV PYTHONPATH /app
WORKDIR /app

RUN adduser -D app
COPY --chown=app:app . .
COPY --from=builder /build /usr/local

USER app

ENTRYPOINT ["python", "workshop_changelogs/run.py"]
