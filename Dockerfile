FROM python:3.10



# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install psycopg2 dependencies
RUN apt-get update && apt-get -y install gcc python3-dev musl-dev



# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/usr/local/poetry python -

# Add Poetry to the PATH
ENV PATH="${PATH}:/usr/local/poetry/bin"
WORKDIR /home/app/fruit_shop
COPY . /home/app/fruit_shop
#COPY poetry.lock pyproject.toml /home/app/fruit_shop/
RUN poetry config virtualenvs.create false
RUN poetry install
# copy project



#RUN chmod a+x ./entrypoint.sh
#ENTRYPOINT ["./entrypoint.sh"]