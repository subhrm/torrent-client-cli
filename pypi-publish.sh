#! /bin/sh
python3 setup.py sdist 
python3 setup.py bdist_wheel
python3 -m twine upload --repository pypi dist/*
rm -rf dist/*
rm -rf build/*