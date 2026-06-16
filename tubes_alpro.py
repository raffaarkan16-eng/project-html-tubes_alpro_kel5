"""
  Fitur:
  - CRUD pengeluaran perjalanan
  - Sequential Search & Binary Search
  - Selection Sort & Insertion Sort
  - Laporan total + saran hemat budget
  - Rekomendasi alokasi budget
  - GUI menggunakan ttkbootstrap (tema flatly)
=============================================================
"""

from datetime import datetime
from tkinter import messagebox

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# DATA STORAGE

data_pengeluaran = []
id_counter = [1]

KATEGORI_LIST = ["Transportasi", "Akomodasi", "Makanan", "Hiburan", "Lainnya"]

BATAS_HEMAT = {
    "Transportasi": 1_000_000,
    "Akomodasi": 1_500_000,
    "Makanan": 500_000,
    "Hiburan": 300_000,
    "Lainnya": 200_000,
}

ALOKASI_PERSEN = {
    "Transportasi": 0.30,
    "Akomodasi": 0.30,
    "Makanan": 0.20,
    "Hiburan": 0.10,
    "Lainnya": 0.10,
}

TIPS_KAT = {
    "Transportasi": "Tiket pesawat/kereta, taksi, bensin",
    "Akomodasi": "Hotel, penginapan, homestay",
    "Makanan": "Makan & minum selama perjalanan",
    "Hiburan": "Wisata, tiket masuk, aktivitas",
    "Lainnya": "Oleh-oleh, darurat, tak terduga",
}


# Algoritma menggunakan (Sequential Search, Binary Search, Selection Sort, Insertion Sort)


def sequential_search(data, keyword):
    """
    Mencari pengeluaran berdasarkan nama atau kategori.
    Kompleksitas O(n) — cocok untuk data tidak terurut.
    """
    keyword = keyword.strip().lower()
    hasil = []
    for item in data:
        if keyword in item["kategori"].lower() or keyword in item["nama"].lower():
            hasil.append(item)
    return hasil


def binary_search(data, keyword):
    """
    Mencari pengeluaran berdasarkan kategori (harus tepat).
    Data diurutkan dulu dengan insertion sort. Kompleksitas O(log n).
    """
    keyword = keyword.strip().lower()
    sorted_data = insertion_sort_by_kategori(data[:])

    low, high, found_index = 0, len(sorted_data) - 1, -1
    while low <= high:
        mid = (low + high) // 2
        mid_val = sorted_data[mid]["kategori"].lower()
        if mid_val == keyword:
            found_index = mid
            break
        elif mid_val < keyword:
            low = mid + 1
        else:
            high = mid - 1

    if found_index == -1:
        return []

    hasil = []
    i = found_index
    while i >= 0 and sorted_data[i]["kategori"].lower() == keyword:
        hasil.append(sorted_data[i])
        i -= 1
    i = found_index + 1
    while i < len(sorted_data) and sorted_data[i]["kategori"].lower() == keyword:
        hasil.append(sorted_data[i])
        i += 1
    return hasil


def selection_sort_by_jumlah(data):
    """
    Urutkan jumlah terbesar ke terkecil.
    Cara kerja: cari nilai max, tukar ke posisi depan, ulangi.
    Kompleksitas O(n^2).
    """
    arr = data[:]
    n = len(arr)
    for i in range(n):
        max_idx = i
        for j in range(i + 1, n):
            if arr[j]["jumlah"] > arr[max_idx]["jumlah"]:
                max_idx = j
        arr[i], arr[max_idx] = arr[max_idx], arr[i]
    return arr


def insertion_sort_by_kategori(data):
    """
    Urutkan kategori A-Z.
    Cara kerja: ambil elemen, geser yang lebih besar, sisipkan.
    Kompleksitas O(n^2).
    """
    arr = data[:]
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j]["kategori"].lower() > key["kategori"].lower():
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def buat_laporan(data):
    """Hitung total per kategori dan beri saran hemat."""
    total_per_kategori = {}
    for item in data:
        kat = item["kategori"]
        total_per_kategori[kat] = total_per_kategori.get(kat, 0) + item["jumlah"]
    total_semua = sum(total_per_kategori.values())
    saran = []
    for kat, total in total_per_kategori.items():
        batas = BATAS_HEMAT.get(kat, 500_000)
        if total > batas:
            lebih = total - batas
            saran.append(
                (
                    "!",
                    kat,
                    total,
                    batas,
                    f"Melebihi batas Rp {batas:,.0f}  —  Hemat Rp {lebih:,.0f}",
                )
            )
        else:
            sisa = batas - total
            saran.append(
                ("v", kat, total, batas, f"Aman  —  Sisa budget Rp {sisa:,.0f}")
            )
    return total_per_kategori, total_semua, saran


# DATA DEMO


def muat_data_demo():
    demo = [
        {
            "nama": "Tiket Pesawat Jakarta-Bali",
            "kategori": "Transportasi",
            "jumlah": 850000,
            "tanggal": "2026-06-01",
            "keterangan": "Penerbangan pagi",
        },
        {
            "nama": "Hotel Kuta 3 Malam",
            "kategori": "Akomodasi",
            "jumlah": 1200000,
            "tanggal": "2026-06-01",
            "keterangan": "Termasuk sarapan",
        },
        {
            "nama": "Makan Malam Seafood",
            "kategori": "Makanan",
            "jumlah": 275000,
            "tanggal": "2026-06-02",
            "keterangan": "Jimbaran",
        },
        {
            "nama": "Rafting Ubud",
            "kategori": "Hiburan",
            "jumlah": 350000,
            "tanggal": "2026-06-03",
            "keterangan": "Sewa peralatan included",
        },
        {
            "nama": "Taksi Online",
            "kategori": "Transportasi",
            "jumlah": 120000,
            "tanggal": "2026-06-02",
            "keterangan": "Dari bandara ke hotel",
        },
        {
            "nama": "Oleh-oleh Bali",
            "kategori": "Lainnya",
            "jumlah": 450000,
            "tanggal": "2026-06-04",
            "keterangan": "Kain dan kerajinan",
        },
        {
            "nama": "Makan Siang Warung Lokal",
            "kategori": "Makanan",
            "jumlah": 85000,
            "tanggal": "2026-06-03",
            "keterangan": "Nasi campur",
        },
    ]
    for d in demo:
        data_pengeluaran.append(
            {
                "id": id_counter[0],
                "nama": d["nama"],
                "kategori": d["kategori"],
                "jumlah": d["jumlah"],
                "tanggal": d["tanggal"],
                "keterangan": d["keterangan"],
            }
        )
        id_counter[0] += 1


# GUI - HELPER TREEVIEW


def buat_treeview(parent, kolom, lebar_kolom, tinggi=12):
    """Membuat Treeview dengan scrollbar vertikal dan horizontal."""
    frame = ttk.Frame(parent)

    # Scrollbar vertikal & horizontal
    sb_y = ttk.Scrollbar(frame, orient=VERTICAL, bootstyle="secondary-round")
    sb_x = ttk.Scrollbar(frame, orient=HORIZONTAL, bootstyle="secondary-round")

    tree = ttk.Treeview(
        frame,
        columns=kolom,
        show="headings",
        height=tinggi,
        yscrollcommand=sb_y.set,
        xscrollcommand=sb_x.set,
        bootstyle="primary",
    )
    sb_y.config(command=tree.yview)
    sb_x.config(command=tree.xview)

    for col, lbr in zip(kolom, lebar_kolom):
        tree.heading(col, text=col, anchor=CENTER)
        tree.column(col, width=lbr, minwidth=40, anchor=CENTER)

    sb_y.pack(side=RIGHT, fill=Y)
    sb_x.pack(side=BOTTOM, fill=X)
    tree.pack(fill=BOTH, expand=YES)
    return frame, tree


def isi_treeview(tree, data):
    """Kosongkan lalu isi ulang Treeview dengan data pengeluaran"""
    tree.delete(*tree.get_children())
    for item in data:
        tree.insert(
            "",
            END,
            values=(
                item["id"],
                item["nama"],
                item["kategori"],
                f"Rp {item['jumlah']:,.0f}",
                item["tanggal"],
                item["keterangan"],
            ),
        )


# GUI - FORM TAMBAH / EDIT


def form_pengeluaran(parent, app_ref, mode="tambah", item=None):
    """
    Jendela Toplevel untuk input data pengeluaran.
    mode = 'tambah' atau 'edit'
    """
    win = ttk.Toplevel(parent)
    win.title("Tambah Pengeluaran" if mode == "tambah" else "Edit Pengeluaran")
    win.geometry("460x380")
    win.resizable(False, False)
    win.grab_set()

    # LabelFrame sebagai wadah form

    lf = ttk.Labelframe(
        win, text="  Data Pengeluaran  ", bootstyle="primary", padding=16
    )
    lf.pack(fill=BOTH, expand=YES, padx=20, pady=16)

    labels = [
        "Nama Pengeluaran",
        "Jumlah (Rp)",
        "Kategori",
        "Tanggal (YYYY-MM-DD)",
        "Keterangan",
    ]
    for i, lbl in enumerate(labels):
        ttk.Label(lf, text=lbl + ":", anchor=W).grid(
            row=i, column=0, sticky=W, pady=6, padx=(0, 12)
        )

    e_nama = ttk.Entry(lf, width=30)
    e_jumlah = ttk.Entry(lf, width=30)
    var_kat = ttk.StringVar(value=KATEGORI_LIST[0])

    # Combobox (dropdown)

    e_kat = ttk.Combobox(
        lf, textvariable=var_kat, values=KATEGORI_LIST, state="readonly", width=28
    )
    e_tgl = ttk.Entry(lf, width=30)
    e_ket = ttk.Entry(lf, width=30)

    for i, widget in enumerate([e_nama, e_jumlah, e_kat, e_tgl, e_ket]):
        widget.grid(row=i, column=1, sticky=EW, pady=6)

    # Isi nilai jika mode edit
    if mode == "edit" and item:
        e_nama.insert(0, item["nama"])
        e_jumlah.insert(0, str(int(item["jumlah"])))
        var_kat.set(item["kategori"])
        e_tgl.insert(0, item["tanggal"])
        e_ket.insert(0, item["keterangan"])
    else:
        e_tgl.insert(0, datetime.today().strftime("%Y-%m-%d"))

    def simpan():
        nama = e_nama.get().strip()
        if not nama:
            messagebox.showerror(
                "Error", "Nama pengeluaran tidak boleh kosong!", parent=win
            )
            return
        try:
            jumlah = float(e_jumlah.get().strip().replace(",", "").replace(".", ""))
            if jumlah < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Error", "Jumlah harus berupa angka positif!", parent=win
            )
            return

        if mode == "tambah":
            data_pengeluaran.append(
                {
                    "id": id_counter[0],
                    "nama": nama,
                    "kategori": var_kat.get(),
                    "jumlah": jumlah,
                    "tanggal": e_tgl.get().strip(),
                    "keterangan": e_ket.get().strip(),
                }
            )
            id_counter[0] += 1
        else:
            item.update(
                nama=nama,
                jumlah=jumlah,
                kategori=var_kat.get(),
                tanggal=e_tgl.get().strip(),
                keterangan=e_ket.get().strip(),
            )

        win.destroy()
        app_ref.refresh_semua()

    # Tombol Simpan & Batal
    frm_btn = ttk.Frame(win)
    frm_btn.pack(pady=6)
    ttk.Button(
        frm_btn, text="💾  Simpan", command=simpan, bootstyle="success", width=14
    ).pack(side=LEFT, padx=8)
    ttk.Button(
        frm_btn, text="Batal", command=win.destroy, bootstyle="danger-outline", width=10
    ).pack(side=LEFT, padx=8)


# GUI - KELAS UTAMA APLIKASI


class AplikasiBudgetTravel:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Pengelolaan Budget Traveling")
        self.root.geometry("980x640")

        self._bangun_ui()

    # Bangun keseluruhan UI

    def _bangun_ui(self):
        # ── Header atas ──
        frm_header = ttk.Frame(self.root, bootstyle="primary", padding=14)
        frm_header.pack(fill=X)
        ttk.Label(
            frm_header,
            text="✈  Aplikasi Pengelolaan Budget Traveling",
            font=("Segoe UI", 15, "bold"),
            bootstyle="inverse-primary",
        ).pack(side=LEFT)
        self.lbl_ringkas = ttk.Label(
            frm_header, text="", font=("Segoe UI", 10), bootstyle="inverse-primary"
        )
        self.lbl_ringkas.pack(side=RIGHT, padx=10)

        # Notebook (tab menu)

        self.nb = ttk.Notebook(self.root, bootstyle="primary")
        self.nb.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        self.tab_data = ttk.Frame(self.nb, padding=10)
        self.tab_cari = ttk.Frame(self.nb, padding=10)
        self.tab_urut = ttk.Frame(self.nb, padding=10)
        self.tab_laporan = ttk.Frame(self.nb, padding=10)
        self.tab_rekomendasi = ttk.Frame(self.nb, padding=10)

        self.nb.add(self.tab_data, text="  📋  Data Pengeluaran  ")
        self.nb.add(self.tab_cari, text="  🔍  Pencarian  ")
        self.nb.add(self.tab_urut, text="  ↕️  Pengurutan  ")
        self.nb.add(self.tab_laporan, text="  📊  Laporan  ")
        self.nb.add(self.tab_rekomendasi, text="  💡  Rekomendasi  ")

        self._bangun_tab_data()
        self._bangun_tab_cari()
        self._bangun_tab_urut()
        self._bangun_tab_laporan()
        self._bangun_tab_rekomendasi()

        #  Status bar bawah

        self.lbl_status = ttk.Label(
            self.root,
            text="  Selamat datang! Klik 'Muat Demo' untuk memuat data contoh.",
            bootstyle="secondary",
            anchor=W,
        )
        self.lbl_status.pack(fill=X, side=BOTTOM)

        self._update_ringkas()

    def set_status(self, pesan):
        self.lbl_status.config(text=f"  {pesan}")

    def _update_ringkas(self):
        total = sum(d["jumlah"] for d in data_pengeluaran)
        self.lbl_ringkas.config(
            text=f"{len(data_pengeluaran)} transaksi  |  Total: Rp {total:,.0f}"
        )

    def refresh_semua(self):
        """Refresh semua tab setelah ada perubahan data."""
        isi_treeview(self.tree_data, data_pengeluaran)
        self._update_ringkas()
        self.set_status("Data diperbarui.")

    # TAB 1: Data Pengeluaran (CRUD)

    def _bangun_tab_data(self):
        tab = self.tab_data

        # Toolbar tombol CRUD
        frm_tb = ttk.Frame(tab)
        frm_tb.pack(fill=X, pady=(0, 8))

        ttk.Button(
            frm_tb,
            text="➕  Tambah",
            command=lambda: form_pengeluaran(self.root, self, "tambah"),
            bootstyle="success",
            width=13,
        ).pack(side=LEFT, padx=(0, 6))
        ttk.Button(
            frm_tb,
            text="✏️  Edit",
            command=self._edit_pengeluaran,
            bootstyle="warning",
            width=11,
        ).pack(side=LEFT, padx=6)
        ttk.Button(
            frm_tb,
            text="🗑️  Hapus",
            command=self._hapus_pengeluaran,
            bootstyle="danger",
            width=11,
        ).pack(side=LEFT, padx=6)

        # Separator — sesuai modul 7.2
        ttk.Separator(frm_tb, orient=VERTICAL).pack(side=LEFT, fill=Y, padx=14, pady=2)

        ttk.Button(
            frm_tb,
            text="⚡  Muat Demo",
            command=self._muat_demo,
            bootstyle="info-outline",
            width=13,
        ).pack(side=LEFT)
        ttk.Button(
            frm_tb,
            text="🔄  Refresh",
            command=self.refresh_semua,
            bootstyle="secondary-outline",
            width=11,
        ).pack(side=LEFT, padx=6)

        # Treeview tabel data
        kolom = [
            "ID",
            "Nama Pengeluaran",
            "Kategori",
            "Jumlah (Rp)",
            "Tanggal",
            "Keterangan",
        ]
        lebar = [45, 230, 120, 140, 105, 200]
        frm_t, self.tree_data = buat_treeview(tab, kolom, lebar, tinggi=16)
        frm_t.pack(fill=BOTH, expand=YES)

        isi_treeview(self.tree_data, data_pengeluaran)

    def _item_terpilih(self):
        sel = self.tree_data.selection()
        if not sel:
            messagebox.showwarning(
                "Peringatan", "Pilih satu baris data terlebih dahulu!"
            )
            return None
        id_val = int(self.tree_data.item(sel[0])["values"][0])
        return next((x for x in data_pengeluaran if x["id"] == id_val), None)

    def _edit_pengeluaran(self):
        item = self._item_terpilih()
        if item:
            form_pengeluaran(self.root, self, "edit", item)

    def _hapus_pengeluaran(self):
        item = self._item_terpilih()
        if not item:
            return
        if messagebox.askyesno(
            "Konfirmasi Hapus",
            f"Yakin ingin menghapus:\n\n'{item['nama']}' (Rp {item['jumlah']:,.0f})?",
        ):
            data_pengeluaran.remove(item)
            self.refresh_semua()
            self.set_status(f"Data '{item['nama']}' berhasil dihapus.")

    def _muat_demo(self):
        if messagebox.askyesno(
            "Muat Data Demo", "Tambahkan 7 data contoh ke aplikasi?"
        ):
            muat_data_demo()
            self.refresh_semua()
            messagebox.showinfo("Berhasil", "7 data demo berhasil dimuat!")
            self.set_status("Data demo dimuat: 7 data baru ditambahkan.")

    # TAB 2: Pencarian

    def _bangun_tab_cari(self):
        tab = self.tab_cari

        # LabelFrame input pencarian
        lf = ttk.Labelframe(
            tab, text="  Parameter Pencarian  ", bootstyle="primary", padding=14
        )
        lf.pack(fill=X, pady=(0, 12))

        # Entry kata kunci
        ttk.Label(lf, text="Kata Kunci:").grid(
            row=0, column=0, sticky=W, padx=(0, 10), pady=6
        )
        self.entry_cari = ttk.Entry(lf, width=32)
        self.entry_cari.grid(row=0, column=1, sticky=W, padx=(0, 20), pady=6)

        ttk.Label(lf, text="Metode:").grid(row=0, column=2, sticky=W, padx=(0, 10))
        self.var_metode_cari = ttk.StringVar(value="Sequential Search  O(n)")
        ttk.Combobox(
            lf,
            textvariable=self.var_metode_cari,
            width=28,
            state="readonly",
            values=["Sequential Search  O(n)", "Binary Search  O(log n)"],
        ).grid(row=0, column=3, padx=(0, 14))

        ttk.Button(
            lf,
            text="🔍  Cari",
            command=self._jalankan_cari,
            bootstyle="primary",
            width=12,
        ).grid(row=0, column=4)

        self.lbl_hasil_cari = ttk.Label(lf, text="", bootstyle="secondary")
        self.lbl_hasil_cari.grid(row=1, column=0, columnspan=5, sticky=W, pady=(6, 0))

        # Treeview hasil pencarian
        kolom = [
            "ID",
            "Nama Pengeluaran",
            "Kategori",
            "Jumlah (Rp)",
            "Tanggal",
            "Keterangan",
        ]
        lebar = [45, 230, 120, 140, 105, 200]
        frm_t, self.tree_cari = buat_treeview(tab, kolom, lebar, tinggi=14)
        frm_t.pack(fill=BOTH, expand=YES)

    def _jalankan_cari(self):
        kw = self.entry_cari.get().strip()
        if not kw:
            messagebox.showwarning("Peringatan", "Masukkan kata kunci pencarian!")
            return
        if not data_pengeluaran:
            messagebox.showinfo("Info", "Belum ada data pengeluaran.")
            return

        if "Sequential" in self.var_metode_cari.get():
            hasil = sequential_search(data_pengeluaran, kw)
            algo = "Sequential Search O(n)"
        else:
            hasil = binary_search(data_pengeluaran, kw)
            algo = "Binary Search O(log n) — masukkan nama kategori yang tepat"

        isi_treeview(self.tree_cari, hasil)
        warna = "success" if hasil else "danger"
        self.lbl_hasil_cari.config(
            text=f"Algoritma: {algo}  |  Keyword: '{kw}'  |  Ditemukan: {len(hasil)} data",
            bootstyle=warna,
        )
        self.set_status(f"Pencarian '{kw}': {len(hasil)} data ditemukan.")

    # TAB 3: Pengurutan

    def _bangun_tab_urut(self):
        tab = self.tab_urut

        lf = ttk.Labelframe(
            tab, text="  Parameter Pengurutan  ", bootstyle="primary", padding=14
        )
        lf.pack(fill=X, pady=(0, 12))

        ttk.Label(lf, text="Metode:").pack(side=LEFT, padx=(0, 10))
        self.var_metode_urut = ttk.StringVar(
            value="Selection Sort — Jumlah Terbesar ke Terkecil"
        )
        ttk.Combobox(
            lf,
            textvariable=self.var_metode_urut,
            width=38,
            state="readonly",
            values=[
                "Selection Sort — Jumlah Terbesar ke Terkecil",
                "Insertion Sort — Kategori A sampai Z",
            ],
        ).pack(side=LEFT, padx=(0, 14))
        ttk.Button(
            lf,
            text="↕️  Urutkan",
            command=self._jalankan_urut,
            bootstyle="primary",
            width=13,
        ).pack(side=LEFT)

        self.lbl_info_urut = ttk.Label(tab, text="", bootstyle="info")
        self.lbl_info_urut.pack(anchor=W, pady=(0, 6))

        kolom = ["ID", "Nama Pengeluaran", "Kategori", "Jumlah (Rp)", "Tanggal"]
        lebar = [45, 280, 140, 160, 120]
        frm_t, self.tree_urut = buat_treeview(tab, kolom, lebar, tinggi=15)
        frm_t.pack(fill=BOTH, expand=YES)

    def _jalankan_urut(self):
        if not data_pengeluaran:
            messagebox.showinfo("Info", "Belum ada data pengeluaran.")
            return

        if "Selection" in self.var_metode_urut.get():
            hasil = selection_sort_by_jumlah(data_pengeluaran)
            info = "Selection Sort O(n²)  —  Jumlah terbesar ke terkecil"
        else:
            hasil = insertion_sort_by_kategori(data_pengeluaran)
            info = "Insertion Sort O(n²)  —  Kategori A sampai Z"

        self.tree_urut.delete(*self.tree_urut.get_children())
        for item in hasil:
            self.tree_urut.insert(
                "",
                END,
                values=(
                    item["id"],
                    item["nama"],
                    item["kategori"],
                    f"Rp {item['jumlah']:,.0f}",
                    item["tanggal"],
                ),
            )
        self.lbl_info_urut.config(text=f"  ✔  {info}")
        self.set_status(info)

    # TAB 4: Laporan

    def _bangun_tab_laporan(self):
        tab = self.tab_laporan

        ttk.Button(
            tab,
            text="🔄  Perbarui Laporan",
            command=self._tampil_laporan,
            bootstyle="primary",
            width=20,
        ).pack(anchor=W, pady=(0, 10))

        # LabelFrame total per kategori
        self.lf_laporan = ttk.Labelframe(
            tab, text="  Total Per Kategori  ", bootstyle="primary", padding=10
        )
        self.lf_laporan.pack(fill=X, pady=(0, 10))

        kolom = ["Kategori", "Total Pengeluaran (Rp)", "Batas Aman (Rp)", "Status"]
        lebar = [160, 220, 200, 200]
        frm_t, self.tree_laporan = buat_treeview(
            self.lf_laporan, kolom, lebar, tinggi=6
        )
        frm_t.pack(fill=X)

        # LabelFrame saran hemat
        self.lf_saran = ttk.Labelframe(
            tab, text="  Saran Hemat Budget  ", bootstyle="info", padding=10
        )
        self.lf_saran.pack(fill=BOTH, expand=YES)

        self.txt_saran = ttk.Text(
            self.lf_saran, height=7, state=DISABLED, font=("Segoe UI", 10)
        )
        self.txt_saran.pack(fill=BOTH, expand=YES)

        self._tampil_laporan()

    def _tampil_laporan(self):
        self.tree_laporan.delete(*self.tree_laporan.get_children())
        self.txt_saran.config(state=NORMAL)
        self.txt_saran.delete("1.0", END)

        if not data_pengeluaran:
            self.txt_saran.insert(
                END, "Belum ada data pengeluaran. Muat data demo terlebih dahulu."
            )
            self.txt_saran.config(state=DISABLED)
            return

        total_kat, total_semua, saran = buat_laporan(data_pengeluaran)

        for flag, kat, total, batas, _ in saran:
            status = "✅  AMAN" if flag == "v" else "⚠️  MELEBIHI"
            self.tree_laporan.insert(
                "",
                END,
                values=(kat, f"Rp {total:,.0f}", f"Rp {batas:,.0f}", status),
                tags=("aman" if flag == "v" else "lebih",),
            )

        self.tree_laporan.tag_configure("aman", foreground="#16A34A")
        self.tree_laporan.tag_configure("lebih", foreground="#DC2626")

        self.txt_saran.insert(END, f"TOTAL SEMUA PENGELUARAN : Rp {total_semua:,.0f}\n")
        self.txt_saran.insert(END, "-" * 55 + "\n")
        for flag, kat, total, batas, pesan in saran:
            ikon = "✅" if flag == "v" else "⚠️"
            self.txt_saran.insert(
                END, f" {ikon}  {kat:<16}  Rp {total:>12,.0f}   {pesan}\n"
            )

        self.txt_saran.config(state=DISABLED)
        self.set_status("Laporan diperbarui.")

    # TAB 5: Rekomendasi Budget

    def _bangun_tab_rekomendasi(self):
        tab = self.tab_rekomendasi

        # LabelFrame input budget
        lf_input = ttk.Labelframe(
            tab, text="  Masukkan Total Budget Kamu  ", bootstyle="primary", padding=14
        )
        lf_input.pack(fill=X, pady=(0, 12))

        ttk.Label(lf_input, text="Total Budget (Rp):").grid(
            row=0, column=0, sticky=W, padx=(0, 12), pady=6
        )
        self.entry_budget = ttk.Entry(lf_input, width=26, font=("Segoe UI", 11))
        self.entry_budget.grid(row=0, column=1, sticky=W, padx=(0, 16), pady=6)
        self.entry_budget.insert(0, "2000000")

        ttk.Button(
            lf_input,
            text="💡  Hitung Rekomendasi",
            command=self._hitung_rekomendasi,
            bootstyle="primary",
            width=22,
        ).grid(row=0, column=2, padx=6)

        self.lbl_info_rek = ttk.Label(lf_input, text="", bootstyle="info")
        self.lbl_info_rek.grid(row=1, column=0, columnspan=3, sticky=W, pady=(6, 0))

        # Label Frame tabel alokasi
        lf_alokasi = ttk.Labelframe(
            tab, text="  Alokasi Per Kategori  ", bootstyle="success", padding=10
        )
        lf_alokasi.pack(fill=X, pady=(0, 10))

        kolom_rek = ["Kategori", "Porsi (%)", "Alokasi (Rp)", "Keterangan"]
        lebar_rek = [160, 100, 200, 290]
        frm_tr, self.tree_rek = buat_treeview(
            lf_alokasi, kolom_rek, lebar_rek, tinggi=6
        )
        frm_tr.pack(fill=X)

        # Label Frame perbandingan vs aktual
        self.lf_banding = ttk.Labelframe(
            tab,
            text="  Perbandingan vs Pengeluaran Aktual  ",
            bootstyle="warning",
            padding=10,
        )
        self.lf_banding.pack(fill=BOTH, expand=YES)

        kolom_b = [
            "Kategori",
            "Rekomendasi (Rp)",
            "Aktual (Rp)",
            "Selisih (Rp)",
            "Status",
        ]
        lebar_b = [150, 175, 175, 175, 130]
        frm_tb, self.tree_banding = buat_treeview(
            self.lf_banding, kolom_b, lebar_b, tinggi=7
        )
        frm_tb.pack(fill=BOTH, expand=YES)

        self.lbl_kesimpulan = ttk.Label(
            self.lf_banding,
            text="",
            font=("Segoe UI", 10, "bold"),
            wraplength=880,
            anchor=W,
        )
        self.lbl_kesimpulan.pack(fill=X, pady=(8, 0))

    def _hitung_rekomendasi(self):
        try:
            total_budget = float(
                self.entry_budget.get()
                .strip()
                .replace(",", "")
                .replace(".", "")
                .replace(" ", "")
            )
            if total_budget <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Error", "Masukkan nominal budget yang valid (angka positif)!"
            )
            return

        # Isi tabel alokasi
        self.tree_rek.delete(*self.tree_rek.get_children())
        rekomendasi = {}
        for kat, persen in ALOKASI_PERSEN.items():
            nominal = total_budget * persen
            rekomendasi[kat] = nominal
            self.tree_rek.insert(
                "",
                END,
                values=(
                    kat,
                    f"{persen * 100:.0f}%",
                    f"Rp {nominal:,.0f}",
                    TIPS_KAT[kat],
                ),
            )

        self.lbl_info_rek.config(
            text=f"Budget Rp {total_budget:,.0f}  →  dialokasikan ke {len(ALOKASI_PERSEN)} kategori berdasarkan proporsi ideal traveling.",
            bootstyle="info",
        )

        # Perbandingan dengan data aktual
        self.tree_banding.delete(*self.tree_banding.get_children())
        if not data_pengeluaran:
            self.lbl_kesimpulan.config(
                text="ℹ️  Belum ada data aktual. Tambahkan pengeluaran di tab Data.",
                bootstyle="secondary",
            )
            self.set_status(
                f"Rekomendasi budget Rp {total_budget:,.0f} selesai dihitung."
            )
            return

        aktual = {}
        for item in data_pengeluaran:
            aktual[item["kategori"]] = aktual.get(item["kategori"], 0) + item["jumlah"]
        total_aktual = sum(aktual.values())

        for kat in KATEGORI_LIST:
            rek = rekomendasi.get(kat, 0)
            act = aktual.get(kat, 0)
            sisa = rek - act
            tanda = "+" if sisa >= 0 else ""
            if act == 0:
                status = "— Belum ada"
                tag = "netral"
            elif sisa >= 0:
                status = "✅  AMAN"
                tag = "aman"
            else:
                status = "⚠️  MELEBIHI"
                tag = "lebih"
            self.tree_banding.insert(
                "",
                END,
                values=(
                    kat,
                    f"Rp {rek:,.0f}",
                    f"Rp {act:,.0f}",
                    f"{tanda}Rp {sisa:,.0f}",
                    status,
                ),
                tags=(tag,),
            )

        self.tree_banding.tag_configure("aman", foreground="#16A34A")
        self.tree_banding.tag_configure("lebih", foreground="#DC2626")
        self.tree_banding.tag_configure("netral", foreground="#64748B")

        sisa_total = total_budget - total_aktual
        if sisa_total > 0:
            kes = f"✅  Budget masih sisa Rp {sisa_total:,.0f}. Bisa dialihkan ke kategori yang kurang atau ditabung."
            bs = "success"
        elif sisa_total == 0:
            kes = "✅  Budget pas! Pengeluaran tepat sesuai budget."
            bs = "success"
        else:
            over = [
                k for k in KATEGORI_LIST if aktual.get(k, 0) > rekomendasi.get(k, 0)
            ]
            kes = f"⚠️  Budget MELEBIHI Rp {abs(sisa_total):,.0f}! Pertimbangkan mengurangi: {', '.join(over)}."
            bs = "danger"

        self.lbl_kesimpulan.config(text=kes, bootstyle=bs)
        self.set_status(f"Rekomendasi budget Rp {total_budget:,.0f} selesai dihitung.")


# ENTRY POINT

if __name__ == "__main__":
    # Window ttkbootstrap dengan tema flatly (sesuai modul praktikum)
    app = ttk.Window(themename="flatly")
    AplikasiBudgetTravel(app)
    app.mainloop()
