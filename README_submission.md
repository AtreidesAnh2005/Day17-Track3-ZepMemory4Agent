# README_submission

## 1. Cau bat buoc (muc 5.2)

**Layer quan trong nhat trong bo test nay:** `long_term` — chiem 4/11 case (E02, E03, E08, E09), phai xu ly ca recency/conflict (E08: TypeScript ghi de Python cho BLUEBIRD-42) va user isolation (E09: Lan/Minh tach biet, khong leak ORCHID-27). Sai o day mat diem nhieu nhat.

**Trade-off Context Block (Zep) vs tu build Redis+Qdrant:** Context Block tu dong tong hop summary + fact + episode co relevance ranking va validity range (`valid_at`/`invalid_at`), khong can tu viet pipeline extract/rank. Redis/Qdrant baseline (`local_baseline.py`) chi cho key-value TTL va similarity search thuan tuy — hoc vien phai tu xu ly conflict/recency/provenance. Doi lai Redis+Qdrant re, chay local, toan quyen schema; Zep la managed service, phu thuoc network/vendor.

**Guardrail chong memory poisoning:** theo `AGENTS.md` va `heartbeat.py` — heartbeat chi de-dup/danh dau stale/tao recap, **khong tu them instruction/quyen moi vao durable memory**. Moi durable write phai giu source/timestamp/confidence/scope (`MEMORY_SCHEMA.md`); conflict dung recency+scope (`MEMORY.md`) thay vi ghi de tuy tien; `privacy_guard.py` yeu cau consent opt-in truoc khi ghi va redact PII.

## 2. Phan tich benchmark (muc 4.5)

1. **Layer hit rate thap nhat:** ca 4 layer dat 100% (11/11 PASS) o benchmark student. Neu thieu implementation, `long_term` de fail nhat vi phai dung dung dinh dang string tra ve tu Context Block.
2. **Query nhieu token nhat:** E03 (long_term, 1376 token) — Context Block tra ve toan bo user summary + nhieu episode lien quan.
3. **E07 (mixed) can:** long-term (Python preference) + semantic (Idempotency-Key payment rule); evidence bat buoc: `Python`, `Idempotency-Key`.
4. **Token reduction:** memory-enabled giam 14.2% so full source, no-memory giam toi 81.8% nhung hit rate chi 18.2% — giam token cao o no-memory chi vi khong retrieve gi ca (re nhung sai), khong phai retrieval hieu qua.

## 3. E08 (recency) va E10 (compaction)

- **E08:** Context Block + `graph.search(scope="edges")` phan biet fact cu (Python cho ORCHID-27) va fact hien tai (TypeScript/NestJS cho BLUEBIRD-42) nho recency+scope.
- **E10:** giam `max_recent_messages` 6→4 khong lam mat `REVIEW-DEADLINE-1600` vi `sliding`/`summary` tach no vao `DURABLE_NOTES`, doc lap voi cua so recent turns bi cat.

## 4. Ket qua benchmark

Practice: **11/11 PASS (100%)**. No-memory baseline: **2/11 (18.2%)**. Chi tiet: `reports/benchmark.md`, `reports/benchmark_no_memory.md`, `reports/comparison.md`.
