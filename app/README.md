# Installation

### run_pipeline.sh

creates the docker images and containers

# USAGE
open browser, go to http://127.0.0.1:5001/
select an option from the dropdown menu, and type one of three options to see data:
sensor_1, sensor_2, sensor_3

### Horizontal scaling works. tested command:
docker-compose up --scale client=5 --scale server=3 --scale parser=2

