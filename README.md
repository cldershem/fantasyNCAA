# scrapeVegas.py
## Scrapes vegas.com spreads for @barneshere.

### Install
#### get source
```
git clone git@github.com:cldershem/fantasyNCAA.git ~/{SOME_DIR}
cd ~/{SOME_DIR}
```
#### make virtualenv (hopefully you're using virtualenvwrapper and zsh)
```
mkvirtualenv --python=`which python3` fantasyNCAA
echo 'fantasyNCAA' > .venv
deactivate
cd .
```
#### double check your virtualenv is right
```
which python3
>>> ~/{SOME_PATH_TO_VENV}
```
#### install requirements
```
pip3 install -r requirements.txt
```
#### use
```
./scrapeVegas.py
```
