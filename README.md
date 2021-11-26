# Link Scanner

It is link scanner for ISP2021.

## Usage

```bash
python3 link_scan.py url_to_scan
```

## Installation

I use Pipenv for virtual environment. If you use pipenv as well, you can use
this following command to install dependencies.

```bash
pipenv install
pipenv shell
python link_scan.py [url_to_scan]
```

For people who use something else, I have `requirements.txt` to use.
You can read instruction from documentation of python virtual environment creator you are using.

For virtualenv
```bash
virtualenv [virtual_env_name]
source [virtual_env_name]/activate
python link_scan.py [url_to_scan]
```

