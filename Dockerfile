FROM python:3.12

WORKDIR /app

COPY requirements.txt setup.py ./

# COPY staking_deposit ./staking_deposit
COPY . .

RUN apt-get update && apt-get install -y gcc jq

RUN pip3 install --no-cache-dir -r requirements.txt && \
  python3 setup.py install && \
  chmod +x deposit.sh

RUN ["./deposit.sh", "install"]

ARG cli_command

ENTRYPOINT [ "python3", "generate_deposit_files.py" ]

CMD [ $cli_command ]
