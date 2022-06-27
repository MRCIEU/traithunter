from funcs.utils import find_project_root

super_proj_root = find_project_root(anchor_file="docker-compose.yml")
data_root = super_proj_root / "data"
assert data_root.exists(), data_root

analysis_root = find_project_root()
assert analysis_root.exists(), analysis_root

data = {
    "artifacts": data_root / "artifacts",
    "efo": data_root / "efo-v3.43" / "efo.json",
}
data["artifacts"].mkdir(exist_ok=True)

models = {
    "scispacy_lg": super_proj_root / "models" / "en_core_sci_lg-0.5.0" / "en_core_sci_lg" / "en_core_sci_lg-0.5.0"
}
