# Official artifact provenance findings

A separate read-only forensic pass traced released and local artifacts through response, initial assembly, temporary repair candidates, and final selected tests.

## Findings

- The inspected local checkout was at commit `fce83f1a4b9aa3f1d54598b62027bc17bb585383` but was already modified, so the commit alone does not identify the local Run3 state.
- In the released official artifacts, 438 of 555 final tests matched a temporary repair candidate byte-for-byte; one more was Java-token equivalent; 62 matched direct initial assembly; 18 fit later overwrite/assembly patterns; 36 remained unmapped.
- The local Run3 chain was internally closed: 106 of 111 final tests matched temporary candidates and 5 matched direct initial assemblies.
- The official aggregate files contain EPR inconsistencies in two repetitions, so exact published EPR provenance remains unresolved. Public comparisons should report denominators and preserve the original summaries.

These findings limit claims about exact historical reproducibility. They do not by themselves explain the lower local score; direct generated/repair quality remains the strongest demonstrated contributor.

