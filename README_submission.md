# README_submission

## Pha A — Short-term memory: buffer vs summary vs sliding

- **Buffer khong du:** giu toan bo 16 message raw, token tang tuyen tinh theo do dai hoi thoai; khong co co che uu tien nen se som vuot token budget trong hoi thoai dai.
- **Compaction giu constraint gi:** ca `summary` va `sliding` deu tach rieng `DURABLE_NOTES` khoi cac luot bi nen. Khi giam `max_recent_messages` tu 6 xuong 4 (raw turn chua `REVIEW-DEADLINE-1600` bi day ra khoi `RECENT_TURNS`), constraint van duoc giu nguyen vi no da duoc trich xuat vao durable note tu truoc, doc lap voi cua so recent turns.
- **Sliding la default cua lab** vi ket hop ca 3 phan: session summary (state), durable notes (constraint/deadline khong duoc quen) va recent turns (K luot gan nhat) — vua kiem soat token vua khong danh mat thong tin quan trong khi buffer thuan tuy khong lam duoc.

## Pha B — Long-term memory voi Zep Context Block

- `retrieve_long_term` goi `prime_eval_thread` (nap query nhu 1 turn tam thoi vao thread danh gia) roi lay `thread.get_user_context(thread_id=...).context` lam noi dung long-term chinh — day la Context Block do Zep tu lap rap tu user graph theo relevance.
- Bo sung `graph.search(scope="edges", limit=20)` de lay them cac fact kem `valid_at`/`invalid_at`, giup case recency/conflict (E08) phan biet duoc fact cu (Python cho `ORCHID-27`) va fact hien tai (TypeScript/NestJS cho `BLUEBIRD-42`) thay vi chi dua vao Context Block tom tat.
- Ket qua practice: E02 (Python preference), E03 (open loop `benchmark report` 16:00), E08 (recency BLUEBIRD-42/TypeScript/NestJS), E09 (user isolation — Lan chi thay LOTUS-88/Java/Spring Boot, khong leak ORCHID-27 cua Minh) deu PASS.

## Pha C — Episodic memory

- `retrieve_episodic` goi `graph.search(user_id=..., scope="episodes", limit=15)` — tim theo `user_id` (khong phai `graph_id` semantic) vi day la trai nghiem/trajectory rieng cua tung user.
- `render_graph_search(..., episode_char_cap=180)`: gioi han do dai moi episode de nhieu episode ngan, giau marker (vi du reflection) khong bi 1-2 episode dai chiem het budget.
- Ket qua: E04 (trajectory fix async timeout: `ClientSession`, `concurrency=20`, `ASYNC-FIX-20`) va E05 (reflection: `connection churn` khong phai `timeout threshold`) deu PASS.

## Pha D — Semantic memory (standalone graph)

- `retrieve_semantic` tim tren `graph_id` (domain KB dung chung, khong gan voi user nao) thay vi `user_id`.
- Dung `scope="episodes"` de giu nguyen marker literal trong raw document (`PAYMENT-RULE-3`, `CONN-POOL-FIRST`...). Neu dung `scope="auto"` se chi ra extracted facts va mat cac ma nay. Co fallback sang `scope="nodes"` neu `episodes` loi.
- Ket qua: E06 (payment retry: `Idempotency-Key`, `max-3-retries`, `exponential-backoff`) va E11 (incident playbook: `connection pooling`, `CONN-POOL-FIRST`) deu PASS.

<!-- Cac muc con lai (Pha E, privacy, phan tich benchmark) se duoc bo sung sau khi hoan thanh cac pha tiep theo. -->
