# iracing-notify

1. Create docker volume

        docker volume create iracing-notify-store

2. Build image

        docker build -t iracing-notify .

3. Configure cron

        */5 * * * * cd ~/iracing-notify && docker run -v iracing-notify-store:/app/data/ iracing-notify