# I181 — Local energy-interface inventory

## Purpose
Remove one distinct owned-PC blocker without fabricating energy: determine whether the actual local machine exposes a pre-existing cumulative energy-counter interface that could later support genuine before/after readings.

## Added
- `implementation/i181_local_energy_interface_inventory.py`
- `implementation/test_i181_local_energy_interface_inventory.py`

## Behavior
I181 performs only local filesystem/interface inventory. It never reads an energy value, installs software, invokes subprocesses, requests elevation, uses credentials/network/CI, creates I166 evidence, or enables spend/value movement.

Linux support is intentionally conservative:
- `/sys/class/powercap/**/energy_uj` is reported as a cumulative candidate when readable;
- `/sys/class/hwmon/**/energy*_input` is reported as a cumulative candidate when readable;
- hwmon `power*_input` is inventory-only and never promoted as a before/after energy counter;
- battery `energy_now` is inventory-only and never promoted as workload energy because charging/background load/battery behavior confound attribution.

Windows/macOS are kept fail-closed because this inert stdlib-only detector does not have a trustworthy generic cumulative counter path there. It does not shell out to vendor tools or request drivers/privileges.

A detected cumulative interface is still only a candidate. Its domain/scope and wrap semantics must be validated on the actual owned PC before genuine readings may enter I166/I162/I129.

## Exact-local verification
Current Git blobs:
- module: `b1dd8714d805d9ccefcab150889138eeffc94a08`
- tests: `44bb833a063e5fbb4458ec06de8fdf22983474e0`

The exact current Git bytes were materialized locally and their Git blob SHA values matched. Focused tests ran with proxy/network environment disabled:
- **6 passed in 0.05s**

## Current execution-host sanity check
Running I181 on the present execution host returned:
- system: Linux
- state: `NO_SUPPORTED_LOCAL_ENERGY_INTERFACE_FOUND`
- candidates: 0
- energy values read: false
- evidence created: false

This is only a property of the current execution host and is **not** evidence about the user's owned PC.

## Result
I181 is complete. The repository now has an inert, exact-tested preflight to determine whether the real owned PC exposes a plausible cumulative energy-counter candidate.

## Next gate
Run I181 on the actual owned PC before I179. If a cumulative candidate exists, validate its scope/wrap semantics and obtain genuine before/after readings around the bound workload. If no suitable counter exists, keep the energy blocker explicit rather than estimate or synthesize it.
