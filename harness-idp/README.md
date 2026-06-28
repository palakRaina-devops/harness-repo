# Reproducing `formContext.user.uid` malforming in Harness IDP

This is a minimal Harness IDP **Workflow** catalog entity built to reproduce the
customer report that `formContext.user.uid` "has started malforming."

## What's in here

| File | Purpose |
|------|---------|
| `workflow.yaml` | The Workflow catalog entity. Surfaces `formContext.user.uid` (and mapped email/name) directly in the form, and optionally echoes uid to a live API. |
| `backend-proxy-config.yaml` | Backend proxy pointing at `httpbin.org` (public echo). Only needed for the optional "over the wire" confirmation. |

## How `uid` works (per the docs)

- The dynamic picker / form context feature exposes the logged-in user via
  `formContext.user.<field>`.
- `uid` is provided **by default** (you do not map it), so it's always available
  as `formContext.user.uid`.
- Other fields are explicitly mapped via `spec.userFieldMapping` (here we map
  `userEmail: email` and `name: name`) so we can compare a possibly-malformed
  `uid` against values that are known to be correct.

A healthy `uid` is a Backstage entity reference, e.g. `user:default/john.doe`.
If it's malforming, you'll typically see it truncated, double-prefixed
(`user:default/user:default/...`), URL-encoded, empty, or carrying the raw
internal id instead of the ref.

## Steps to reproduce

1. **Register the workflow.**
   - Edit `workflow.yaml` and replace `owner` with a valid user/group in your
     account (e.g. `user:account/you@company.com`).
   - Push it to a Git repo connected to your Harness IDP account, then register
     it from **IDP → Catalog → Register** (or import via the catalog ingestion
     you normally use). Use the new `harness.io/v1` `Workflow` kind as-is.

2. **Open the workflow and read page 1 ("Inspect formContext.user.uid").**
   - **Full Form Context (DEBUG)** shows the whole `formContext` object —
     inspect the `user` block to see the raw shape of `uid`.
   - **formContext.user.uid** shows the value on its own. This is the field
     under investigation.
   - The mapped **userEmail** / **name** fields let you confirm the session is
     resolving correctly while only `uid` is wrong (which is what the customer
     is describing).

   > Note: per Harness docs, form-context features do **not** work in the
   > Workflow Playground editor — you must run the **registered** workflow.

3. **(Optional) Confirm what's sent over the wire — page 2.**
   - Paste `backend-proxy-config.yaml` into
     **IDP → Configure → Plugins → "Configure Backend Proxies"** and save.
   - Open the workflow, go to the second page, and open browser **DevTools →
     Network**. The `Echo user fields to API` picker calls `proxy/httpbin/get`
     with `uid`, `userEmail`, and `name` appended as query params + headers.
   - The httpbin response (and the request URL in the Network tab) shows the
     exact `uid` string Harness transmitted — this isolates whether the
     malformation happens in the value itself or only in rendering.

## What to capture for the customer answer

- Screenshot of the **Full Form Context** block (the `user` object).
- The value shown in **formContext.user.uid** vs. the correct **userEmail**.
- The httpbin request URL / response showing the transmitted `uid`.

With those three, you can state definitively whether `uid` is malformed at the
source, only in transit, or only in display.
