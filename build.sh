sudo docker build -t slack_alert .
sudo docker run --name slack_alert -d -p 8000:8000 slack_alert:latest