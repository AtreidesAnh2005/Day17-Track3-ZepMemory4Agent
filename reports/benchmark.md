# Lab 17 Benchmark Report

- Implementation: `student`
- Kind: `practice`
- Cases: **11**
- Passed: **11/11**
- Evidence hit rate: **100.0%**
- Average retrieval latency: **806.2 ms**
- Average token reduction vs full source context: **19.0%**

| Case | Layer | Pass | Latency ms | Retrieved tokens | Token reduction | Missing / Error |
| --- | --- | --- | ---: | ---: | ---: | --- |
| E01 | short_term | PASS | 0.0 | 133 | 0.0% |  |
| E06 | semantic | PASS | 296.1 | 56 | 87.8% |  |
| E09 | long_term | PASS | 1320.4 | 841 | 0.0% |  |
| E10 | short_term | PASS | 0.2 | 195 | 0.0% |  |
| E02 | long_term | PASS | 1331.6 | 1681 | 0.0% |  |
| E03 | long_term | PASS | 1677.0 | 1612 | 0.0% |  |
| E04 | episodic | PASS | 370.2 | 233 | 0.0% |  |
| E05 | episodic | PASS | 328.5 | 252 | 0.0% |  |
| E07 | mixed | PASS | 1759.4 | 392 | 30.6% |  |
| E11 | semantic | PASS | 205.4 | 55 | 90.3% |  |
| E08 | long_term | PASS | 1579.6 | 1475 | 0.0% |  |

## Evidence excerpts

### E01 - short_term

`<RECENT_TURNS> user: Ten du an ca nhan cua toi la ORCHID-27. Toi thich Python va khong thich Java. Khi giai thich code, hay dung vi du ngan. assistant: Da hieu: demo ca nhan ORCHID-27, uu tien Python, tranh Java, vi du ngan. user: Toi dang hoc async/await va hay nham coroutine voi Task. Neu sau nay gap chu de nay, hay giai thich bang timeline. assistant: Toi se uu tien timeline khi giai thich coroutine va Task. user: TODO: hoan thanh benchmark report truoc thu Sau luc 16:00. Day la open loop LAB-REPORT-1600. </RECENT_TURNS>`

### E06 - semantic

`EPISODE: For POST /payments, every retryable request MUST send the same Idempotency-Key. Retry only HTTP 429 or transient 5xx errors, use exponential-backoff, and stop after max-3-retries. Marker: PAYMENT-RULE-3. metadata=`

### E09 - long_term

`<USER_SUMMARY> Lan Tran's project is LOTUS-88. They prioritize Java and Spring Boot for backend development.  Lan Tran prioritizes Java and Spring Boot for backend development and explicitly does not use Python for the backend. </USER_SUMMARY>  <EPISODES> Episodes are source message or document excerpts shown in selection order.   - Created At: 2026-08-01 11:00:20     Source: message     Content: Lab Assistant (assistant): Da hieu: LOTUS-88, Java + Spring Boot cho backend examples.   - Created At: 2026-08-01 11:00:00     Source: message     Content: [user] {   "user_id": "lan-lab17",   "first_name": "Lan",   "last_name": "Tran",   "user_alias": "Lan Tran" }: Toi la Lan. Du an cua toi la LOTU`

### E10 - short_term

`<SESSION_SUMMARY> user: Constraint: REVIEW-DEADLINE-1600 - project review is Friday at 16:00 and must not be forgotten. | assistant: Acknowledged review constraint. | user: Filler turn 1 about UI spacing. | assistant: Filler answer 1. | user: Filler turn 2 about naming. | assistant: Filler answer 2. | user: Filler turn 3 about logging. | assistant: Filler answer 3. </SESSION_SUMMARY> <DURABLE_NOTES> - user: Constraint: REVIEW-DEADLINE-1600 - project review is Friday at 16:00 and must not be forgotten. - assistant: Acknowledged review constraint. </DURABLE_NOTES> <RECENT_TURNS> user: Filler turn 4 about tests. assistant: Filler answer 4. user: Filler turn 5 about docs. assistant: Filler answe`

### E02 - long_term

`<USER_SUMMARY> Minh Nguyen is working on completing a benchmark report by Friday at 16:00 for an open-loop initiative named LAB-REPORT-1600. The user is debugging async HTTP requests and has increased the timeout to 60 seconds. The user is also checking the connection pool, client lifecycle, and concurrency. The user's effective approach involves reusing the aiohttp ClientSession and setting concurrency to 20, identifying connection churn as the primary issue rather than the timeout threshold, related to incident ASYNC-FIX-20.  Minh Nguyen likes Python and dislikes Java. When explaining code, the user prefers short examples. Their personal project is named ORCHID-27.  When explaining code, u`

### E03 - long_term

`<USER_SUMMARY> Minh Nguyen is working on completing a benchmark report by Friday at 16:00 for an open-loop initiative named LAB-REPORT-1600. The user is debugging async HTTP requests and has increased the timeout to 60 seconds. The user is also checking the connection pool, client lifecycle, and concurrency. The user's effective approach involves reusing the aiohttp ClientSession and setting concurrency to 20, identifying connection churn as the primary issue rather than the timeout threshold, related to incident ASYNC-FIX-20.  Minh Nguyen likes Python and dislikes Java. When explaining code, the user prefers short examples. Their personal project is named ORCHID-27.  When explaining code, u`

### E04 - episodic

`EPISODE: Ten du an ca nhan cua toi la ORCHID-27. Toi thich Python va khong thich Java. Khi giai thich code, hay dung vi du ngan. EPISODE: TODO: hoan thanh benchmark report truoc thu Sau luc 16:00. Day la open loop LAB-REPORT-1600. EPISODE: Cap nhat moi: voi du an cong ty BLUEBIRD-42, backend bat buoc dung TypeScript voi NestJS; khong dung Python cho backend du an nay. Preference Python van dung cho demo ca nhan ORCHI EPISODE: Cach hieu qua la reuse aiohttp ClientSession va dat concurrency=20. Reflection: loi chinh la connection churn, khong phai timeout threshold. Ma su co ASYNC-FIX-20. EPISODE: Toi dang hoc async/await va hay nham coroutine voi Task. Neu sau nay gap chu de nay, hay giai thi`

### E05 - episodic

`EPISODE: Ten du an ca nhan cua toi la ORCHID-27. Toi thich Python va khong thich Java. Khi giai thich code, hay dung vi du ngan. EPISODE: TODO: hoan thanh benchmark report truoc thu Sau luc 16:00. Day la open loop LAB-REPORT-1600. EPISODE: Cap nhat moi: voi du an cong ty BLUEBIRD-42, backend bat buoc dung TypeScript voi NestJS; khong dung Python cho backend du an nay. Preference Python van dung cho demo ca nhan ORCHI EPISODE: Cach hieu qua la reuse aiohttp ClientSession va dat concurrency=20. Reflection: loi chinh la connection churn, khong phai timeout threshold. Ma su co ASYNC-FIX-20. EPISODE: Toi dang hoc async/await va hay nham coroutine voi Task. Neu sau nay gap chu de nay, hay giai thi`

### E07 - mixed

`<LONG_TERM> <USER_SUMMARY> Minh Nguyen is working on completing a benchmark report by Friday at 16:00 for an open-loop initiative named LAB-REPORT-1600. The user is debugging async HTTP requests and has increased the timeout to 60 seconds. The user is also checking the connection pool, client lifecycle, and concurrency. The user's effective approach involves reusing the aiohttp ClientSession and setting concurrency to 20, identifying connection churn as the primary issue rather than the timeout threshold, related to incident ASYNC-FIX-20.  Minh Nguyen likes Python and dislikes Java. When explaining code, the user prefers short examples. Their personal project is named ORCHID-27.  When explai`

### E11 - semantic

`EPISODE: When async HTTP calls time out, inspect connection pooling, downstream saturation and concurrency before increasing timeout. Reuse a long-lived client session where possible. Marker: CONN-POOL-FIRST. metadata=`

### E08 - long_term

`<USER_SUMMARY> Minh Nguyen is working on completing a benchmark report by Friday at 16:00 for an open-loop initiative named LAB-REPORT-1600. The user is debugging async HTTP requests and has increased the timeout to 60 seconds. The user is also checking the connection pool, client lifecycle, and concurrency. The user's effective approach involves reusing the aiohttp ClientSession and setting concurrency to 20, identifying connection churn as the primary issue rather than the timeout threshold, related to incident ASYNC-FIX-20.  Minh Nguyen likes Python and dislikes Java. When explaining code, the user prefers short examples. Their personal project is named ORCHID-27.  When explaining code, u`
