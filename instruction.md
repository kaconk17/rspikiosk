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

## Merubah default User dan Merubah Password root

Untuk merubah default user dan merubah password gunakan perintah:

    usermod -l new_username old_username
    passwd username
    usermod -d /home/new_username -m new_username

Untuk merubah password root menggunakan perintah:

    passwd

## Memberi akses sudo untuk user

Install paket **sudo**:

    pacman -S sudo

Edit file config yang ada di `/etc/sudoers` dengan menggunakan perintah:

    EDITOR=nano visudo

Dalam config file temukan baris text `root ALL=(ALL) ALL` dan tambahkan dibawahnya:

`new_user ALL=(ALL) ALL`

## Merubah nama hostname

Untuk mengganti nama hostname gunakan perintah:

    hostnamectl set-hostname New_Hostname

## Install AUR Helper

Install **git** dan **base-devel** dengan perintah:

    sudo pacman -S git base-devel

Install **yay** sebagai AUR Helper:

    git clone https://aur.archlinux.org/yay.git
    cd yay
    makepkg -si

## Setting timezone & ntp

Aktifkan ntp agar waktu pada system selalu update:

    sudo timedatectl set-ntp true

Rubah setting zona waktu sesuai lokasi:

    sudo timedatectl set-timezone Asia/Jakarta

## Install Window Manager

Untuk dapat menjalankan Raspberry sebagai KIOSK mode diperlukan Window manager, install window manager dengan perintah:

    sudo pacman -S xorg i3 xorg-xinit ttf-dejavu

## Membuat user Auto login

Dalam system KIOSK tidak memerlukan login user untuk bisa menjalankan system, sehingga harus dibuatkan configurasi agar user kita bisa auto login tanpa memerlukan password.

Buat file config dalam systemd menggunakan perintah:

    sudo mkdir /etc/systemd/system/getty@tty1.service.d
    sudo nano /etc/systemd/system/getty@tty1.service.d/override.conf

Kemudian masukkan dalam file **override.conf** :

    [Service]
    ExecStart=
    ExecStart=-/usr/bin/agetty --autologin new_user --noclear %I $TERM

## Menjalankan firefox dalam KIOSK Mode

Dalam KIOSK system ini menggunakan browser firefox, sehingga harus install dulu firefox:

    sudo pacman -S firefox

Buatkan script untuk menjalankan window manager & forefox dalam mode KIOSK:

    nano startkiosk.sh

Masukkan script dalam file **startkiosk.sh** dengan script berikut:

    #!/bin/sh
    xset -dpms      # disable DPMS (Energy Star) features.
    xset s off      # disable screen saver
    xset s noblank  # don't blank the video device
    i3 & # starts the WM
    xterm &         # launches a helpful terminal
    firefox --kiosk --noerrdialogs --disable-pinch --check-for-update-interval=604800 http://yourwebappaddress

Jalankan script secara otomatis menggunakan **.bash_profile**, edit bash_profile seperti berikut:

    nano .bash_profile

Rubah isi bash_profile seperti berikut:

    # ~/.bash_profile

    [[ -f ~/.bashrc ]] && . ~/.bashrc
    [[ -z $DISPLAY && $XDG_VTNR -eq 1 ]] && xinit ./startkiosk.sh

Jika ukuran layar kurang pas bisa dirubah settingan pada boot config.txt:

    sudo nano /boot/config.txt

Kemudian tambahkan text berikut:

    hdmi_group=2
    hdmi_mode=85

## Menjalankan python flask server untuk keperluan shutdown

Untuk bisa menggunakan GPIO Pin dengan python diperlukan install paket berikut:

    yay -S python-nanopi-gpio-git
    yay -S python-adafruit-gpio

Buat script python dalam folder `/home/new_user` dengan nama **app.py** dengan isi sesuai sample file app.py.

Instal python pip:
    
    sudo pacman -S python-pip

Install semua python package yang diperlukan sesuai daftar dalam file **requirements.txt** dengan cara:

    sudo pip install -r requirements.txt

Jalankan flask app.py sebagai service:

    sudo nano /etc/systemd/system/myscript.service

Kemudian masukkan script berikut:

    [Unit]
    Description=Script

    [Service]
    ExecStart=sudo python /home/new_user/app.py
    RemainAfterExit=true

    [Install]
    WantedBy=multi-user.target

Jalankan script sebagai service sehingga otomatis jalan saat system start:

    sudo systemctl start myscript.service
    sudo systemctl enable myscript.service
