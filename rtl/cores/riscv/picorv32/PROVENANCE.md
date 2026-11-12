# PicoRV32 provenance
- Upstream: https://github.com/YosysHQ/picorv32 (maintained by YosysHQ, same group as Yosys)
- Commit: ef203c2b0a3fb793280f5114941416c425c5b461
- License: ISC (see LICENSE)
- Files: picorv32.v (contains modules picorv32, picorv32_axi, picorv32_wb, picorv32_pcpi_*)
- Local modifications: none. Do not edit; wrap it instead.
- ISA: RV32I[M][C], configurable via parameters. Native memory interface;
  picorv32_axi gives AXI4-Lite, picorv32_wb gives Wishbone. APB needs a bridge in rtl/bus.
