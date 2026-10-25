# gravitational-imaging-teaching-team

How can a glass of water help make gravitational lensing feel less abstract? We use hands-on optics demonstrations to connect the bending of light by ordinary lenses and galaxies, then build toward dark matter, strong-lens substructure, and space-telescope observations. We keep our workshop materials here as the curriculum takes shape.

Our `paths.py` module reads `GRAVITATIONAL_IMAGING_TEACHING_TEAM_PATH`, which defaults to this checkout. It exposes local `data/` and `visuals/` directories. Git ignores both.

Create the workshop environment from `environment.yml` before running the notebook. It pins a published TDpy revision containing the verbosity helper for quiet, relative file-operation messages.

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

## Notebook activity

In the [point-mass lensing activity](examples/point_mass_lensing_activity.ipynb), we explore how one source produces two images and how magnification changes with alignment. The notebook uses an explicitly synthetic point-mass lens in Einstein-angle units and saves its figure under the ignored `examples/visuals/` directory.
