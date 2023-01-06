import json
import sys
from pathlib import Path

import ray

_pwd = Path(".").resolve()  # isort:skip
sys.path.append(str(_pwd))  # isort:skip


from common_funcs import utils  # isort:skip
import mvp_funcs  # isort:skip

proj_root = utils.find_project_root("docker-compose.yml")
assert proj_root.exists(), proj_root

data_path = proj_root / "data"

input_path = data_path / "output" / "mvp-mapping-round-2"
assert input_path.exists(), input_path

NUM_WORKERS = 2


def main():
    input_file = input_path / "mvp-encode.json"
    assert input_file.exists(), input_file

    with input_file.open() as f:
        dat_encode = json.load(f)

    print(len(dat_encode))

    if ray.is_initialized():
        ray.shutdown()
    ray.init(num_cpus=NUM_WORKERS)

    mapping_res = ray.get(
        [
            mvp_funcs.get_mapping_remote.remote(idx, total=len(dat_encode), item=_)
            for idx, _ in enumerate(dat_encode)
        ]
    )

    output_file = input_file.parent / "mvp-mapping.json"
    with output_file.open("w") as f:
        json.dump(mapping_res, f)


if __name__ == "__main__":
    main()
