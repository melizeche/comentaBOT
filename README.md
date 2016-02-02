# comentaBOT

Twitter bot made using Markov chains and powered through nonsensical garbage from the comments section of a local newspaper
https://twitter.com/ComentaristaABC

## TODO
- Documentation(scraper, libs and bot)
- Improve the Markov chain algorithm
- Release the dataset(53K of beautiful garbage)

## Requirements

- Python 3
- requests==2.9.1
- tweepy==3.5.0
- APScheduler==3.0.5

## Instructions
```
- git clone
- virtualenv -p python3 env
- source env/bin/activate
- pip install -r requirements.txt
- create config.py (or fill the missing fields in config.py.example and rename it)
- "comentarios.txt" is the default source for the markov chains but you can use any textfile
- python lib_comment.py makedatabase
- python comment_bot.py
```
