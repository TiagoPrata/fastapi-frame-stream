# fastapi_frame_stream

Package to easily stream individual frames using FastAPI

## To execute the setup

pipenv run python setup.py sdist bdist_wheel

### Upload the package to codebits

```cmd
python -m twine upload dist/*
```

## Testing

### pytest

Run pytests and code coverage using:

```cmd
python -m pytest --cov=avtypes --cov-report=term --cov-report=html
```
