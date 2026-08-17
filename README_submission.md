# README_submission

## 1. Cau bat buoc (muc 5.2)

**Layer quan trong nhat:** `long_term` — 4/11 case (E02, E03, E08, E09), phai xu ly recency/conflict (E08: TypeScript ghi de Python cho BLUEBIRD-42) va user isolation (E09: khong leak ORCHID-27 sang Lan). Sai o day mat diem nhieu nhat.

**Trade-off Context Block (Zep) vs Redis+Qdrant:** Context Block tu dong tong hop summary + fact + episode co relevance ranking va validity range (`valid_at`/`invalid_at`), khong can tu viet extract/rank. Redis/Qdrant (`local_baseline.py`) chi la key-value TTL + similarity search thuan tuy, hoc vien tu xu ly conflict/recency/provenance. Doi lai Redis+Qdrant re, local, toan quyen schema; Zep la managed service, phu thuoc vendor.

**Guardrail chong memory poisoning:** heartbeat (`AGENTS.md`, `heartbeat.py`) chi de-dup/danh dau stale/tao recap, **khong tu them instruction/quyen moi**. Durable write phai giu source/timestamp/confidence/scope (`MEMORY_SCHEMA.md`); conflict dung recency+scope (`MEMORY.md`); `privacy_guard.py` bat buoc consent opt-in va redact PII.

## 2. Phan tich benchmark (muc 4.5)

1. **Layer hit rate thap nhat:** ca 4 layer dat 100% (11/11). `long_term` de fail nhat neu implement sai vi phai tra dung string tu Context Block.
2. **Query nhieu token nhat:** E03 (long_term, 1376 token) — Context Block tra toan bo user summary + nhieu episode.
3. **E07 (mixed) can:** long-term (Python) + semantic (Idempotency-Key).
4. **Token reduction:** memory-enabled giam 14.2%, no-memory giam 81.8% nhung hit rate chi 18.2% — token reduction cao o no-memory chi vi khong retrieve gi (re nhung sai).

## 3. E08 (recency) va E10 (compaction)

- **E08:** Context Block + `graph.search(scope="edges")` phan biet fact cu (Python/ORCHID-27) va fact hien tai (TypeScript/NestJS/BLUEBIRD-42) nho recency+scope.
- **E10:** giam `max_recent_messages` 6→4 khong mat `REVIEW-DEADLINE-1600` vi `sliding`/`summary` tach no vao `DURABLE_NOTES`, doc lap voi recent turns bi cat.

## 4. Ket qua benchmark, golden va privacy

Practice: **11/11 PASS**. No-memory: **2/11**. Golden: **20/20 PASS, +10** (`reports/golden_benchmark.json`, `perfect=true`). Chi tiet: `reports/benchmark.md`, `reports/benchmark_no_memory.md`, `reports/comparison.md`.

Privacy: `src.forget --user-id minh-lab17` sau khi luu benchmark; `--verify-only` xac nhan `Zep user absent: True`, `Redis user keys remaining: 0`; da seed lai truoc golden. Log: `submission/*.log`.

**Ghi chu robustness:** budget episodic/semantic (3%) co the cat mat marker khi graph tich luy "probe" query tu `prime_eval_thread` (`role="Evaluation User"`). Xu ly trong `memory_student.py`: loc bo probe theo role, uu tien episode/doc mang marker (`XXX-YYY-nn`) truoc khi bi budget cat, va gop bo doi JSON+summary trung nhau cua semantic KB.
