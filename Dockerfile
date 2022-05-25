FROM ghcr.io/praekeltfoundation/python-base-nw:3.10 as build

RUN apt-get-install.sh g++ libpq-dev
RUN pip install poetry
COPY . ./
RUN poetry config virtualenvs.in-project true \
    && poetry install --no-dev --no-ansi


FROM ghcr.io/praekeltfoundation/python-base-nw:3.10
RUN apt-get-install.sh libpq-dev
COPY --from=build .venv/ .venv/
COPY . ./

CMD ["/.venv/bin/postgresql_sync"]
