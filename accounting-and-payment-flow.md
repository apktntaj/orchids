# Ringkasan Belajar – Accounting & Payment Flow (QBO)

Today I learn; **invoice, payment, AR, Deposit, dan Bank** dalam konteks **QuickBooks Online (QBO)**.  
Struktur: **Konsep → Implementasi di QBO → Mitigasi Edge Case**.

---

## 1. Invoice, AR, dan Status “Paid”

### Konsep
- **Invoice = pernyataan bisnis & akuntansi**, bukan sekadar dokumen tagihan.
- Invoice menciptakan **Accounts Receivable (AR)** → klaim uang ke customer.
- Status **Paid** berarti:
  - AR sudah ditutup
  - **BUKAN jaminan uang sudah masuk bank**

> Paid = selesai secara AR  
> Bank = selesai secara kas

---

### Implementasi di QBO
- Invoice dibuat → AR naik
- Receive Payment:
  - Invoice → status **Paid**
  - AR → turun
  - Uang diarahkan ke:
    - **Deposit (Undeposited Funds)** jika belum ke bank
    - **Bank** jika real-time/final (misalnya wire)

---

### Mitigasi Edge Case
- Invoice bisa **Paid tapi uang belum di bank** → normal (ACH, Stripe, check).
- Invoice **tidak boleh ditutup** hanya karena:
  - customer bilang “sudah kirim check”
  - ada email tanpa bukti sistem/bank
- Paid tanpa bank confirmation → **harus diawasi**, bukan diabaikan.

---

## 2. Deposit / Undeposited Funds

### Konsep
- **Deposit adalah akun aset (Current Asset)** di Chart of Accounts.
- Deposit = **uang sudah dibayar customer, tapi masih di jalan**.
- Deposit **bukan pendapatan**, **bukan bank**, **bukan uang fiktif**.

Deposit berfungsi sebagai **jembatan kejujuran**:
> AR turun → harus diganti aset lain agar neraca seimbang.

---

### Implementasi di QBO
- Receive Payment (ACH, Stripe, Card, Check):
  - AR ↓
  - Deposit ↑
- Saat bank statement confirm:
  - Deposit ↓
  - Bank ↑

---

### Mitigasi Edge Case
- Deposit numpuk lama = red flag:
  - settlement belum terjadi
  - atau salah posting
- Deposit **tidak boleh dilewati**, karena:
  - bank menerima uang dalam **batch**
  - bank **tidak menyediakan detail per invoice**
- Deposit idealnya **kecil & sementara**.

---

## 3. Bank Statement & Rekonsiliasi

### Konsep
- **Bank adalah sumber kebenaran kas terakhir**.
- Bank **tidak tahu invoice, customer, atau AR**.
- Bank hanya tahu:
  - tanggal
  - jumlah
  - deskripsi singkat (ACH / Stripe / Wire)

---

### Implementasi di QBO
- Bank statement dipakai untuk:
  - memindahkan Deposit → Bank
  - melakukan bank reconciliation
- Rekonsiliasi = pengecekan **integritas cerita kas**, bukan formalitas.

---

### Mitigasi Edge Case
- Jangan mencoba menentukan customer **dari bank statement**.
- Detail customer harus dibaca dari:
  - QBO (Receive Payment / Deposit)
- Jika bank masuk tapi tidak jelas invoice-nya:
  - **tahan sebagai unapplied**
  - jangan tebak

---

## 4. ACH, Stripe, Check, Wire (Metode Pembayaran)

### Konsep
- **ACH** = mekanisme / jaringan (batch-based), bukan tempat uang.
- **Stripe** = perusahaan (pihak ketiga) yang memegang uang sementara.
- **Check** = perintah tertulis, **bisa bounce**, paling lambat.
- **Wire** = real-time / same-day, final.

Uang **tidak pernah “masuk ACH”**.  
Uang selalu ada di:
- bank customer
- bank perusahaan
- atau rekening processor (Stripe / Wise)

---

### Implementasi di QBO
- ACH / Stripe / Card / Check:
  - Receive Payment → Deposit → Bank
- Wire:
  - Langsung ke Bank
  - Tidak perlu Deposit

---

### Mitigasi Edge Case
- Check baru aman **setelah clearing bank**.
- ACH bisa reversal → Paid ≠ aman secara kas.
- Wire relatif aman, tapi ada fee.

---

## 5. Matching Payment yang Tidak Deterministik

### Konsep
- Bank batch **tidak menyediakan detail per customer**.
- Matching berdasarkan amount / tanggal **tidak deterministik**.
- Akuntansi profesional **tidak memaksakan kepastian palsu**.

Prinsip utama:
> Lebih baik menunda daripada salah posting.

---

### Implementasi di QBO
- Jika payment ACH masuk bank tapi tidak jelas invoice:
  - simpan sebagai **unapplied payment / suspense**
- Apply ke invoice **hanya jika bukti cukup kuat**.

---

### Mitigasi Edge Case
- Konsekuensi menunda:
  - invoice yang sebenarnya sudah dibayar masih terlihat outstanding
  - risiko double reminder (minor)
- Konsekuensi salah apply:
  - AR bohong
  - customer dispute
  - trust owner rusak (major)

Trade-off yang benar:
> AR sementara jelek lebih aman daripada AR rapi tapi salah.

---

## 6. Outstanding, Partial Payment, dan Overpayment

### Konsep
- **Outstanding = invoice masih open** (belum lunas).
- Partial payment:
  - AR turun sebagian
  - sisa tetap outstanding
- Overpayment:
  - menjadi **customer credit**
  - **bukan revenue**
  - kewajiban sementara perusahaan

---

### Implementasi di QBO
- Partial payment:
  - apply ke invoice tertua dulu (best practice)
- Overpayment:
  - simpan sebagai credit
  - atau refund jika diminta

---

### Mitigasi Edge Case
- Jangan membuat invoice palsu untuk “menghabiskan” credit.
- Jangan mengakui overpayment sebagai revenue.

---

## 7. Fee (Wise, Wire, Stripe)

### Konsep
- **Fee adalah expense perusahaan**, bukan potongan gaji pekerja.
- Gaji / invoice tetap dicatat **gross**.
- Fee dicatat terpisah sebagai **Bank / Transfer Fee**.

---

### Implementasi di QBO
- Salary / invoice: gross amount
- Wise / Wire fee: expense terpisah
- Cash out = gross + fee

---

### Mitigasi Edge Case
- Fee hanya boleh dibebankan ke pekerja jika:
  - kontrak eksplisit menyatakan “net of fees”
- Tanpa itu → fee = tanggung jawab company.

---

## 8. Cara Melihat Laporan untuk Owner

### Konsep
- Laporan tidak boleh dibaca parsial.
- **AR, Deposit, dan Bank harus konsisten**.

---

### Implementasi di QBO
Saat owner minta laporan, cek:
1. **AR Aging** → klaim uang
2. **Deposit** → uang di jalan
3. **Bank statement** → kas nyata

---

### Mitigasi Edge Case
- Revenue bagus + Deposit besar + Bank stagnan = red flag.
- Laporan tanpa cek Deposit & Bank = laporan tanpa verifikasi kas.

---

## Penutup – Prinsip Utama yang Saya Pegang

- Paid ≠ Bank
- AR ≠ Cash
- Deposit = jembatan kejujuran
- Lebih baik menunda daripada salah posting
- Akuntansi = mengelola ketidakpastian tanpa berbohong