FROM python:3.11-slim

RUN useradd -m -s /bin/bash sandbox_user

RUN pip install --no-cache-dir \
    numpy \
    pandas \
    matplotlib \
    requests \
    beautifulsoup4 \
    jupyter 

USER sandbox_user

WORKDIR /home/sandbox_user/app

RUN mkdir -p input output data

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

CMD ["python3"]