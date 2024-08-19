from analysis_funcs.paths import data_root
from analysis_funcs.settings import es_url

DATA_DIR_HPO = data_root / "source" / "hpo-2024-08"
DATA_DIR_UKBB = data_root / "source" / "ukbiobank-2024-08"
assert DATA_DIR_HPO.exists(), print(DATA_DIR_HPO)
assert DATA_DIR_UKBB.exists(), print(DATA_DIR_UKBB)

def main():
    pass


if __name__ == "__main__":
    main()
