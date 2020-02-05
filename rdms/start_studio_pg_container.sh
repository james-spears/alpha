docker run --rm  --name alpha-pg -e POSTGRES_PASSWORD=docker -d -p 5433:5432 -v $HOME/docker/volumes/alpha/postgres:/var/lib/postgresql/data  postgres
