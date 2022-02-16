FROM xxx
WORKDIR /usr/robot/sanfierro-slackbot
EXPOSE 80 443
COPY requirements.txt /usr/robot/sanfierro-slackbot
RUN pip3 install -r requirements.txt
COPY . /usr/robot/sanfierro-slackbot
CMD python3 start_bot.py