import argparse
from pathlib import Path

from simple_parsing import ArgumentParser

import pandas as pd  # noqa
import janitor  # noqa

from local_utils import data_types  # isort:skip


def make_args() -> argparse.Namespace:
    parser = ArgumentParser()
    parser.add_argument("--input-file", type=str, help="input file")
    parser.add_argument("--output-dir", type=str, help="output directory")
    args = parser.parse_args()
    return args


def prep_data(input_file: Path, output_dir: Path) -> pd.DataFrame:
    raw_df = pd.read_csv(input_file).also(lambda df: print("Raw df: ", df.info()))
    data_types.SourceDf.validate(raw_df)
    df = (
        raw_df[["EFO_ID", "EFO_Term"]]
        .rename(columns={"EFO_ID": "efo_id", "EFO_Term": "efo_term"})
        .assign(efo_term_clean=lambda df: df["efo_term"])
        .also(lambda df: print("Cleaned df: ", df.info()))
    )
    output_path = output_dir / "efo_terms.csv"
    print(f"Write cleaned df to: {output_path}")
    df.to_csv(output_path, index=False)
    return df


def main():
    args = make_args()
    input_file = Path(args.input_file)
    print(f"input_file: {input_file}")
    output_dir = Path(args.output_dir)
    print(f"output_dir {output_dir}")
    output_dir.mkdir(exist_ok=True)
    cleaned_df = prep_data(input_file=input_file, output_dir=output_dir)
    data_types.CleanedDf.validate(cleaned_df)


if __name__ == "__main__":
    main()
