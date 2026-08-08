# Frozen Object: Capability Claim

Status: frozen for review

Claim under review:

> The repository executes a live external AI provider during its default test run.

Acceptance requires all of the following contemporaneous evidence:

1. A test invokes the provider through the public integration path.
2. The record identifies the provider, model, invocation time, and non-secret
   request identifier.
3. The test fails when provider access is unavailable or replaced by a fixture.
4. A Reviewer checks the raw execution record without relying on the Producer's
   conclusion.

If any item is absent, the permitted conclusion is `not demonstrated`.

The reviewer may not edit this object. The repository Owner retains acceptance
and publication authority.
