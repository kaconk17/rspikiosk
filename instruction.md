# Instalasi
Menggunakan OS linux :

Jalankan **fdisk** untuk mempartisi SD card:

    fdisk /dev/sdX

Dalam **fdisk** prompt, hapus semua prtisi dan buat partisi baru:

ketik `o`. Perintah ini akan menghapus semua partisi dalam drive.

Ketik `p` Untuk menampilkan seluruh partisi. Pastikan tidak ada pertisi yang tersisa.


Ketik `n`, kemudian `p` untuk partisi primary, `1` untuk membuat pertisi pertama dalam drive, tekan `ENTER` untuk memilih sector pertama secara default,

ketikkan `+200M` untuk sector terakhir.


Ketik `t`, kemudian `c` untuk menjadikan prtisi pertama menjadi type W95 FAT32 (LBA).


Ketik `n`, kemudian `p` untuk partisi primary, `2` untuk partisi yang kedua dalam drive, dan kemudian tekan `ENTER` 2x untuk memilih sector pertama dan sector terakhir.


Tulis tabel partisi kedalam drive sekaligus exit dengan mengetikkan `w`.


Membuat dan mount filesystem FAT:

    mkfs.vfat /dev/sdX1
    mkdir boot
    mount /dev/sdX1 boot

Membuat dan mount filesystem ext4:

    mkfs.ext4 /dev/sdX2
    mkdir root
    mount /dev/sdX2 root

Download dan extract filesystem root (sebagai root, bukan via sudo):

    wget http://os.archlinuxarm.org/os/ArchLinuxARM-rpi-4-latest.tar.gz
    bsdtar -xpf ArchLinuxARM-rpi-4-latest.tar.gz -C root
    sync

Pindahkan file-file **boot** kedalam partisi pertama:

    mv root/boot/* boot

Unmount kedua partisi:

    umount boot root

Masukkan SD card kedalam Raspberry Pi, sambungkan kabel ethernet, dan pasang power 5V.

Gunakan serial console atau **SSH** pada IP address yang didapatkan Raspberry Pi.

Login menggunakan default user **alarm** dengan password **alarm**.

Password default untuk **root** adalah **root**.

Inisialisasi **pacman keyring** dan populate package Arch Linux ARM signing keys:

    pacman-key --init
    pacman-key --populate archlinuxarm
