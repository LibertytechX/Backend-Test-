## Minimal E-commerce Backend API Development Test Solution

### Setup 

- Install dependencies
```sh
poetry install
```

- Activate poetry venv 
```sh
poetry shell
```
- Set up PSQL Database configuration
```sh
cp .env.sample .env
# update the configuration details inside the .env
```
- Run makemigrations (This is because dev migrations are not being pushed to Github)
```sh
make mms
```

- Run Migrate
```sh
make migrate
```

- Start the application
```sh
make run
```

## Deployment
Currently the application is being deployed to AWS ECS(Elastic Container Service)

- live url at
[live](http://liberty-lb-723786584.eu-north-1.elb.amazonaws.com)

- Visit Postman Documentation
[docs](https://documenter.getpostman.com/view/35174244/2sA3kVjgC9)

- Run Test
```sh
make test
```




