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

## Semester registration key

The registration key is private to the enrolled course. It is generated randomly on first installation, saved with mode 0600 in `~/.jdu-teacher/registration.key`, and reused by ordinary updates. The retired public key is detected by fingerprint and replaced automatically. AWS stores only its hash for checking new registrations. Actual keys never belong in this public repository.

At the start of each semester, use the same existing stack and add `--rotate-registration-key`:

```bash
bash /tmp/jdu-install-teacher.sh --region us-east-1 --rotate-registration-key
```

After successful deployment, copy the newly printed one-line setup command, also saved privately in `~/.jdu-teacher/student-setup-command.txt`, into the enrolled Google Classroom course only. Do not publish that file, logs containing the command, screenshots or setup commands on GitHub. A failed deployment retains the old key file and a private pending key for retry. Rotation preserves the admin key, DynamoDB records and existing server tokens. Previously registered students can still submit and view progress; only new registrations using the old semester key are rejected. Students using an old setup command must obtain the current course command. Anyone receiving the course key can register; this is course distribution control, not verification of student identity.

When updating an existing installation, run the teacher installer again against the same stack in the same account and region. This updates Lambda and adds the authenticated `/status` and `/link-email` routes. Update the teacher stack **before** distributing the new student installer. Source publication alone does not update the running AWS stack.

## Open the dashboard

Run this only in the teacher CloudShell:

```bash
jdu-dashboard
```

The command authenticates with the admin key stored in `~/.jdu-teacher/admin.key`. It prints a dashboard URL that expires after 30 minutes. Open that URL in a browser. The admin key remains private. The semester registration key only authorizes server registration and cannot open the dashboard.

The HTTPS endpoint is internet reachable because the browser must reach it. The admin endpoint is protected by a random key kept in the teacher CloudShell. The browser receives only a short-lived session token.

The dashboard shows individual columns in learning order: P0, T1, M1, T2, M2, …, T6, M6, M7. T1–T6 are display names for the existing P1–P6 practice submissions; commands and stored mission IDs still use P. There are no Guided or Challenge summary columns. T6 and M6 combine both sides while retaining their Ubuntu/CloudShell breakdown. Missing reports show a dash, partial results are yellow, and complete results are green. This remains a latest-result view, not a highest-score grade book.

## Student viewing

Student setup defaults to `--instance-type auto`. Before deployment it queries instance metadata, retaining only x86_64 T-series micro sizes, then intersects instance-type offerings with available AZs in the selected region. It chooses the highest numeric generation; within a generation the standard variant is preferred over letter-suffixed alternatives (for example T3 before T3a), then the first compatible AZ. This is a generation policy, not a price or performance ranking. Existing subnet placement and instance type are preserved on ordinary updates. An explicit `--instance-type t3.micro` override is supported and must pass the same architecture/AZ checks. ARM types such as T4g are excluded. Discovery errors or no compatible pair stop deployment. This checks advertised support, not temporary capacity or Academy launch permissions; Learner Lab region and instance-type restrictions still apply. The installer never deletes a failed stack automatically.

If a first installation fails and CloudFormation reaches `ROLLBACK_COMPLETE`, delete only that failed student stack, wait for deletion, and rerun the current student setup command. Retain `~/.jdu-student` when retrying the same installation so its server identity is reused. Do not delete the teacher stack or the Academy foundation stack.

The current dashboard is teacher-only and lists every student's self-declared email and progress. Do not distribute its session URL to students: anyone holding that URL can view the entire table until it expires. HTTPS certificates protect the connection; they do not decide whose progress a viewer may see. The existing AWS-managed execute-api HTTPS endpoint does not require students to install certificates or sign into AWS to open a properly authorized browser page. Client certificates (mutual TLS) are not configured or proposed.

Students run `jdu-my-progress` in their CloudShell. It authenticates with the existing private server token through `POST /student/session` and prints a read-only URL to `GET /student/progress`, valid for at most 15 minutes. The permanent server token never appears in the URL. The student-session namespace is separate from teacher sessions. Each session stores a role, server ID and the issuing credential hash; the personal page reads only that record, never scans all students, and omits email addresses. It rejects a different server ID, expired or missing sessions, and credential changes. A student session cannot open the teacher dashboard, submit results, change emails, or create admin sessions. Responses use no-store and no-referrer headers and no third-party assets. Close the page on shared PCs; its URL is a bearer credential until expiry. DynamoDB TTL removes expired records eventually; application checks expiry on every request.

Update the existing teacher stack to add the two student routes before distributing the helper. New student installations receive it automatically; existing labs can add the helper without re-running the full installer (see the root README). This proves possession of the lab token, not ownership of an email address. If university account identity is required, assess Google sign-in separately, including account availability, OAuth configuration and Academy permissions.

References (checked 2026-09-29): [HTTP API endpoints](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop.html), [mutual TLS client certificates](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-mutual-tls.html).

Keep the semester registration key within the enrolled Google Classroom course. Public teaching materials do not include a working key. This dashboard remains for formative progress, not identity verification or formal grading.

## Data policy

The table stores a random server ID, the student's self-entered Google Classroom email, EC2 instance metadata, the latest guided P0-P6 and challenge M1-M7 scores, and timestamps. P6 and M6 store Ubuntu (2 checks) and CloudShell (4 checks) separately. The dashboard counts each complete only when both parts are complete. It does not store student names. Use `jdu-progress id` on a student server to display its server ID.

The student enters their email once during installation. It is sent over HTTPS with the server token to `/link-email`, after the existing server registration has been read back and the EC2 identity has been checked. The email is not passed to CloudFormation or EC2 and is not printed in installation output. It is cached with mode 0600 in the student's private CloudShell `~/.jdu-student/student-email.txt`, and stored in the teacher's DynamoDB record. Only the authenticated teacher dashboard displays the email; student status responses expose only whether an email is linked. Keep dashboard URLs private. Delete the course progress stack/table and local email caches when no longer needed under the university's record retention policy.

This is **self-declared email linking**, not Google authentication or verification that the student owns the address. Compare emails with your Classroom roster. The same email may appear on several server records after rebuilding; choose the active record using the instance ID and last report. There is no Classroom API integration or automatic grade return. Students no longer need to submit a server ID merely to identify their environment. Existing anonymous records remain compatible and display as unregistered emails until linked.

To correct an email or retry linking after an API problem, the student can run `jdu-register --change-email` or `jdu-register` in the same CloudShell. This does not reset any exercise or alter scores. Initial setup must have registered the server successfully; otherwise diagnose the setup/registration logs first. Do not collect progress.env, server tokens, SSH private keys, or dashboard session URLs as student submissions.

P0-P6 are checked on each student's Ubuntu instance by `jdu-check P1` through `jdu-check P6`; P6 also requires `jdu-check P6` in CloudShell. Each run submits its latest PASS count over HTTPS. The teacher stack receives and displays those results; it does not independently log in to or re-check student instances. The student CloudFormation stack already installs the guided fixtures and check scripts, so no separate teacher-side CloudFormation stack is needed for P0-P6 beyond this progress server.

This is a formative progress view. It is not a tamper-proof examination system because students have administrative access to their own lab server.

## P0への更新

旧M0を手順付き練習P0へ変更しました。P0の送信に対応するため、既存の教員CloudShellでinstallerを再実行して同じスタックを更新します。別のスタックを作らず、現在のスタック名・リージョンを指定してください。既定構成の場合は以下を使います。

```bash
curl -fsSL https://raw.githubusercontent.com/ShinyaHaga0910/OS-Linux-Control/main/2026/v1.0.0/teacher/install-teacher.sh -o /tmp/jdu-install-teacher.sh
bash /tmp/jdu-install-teacher.sh --region us-east-1 --stack-name jdu-linux-progress-2026-v140
jdu-dashboard
```

既存CloudShellの保存済みキーを再利用します。今回の更新では`--rotate-registration-key`を付けません。学生の登録やDynamoDBの既存提出を削除する必要はありません。P0の提出がなければ旧M0の結果をP0欄へ表示し、旧クライアントが送るM0はP0として保存します。P0の新規提出があればその結果を優先します。既存学生EC2のスクリプト更新は[Lab README](../README.md#既存のubuntu環境を使い続ける場合)を参照してください。
