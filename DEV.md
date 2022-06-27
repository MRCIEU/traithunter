# dev docs

## Init

### Overall environment

```
docker-compose up -d
```

### analysis environment

```
cd analysis
conda env create -f environment.yml
conda activate phenotype-mapping
python -m pip install -e .
python -m mypy --install-types
```

```
# verify state of setup
python -m pytest tests/test_init.py
```

## env vars
