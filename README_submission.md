# README_submission

## Pha A — Short-term memory: buffer vs summary vs sliding

- **Buffer khong du:** giu toan bo 16 message raw, token tang tuyen tinh theo do dai hoi thoai; khong co co che uu tien nen se som vuot token budget trong hoi thoai dai.
- **Compaction giu constraint gi:** ca `summary` va `sliding` deu tach rieng `DURABLE_NOTES` khoi cac luot bi nen. Khi giam `max_recent_messages` tu 6 xuong 4 (raw turn chua `REVIEW-DEADLINE-1600` bi day ra khoi `RECENT_TURNS`), constraint van duoc giu nguyen vi no da duoc trich xuat vao durable note tu truoc, doc lap voi cua so recent turns.
- **Sliding la default cua lab** vi ket hop ca 3 phan: session summary (state), durable notes (constraint/deadline khong duoc quen) va recent turns (K luot gan nhat) — vua kiem soat token vua khong danh mat thong tin quan trong khi buffer thuan tuy khong lam duoc.

<!-- Cac muc con lai (Pha B-E, privacy, phan tich benchmark) se duoc bo sung sau khi hoan thanh cac pha tiep theo. -->
