# dev docs

## Init

### Overall environment

```
docker-compose up -d
```

### traithunter-processing environment

```
# bootstrap conda environment
mamba env create -f processing/environment.yml
conda activate traithunter-processing

# install common_funcs
python -m pip install -e common_funcs

# install yiutils
python -m pip install -e yiutils

# install processing_funcs
python -m pip install -e processing_funcs

# install mypy
python -m mypy --install-types
```

```
# Now using processing as the root
cd processing
# verify state of setup
python -m pytest tests/test_init.py
```

## env vars
