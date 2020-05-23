# crucible
Testing facilities for MoodyTunes. This repository will house all the code needed to test the MoodyTunes
application.

## Load Testing

We use [locust](https://locust.io/) for load testing MoodyTunes. This allows us to simulate high
volume traffic against our application.

### Installation

1. Install the Python3 dev package for installing the locust library

`sudo apt-get install python3-dev`

2. Create a virtual environment in the repository directory and activate it

```shell script
virtualenv -p $(which python3) venv
source venv/bin/activate
```

3. Install the requirements

`(venv) pip install -r requirements.txt`
