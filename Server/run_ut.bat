@echo off
set PYTHONPATH=%PYTHONPATH%;%cd%\src

pushd ut
pytest -v --debug --log-level=DEBUG