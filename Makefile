install:
	find . -name "*.pyc" -exec rm -f {} \;
	pip uninstall -y t2to3
	python setup.py install

clean:
	find . -name "*.pyc" -exec rm -f {} \;
	pip uninstall -y t2to3

.PHONY: install clean