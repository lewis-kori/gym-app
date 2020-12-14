FROM python:3.8

RUN mkdir /code
WORKDIR /code

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

EXPOSE 8070
COPY ./entrypoint.sh /
ENTRYPOINT [ "/entrypoint.sh" ]