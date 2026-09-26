# Submission draft
Use this description after verifying the live workflow.

Theme: Agents That Act
Problem statement: Ticket Resolver
Project title: PatchPilot - AI Bug Repair with Human Approval

PatchPilot helps developers turn a reproducible bug into a validated repair.
Built on TrueForge, it connects to a GitHub repository, reproduces failing tests
in an isolated sandbox, and generates one minimal patch. It reruns targeted and
regression tests, then presents the root cause, exact diff, before-and-after test
evidence, risk and confidence. Before changing GitHub, it pauses for explicit
human approval. After approval, gated tools create a branch, commit the validated
patch and open a draft pull request. It never merges automatically.
Our demo uses a deliberately seeded Python arithmetic bug; repository access,
test execution and PR creation must be real. The MVP supports one small public
Python repository and one candidate fix.

GitHub: https://github.com/Charan788/patchpilot
Repository created publicly; verify the uploaded project before submitting.

AI assistants: OpenAI ChatGPT/Codex helped with planning, implementation, tests,
agent instructions and documentation. Add other tools only if actually used.

Video: PENDING. Upload a 1080p MP4 of at most 3:00 with narration or captions,
including at least 30 seconds showing TrueForge. Enable public viewing.


