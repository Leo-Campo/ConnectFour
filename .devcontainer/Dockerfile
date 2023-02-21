FROM python:3.9 as builder

ENV PATH="/opt/venv/bin:$PATH" \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    LANG=C.UTF-8 

# target development requirements
COPY ./.devcontainer/requirements.txt /tmp/requirements.txt 
# add pip-tools
RUN python -m venv /opt/venv \
    && python3 -m pip install -U --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org setuptools wheel pip-tools pip install \
    && python3 -m pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r /tmp/requirements.txt


# Not slim image for development
FROM python:3.9

ARG USERNAME=user
ARG USER_UID=1000
ARG USER_GID=$USER_UID

ENV TZ=Europe/Rome \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH=/home/$USERNAME/crma-to-akeron

COPY --from=builder /opt/venv /opt/venv

# add shell to user
# and allow installing packages in local venv
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive \
    apt-get install -y --no-install-recommends tzdata curl libcurl4 \
    && apt-get clean autoclean \
    && rm -rf /var/lib/apt/lists/{apt,dpkg,cache,log} \
    && ln -snf /usr/share/zoneinfo/${TZ} /etc/localtime \
    && echo ${TZ} > /etc/timezone \
    && addgroup --system --gid $USER_GID $USERNAME \
    && adduser --system --uid $USER_UID --gid $USER_GID --home /home/$USERNAME --shell /bin/bash $USERNAME \
    && chown -R $USERNAME:$USERNAME /opt/venv

USER $USERNAME
WORKDIR /home/$USERNAME

CMD ["python", "-m", "app"]

COPY --chown=user ./app/ ./app/
