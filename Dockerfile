FROM python:3.13-slim

RUN useradd -m -s /bin/bash pfa.manager && mkdir /app

WORKDIR /app

COPY ./web /app/web

RUN chown -R pfa.manager: /app

USER pfa.manager

RUN pip install -r ./web/requirements.txt

EXPOSE 8000

ENTRYPOINT ["/home/pfa.manager/.local/bin/gunicorn"]
CMD ["-w", "4", "-b", "0.0.0.0:8000" , "web:create_app()"]