# CPU cores

One folder per ISA family, one subfolder per core. Each core keeps its
upstream LICENSE and a PROVENANCE.md (URL, commit, license, local changes).
Third-party code is vendored unmodified; wrap it instead of editing it.

| Folder | Cores |
|---|---|
| riscv/ | picorv32 (present); candidates: ibex (lowRISC), cv32e40p/cv32e40x (OpenHW), VexRiscv, NEORV32 |
| arm/ | Cortex-M0/M3 (licensed by Arm; not open, add under your own license terms) |
| lm32/ | LatticeMico32 (open, add when needed) |
| other/ | any other ISA |
