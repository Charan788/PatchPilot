# PatchPilot
AI bug repair with human approval, built on TrueForge.

Status: local implementation prepared. Live model, GitHub, Daytona, rejection,
PR creation and three-minute timing must still be verified.

## Architecture
Developer -> TrueForge agent -> GitHub MCP reads -> Daytona sandbox ->
failing test -> model-generated app.py patch -> regression tests -> evidence/diff ->
human approval -> gated GitHub branch, commit and draft PR.
TrueForge provides the UI and agent runtime; no separate frontend is required.

## Run local checks
Python 3.10+:
```sh
python -m pip install -r requirements.txt
python -m pytest -q
```
Five failing tests and one passing application test are intentional before repair.
Offline fixture and configuration checks (standard library only):
```sh
python scripts/verify_fixture.py
python -m unittest discover -s verification -v
```
The fixture verifier applies a hardcoded reference fix in a temporary copy only.
It verifies the demo fixture, not AI repair or sandbox integration.

## TrueForge setup
1. Start TrueForge using npx @truefoundry/trueforge. Record the version for the demo.
2. Settings -> Models: configure the organizer endpoint and valid API key.
   Resolve the earlier 401 Invalid token and test a simple chat first.
3. Settings -> Connectors: authenticate GitHub with access restricted to
   Charan788/patchpilot, allowing repository contents and pull-request writes.
4. Settings -> Sandbox providers: configure Daytona, including sandbox access and
   snapshot-create permission. AWS credits do not cover Daytona automatically.
5. Verify the connector exposes get_file_contents, list_commits, get_commit,
   list_branches, create_branch, push_files and create_pull_request.
   If your gateway renames tools, update BOTH tool lists in scripts/configure_agent.py.
6. Use the exact model name registered in Settings:
```sh
python scripts/configure_agent.py --model "YOUR_REGISTERED_MODEL_NAME"
python scripts/configure_agent.py --model "YOUR_REGISTERED_MODEL_NAME" --connector github --apply
```
The first command prints config; --apply creates an agent on localhost:8790.
Existing agents are not overwritten. Credentials remain in TrueForge Settings.
Alternatively paste agent/instructions.md into Build Agent; attach only the seven
listed tools; enable sandbox; disable subagents; enable approval shields on
create_branch, push_files and create_pull_request.
7. Inspect the saved agent Overview and verify all three write-tool shields.
8. Start a chat with the saved agent:
"Find why tests fail in Charan788/patchpilot. Prepare a safe fix, show test evidence
and the exact diff, then stop before any GitHub write."

## Repository
Public project: https://github.com/Charan788/PatchPilot
Clone this repository and follow the setup steps above.

## Acceptance rehearsal
Reject the first proposed publication: verify no remote branch, commit or PR.
On a second run, approve the preview and each runtime write checkpoint.
Verify the draft PR contains only the tested app.py change.
A denial after an earlier approved write can leave a branch or commit; report it.
Do not merge into main before recording. Measure actual end-to-end time.
Three minutes is a demo target, not an established execution benchmark.

## Limits
One public Python repository, one candidate, one app.py patch, no automatic merge.
Repository restrictions in the prompt must be backed by scoped GitHub credentials.
Writes are not atomic across branch, commit and PR. Approval is enforced by
TrueForge, not by prompt text alone. Live setup is necessary to verify enforcement.

## Submission
See docs/submission.md and docs/demo.md. MIT license.
AI assistance: OpenAI ChatGPT/Codex for planning, code, tests and documentation.
Official references:
https://trueforge.dev/create-agent/overview
https://trueforge.dev/mcp-servers
https://trueforge.dev/sandbox


Run python scripts/verify_fixture.py --pytest to verify the fixture with pytest after installing requirements. agent/patchpilot.json is a ready payload using the model name observed in your local TrueForge; registration still requires a configured GitHub connector and sandbox.

