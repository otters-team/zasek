**Install poetry** \
`curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python` \
\
**Update shell config**\
`source $HOME/.poetry/env`\
\
**Make dirty hack**\
`nano $(which poetry)`\
change `python` to `python3` in first line\
`Ctrl+X` then `Y` and press `Enter`\
\
**Install dependencies and create venv**\
`poetry install`\
\
**Get path to new venv**\
`poetry show -v`