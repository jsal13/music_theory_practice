set shell := ["zsh", "-cu"]

default:
  just --list

install:
  @echo "Installing Lilypond..."
  sudo apt-get install -y lilypond fluidsynth



venv: 
  pip install --upgrade uv
  uv venv \
    && . .venv/bin/activate \
    && uv pip install -r requirements.txt \
    && uv pip install -r requirements-dev.txt

ds:
  . .venv/bin/activate \
    && uv pip install -r requirements-ds.txt

test:
  python -m pytest --doctest-modules ./tests
