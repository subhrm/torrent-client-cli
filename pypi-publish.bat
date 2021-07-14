@echo off
rmdir /S /Q dist
rmdir /S /Q build
python setup.py sdist 
python setup.py bdist_wheel
@REM python -m twine upload --repository pypi dist/*

