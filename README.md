# Youmu Bot Rewrite (Rewrite)
**If you're here from my web dev class project, welcome to my Github, where you can find a bunch of the stuff I've made over time**

## Introduction

Youmu Bot was a Discord bot originally created on May 30, 2021 as an experiment with lexers and parsers. 
A while after development stopped on Youmu Bot, I realized the original concept for Youmu Bot was stupid and the code was horrible, so I rewrote the code, focusing on its art searching and code quality.

Around May 30, 2022, I began to rewrite the code yet again to celebrate the 1 year anniversary of Youmu Bot, which was my first large project. And that's what this is.

This rewrite extends upon the philosophy of the original rewrite, but executes it in a way that is more convenient for developers and end users. 
For example, most previously hardcoded configuration is now stored in a `config.json` file, proper logging was added, and the art-searching commands were expanded upon and made easier to use.


## Usage
Prerequisites: 
- Python 3.10, with pip


To run Youmu Bot locally, follow the following instructions after cloning the repository and changing the working directory

- Create a virtual environment
```commandline
python -m venv ./venv
```
- Activate virtual environment (if this doesn't work, see the [official venv docs](https://docs.python.org/3/tutorial/venv.html))
```commandline
source venv/bin/activate
```
- Install dependencies
```commandline
pip install -r requirements.txt
```
- Run the main script
```commandline
python main.py
```

## TODO
- Add documentation for every feature
- Add more character descriptions
- Add more small features
