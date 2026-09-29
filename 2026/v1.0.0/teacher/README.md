# Teacher progress server

This stack is separate from every student stack.

See [registration validation and AWS rollout order](registration-validation.md) for the latest test scope and update sequence.

It creates an API Gateway HTTPS endpoint, one Lambda function, and one DynamoDB table. It does not create a public EC2 instance or open an SSH port.

## Install in the teacher CloudShell

```bash
curl -fsSL \
  https://raw.githubusercontent.com/ShinyaHaga0910/OS-Linux-Control/main/2026/v1.0.0/teacher/install-teacher.sh \
  -o /tmp/jdu-install-teacher.sh
bash /tmp/jdu-install-teacher.sh --region us-east-1
```

Use the AWS region allowed by the Academy Lab. If the Lambda execution role is not named `LabRole`, add `--role-name ROLE_NAME`.

The installer prints the one-line student installation command with the actual deployed endpoint and registration key. Distribute that complete command, not a command copied from an older deployment. Students do not type either value manually. The admin key is never included.

When updating an existing installation, run the teacher installer again against the same stack in the same account and region. This updates Lambda and adds the authenticated `/status` and `/link-email` routes. Update the teacher stack **before** distributing the new student installer. Source publication alone does not update the running AWS stack.

## Open the dashboard

Run this only in the teacher CloudShell:

```bash
jdu-dashboard
```

The command authenticates with the admin key stored in `~/.jdu-teacher/admin.key`. It prints a dashboard URL that expires after 30 minutes. Open that URL in a browser. The admin key remains private. The fixed registration key is only a public course bootstrap value and does not open the dashboard.

The HTTPS endpoint is internet reachable because the browser must reach it. The admin endpoint is protected by a random key kept in the teacher CloudShell. The browser receives only a short-lived session token.

The fixed registration key is public by design. It cannot open the teacher dashboard, but anyone who knows the endpoint and key can create a new anonymous server record. Therefore, use this dashboard for formative progress only, not identity verification or formal grading.

## Data policy

The table stores a random server ID, the student's self-entered Google Classroom email, EC2 instance metadata, the latest guided P1-P6 and challenge M0-M7 scores, and timestamps. P6 and M6 store Ubuntu (2 checks) and CloudShell (4 checks) separately. The dashboard counts each complete only when both parts are complete. It does not store student names. Use `jdu-progress id` on a student server to display its server ID.

The student enters their email once during installation. It is sent over HTTPS with the server token to `/link-email`, after the existing server registration has been read back and the EC2 identity has been checked. The email is not passed to CloudFormation or EC2 and is not printed in installation output. It is cached with mode 0600 in the student's private CloudShell `~/.jdu-student/student-email.txt`, and stored in the teacher's DynamoDB record. Only the authenticated teacher dashboard displays the email; student status responses expose only whether an email is linked. Keep dashboard URLs private. Delete the course progress stack/table and local email caches when no longer needed under the university's record retention policy.

This is **self-declared email linking**, not Google authentication or verification that the student owns the address. Compare emails with your Classroom roster. The same email may appear on several server records after rebuilding; choose the active record using the instance ID and last report. There is no Classroom API integration or automatic grade return. Students no longer need to submit a server ID merely to identify their environment. Existing anonymous records remain compatible and display as unregistered emails until linked.

To correct an email or retry linking after an API problem, the student can run `jdu-register --change-email` or `jdu-register` in the same CloudShell. This does not reset any exercise or alter scores. Initial setup must have registered the server successfully; otherwise diagnose the setup/registration logs first. Do not collect progress.env, server tokens, SSH private keys, or dashboard session URLs as student submissions.

P1-P6 are checked on each student's Ubuntu instance by `jdu-check P1` through `jdu-check P6`; P6 also requires `jdu-check P6` in CloudShell. Each run submits its latest PASS count over HTTPS. The teacher stack receives and displays those results; it does not independently log in to or re-check student instances. The student CloudFormation stack already installs the guided fixtures and check scripts, so no separate teacher-side CloudFormation stack is needed for P1-P6 beyond this progress server.

This is a formative progress view. It is not a tamper-proof examination system because students have administrative access to their own lab server.
