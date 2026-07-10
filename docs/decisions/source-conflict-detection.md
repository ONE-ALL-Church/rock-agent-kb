# Source Conflict Detection

`agent/source-conflicts.jsonl` contains potential contradictions, not every
topic that has both community and higher-authority coverage.

A conflict candidate requires all of the following:

- the same concept and claim type;
- one community claim and one official, source-code, release-note, or
  RockU-confirmed claim;
- meaningful shared topic terms; and
- opposing language about a directive, requirement, capability, availability,
  enablement, or safety property.

Broad authority alignment remains an answer-time policy: prefer the
higher-authority source and treat community material as an implementation
example. It is not a conflict by itself. This distinction prevents large topic
clusters such as workflows, security, check-in, and Lava from appearing as
contradictions merely because the KB has useful sources at multiple tiers.
