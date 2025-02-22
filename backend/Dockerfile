FROM python:3.13

# Configuration
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    APP_DIR=/code \
    USER_DIR=/home/user \
    PATH=/home/user/.poetry/bin:$PATH

RUN apt-get update && apt-get install openssh-client git libpq-dev uuid-runtime libgirepository1.0-dev -y && \
    pip install --upgrade pip && \
    python -m pip install -q poetry

# Create dev user
RUN addgroup --system user --gid 1000 && \
    adduser --system user --ingroup user --uid 1000 --home $USER_DIR && \
    mkdir -p $USER_DIR && chown user:user $USER_DIR && chmod 777 $USER_DIR

# # Create src dir
RUN mkdir -p $APP_DIR && \
    chown user:user $APP_DIR && \
    chmod 777 -R $APP_DIR
WORKDIR $APP_DIR

USER user
RUN cd $USER_DIR && echo "source /code/env/profile" >> $USER_DIR/.bashrc

# install app
COPY --chown=user:user code/ $APP_DIR
RUN poetry install

ENTRYPOINT ["/code/entrypoint"]
CMD ["webapi"]

# Now set it as an env var
ARG BRANCH=""
ARG COMMIT="dev"
LABEL branch=${BRANCH}
LABEL commit=${COMMIT}
ENV COMMIT_SHA=${COMMIT}
ENV COMMIT_BRANCH=${BRANCH}

EXPOSE 80
