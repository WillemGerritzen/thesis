FROM python:3.10 as thesis

RUN mkdir /thesis/
WORKDIR /thesis/

COPY ./requirements.txt /thesis/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /thesis/requirements.txt

COPY ./ /thesis/
CMD python3 main.py