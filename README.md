# Small general scraper

---

**A simple scraper used collecting datas from various different websites**

---

- [How it works](#how-it-works)
- [What can it do](#what-can-it-do)
- [Features](#features)
- [Installation](#installation)
- [Config](#config)


## How it works

1. Get data text from URL
2. Match that desired datas through user-defined XPath or RegEx expression
3. Add datas of matched to total results
4. Write all of results to file

That is all!


## What can it do

used scraping simple datas from various web pages

## Features
- [x] Supported `HTTP`/`SOCKS`proxy
- [x] Supported XPath selector versions: 1.0/2.0/3.0 
- [x] Custom HTTP headers


## Installation

### install dependencies
```bash
pip install -r requirements
```
### run
```bash
python main.py
```


## Config
It works through config file, the config file is `cfg.yml` by default, example config have verbose comments, please see:[example.yml](example.yml)