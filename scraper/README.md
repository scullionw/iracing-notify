# iracing-notify

1.  Create env file with credentials

        IRACING_USERNAME=
        IRACING_PASSWORD=

2.  Create secrets resource

        kubectl create secret generic scraper-configuration --from-env-file=.env

3.  Apply deployments

        kubectl apply -f redis-storage.yaml -f database-storage.yaml
        kubectl apply -f redis.yaml -f database.yaml
        kubectl apply -f api.yaml -f ui.yaml -f scraper.yaml
