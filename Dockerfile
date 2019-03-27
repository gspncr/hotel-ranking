FROM python:alpine3.7
RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev
ADD app.py /hotel-ranking/
COPY templates /hotel-ranking/templates/
COPY static /hotel-ranking/static/
ENV HS_DB=
ENV twilio_account_SID=
ENV twilio_auth_token=
ADD requirements.txt ./hotel-ranking/
RUN pip install -r ./hotel-ranking/requirements.txt
EXPOSE 8080
WORKDIR /hotel-ranking/
CMD python3 app.py
