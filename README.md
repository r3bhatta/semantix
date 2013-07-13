Semantix
========

The Semantix crawler.

Installation
------------

1. Install Python 2.7.3.
2. Install `virtualenv` and make sure it is activated. All Python libraries should be installed 
while `virtualenv` is activated.
3. Install [Flask](http://flask.pocoo.org/docs/installation/ "Flask").
4. Install [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/bs4/doc/ "BeautifulSoup").
5. Install [NLTK](http://nltk.org/install.html "NLTK").

Run
---

1. Run `./start`.
2. You can also run `python app/main.py` to check out the main algorithms without starting flask.

Notes
-----

We activate a virtual environment to ensure our project runs on the enclosed Python version and is 
not affected by the other Python versions installed on the machine. Flask is also installed into 
the virtual environment, and not globally on our machine.

OCR Recognition
---------------

OCR recognition is done using the Tesseract library.

1. `brew install tesseract`  

Usage:  
    `tesseract [image_name] [output_file]`
