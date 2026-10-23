# gravitational-imaging-teaching-team

How can a glass of water help make gravitational lensing feel less abstract? We use hands-on optics demonstrations to connect the bending of light by ordinary lenses and galaxies, then build toward dark matter, strong-lens substructure, and space-telescope observations. This repository collects our workshop materials as the curriculum takes shape.

Our `paths.py` module reads `GRAVITATIONAL_IMAGING_TEACHING_TEAM_PATH`, which defaults to this checkout. It exposes local `data/` and `visuals/` directories. Git ignores both.

## Notebook Checks

Our push and pull-request workflow executes added or modified notebooks with
nbconvert. Changed paths are passed as JSON data and literal process arguments,
preserving spaces, quotes, and Unicode filenames. A failed notebook stops the
check, and the workflow token has read-only repository and pull-request access.
This workflow does not build or publish the MkDocs site.

With pytest and PyYAML available, run the workflow regression checks from this
repository's root.

```bash
python -m pytest test_workflow.py -q
```

These tests exercise the actual workflow runner with a substituted notebook
process. They verify argument handling and error propagation without executing
the curriculum notebooks or certifying their scientific content.
