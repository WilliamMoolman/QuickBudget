# Starting Postgres
```sh
docker pull postgres
docker run --name postgresdb -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres
diesel setup
```