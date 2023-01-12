# Installation
### Option 1

create a venv 
pip install -r requirements.txt
run elasticsearch.bat
rabbitmqctl start_app

execute in following order: 
python server.py
python client.py
python parser.py
python elasticsearch_api.py
python gui.py

### Option 2
run_pipeline_no_docker.bat

removed the .bat because of gmail restrictions. 


### Option 3
run_pipeline.sh

creates the docker images and containers 
fails to connect to rabbitmq

# USAGE
open browser, go to http://localhost:5001
select an option from the dropdown menu, and type one of three options to see data:
sensor_1, sensor_2, sensor_3

