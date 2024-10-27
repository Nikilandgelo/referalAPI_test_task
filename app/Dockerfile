FROM python:3.13-alpine
WORKDIR /app

RUN pip install pip-tools
COPY --from=root requirements.in .
RUN pip-compile && pip-sync

COPY . .

EXPOSE 8000
ENTRYPOINT fastapi run main.py