# AWS credits
Start with local TrueForge plus GitHub MCP and Daytona.
Use AWS credits for hosting TrueForge after the end-to-end workflow works.
AWS credits do not automatically cover model-provider APIs or Daytona.

A possible deployment is EC2 running the upstream hosted Docker Compose stack.
Follow https://trueforge.dev/quickstart for its current dependencies and setup.
Use hosted authentication and HTTPS; do not expose unauthenticated local mode.
Choose instance capacity against upstream requirements and measured use.
Check credit eligibility, expiry and account, and set an AWS budget alert first.

No AWS resources have been provisioned. Deployment is a subsequent step requiring
an AWS account/region and a hosting choice. It is not necessary for the local demo.

