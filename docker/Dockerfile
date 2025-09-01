FROM fedora:latest

RUN dnf -y update && \
    dnf -y install \
        git \
        make \
        gcc \
        gnucobol \
        python3 \
        python3-pip \
        python3-devel \
        vim \
        less \
        && dnf clean all

WORKDIR /app

RUN if [ -f /app/code/python/requirements.txt ]; then \
    python3 -m pip install --no-cache-dir -r /app/code/python/requirements.txt || true; \
fi

CMD ["/bin/bash"]
