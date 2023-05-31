# Instalasi



## Memberi akses sudo untuk user

Install paket **sudo**:

    apt install sudo

Tambahkan user kedalam group sudo:

    usermod -aG sudo newuser




## Install Window Manager

Untuk dapat menjalankan debian sebagai KIOSK mode diperlukan Window manager, install window manager dengan perintah:

    sudo apt install xorg i3

## Membuat user Auto login

Dalam system KIOSK tidak memerlukan login user untuk bisa menjalankan system, sehingga harus dibuatkan configurasi agar user kita bisa auto login tanpa memerlukan password.

Edit file config dalam systemd menggunakan perintah:

    sudo nano /lib/systemd/system/getty@.service

Kemudian rubah pada bagian ExecStart :

    [Service]
    ExecStart=-/sbin/agetty --noclear -a newuser %I $TERM

Tambah kan user kedalam group tty:

`sudo usermod -aG tty newuser`

Edit file `/etc/X11/Xwrapper.config` :

```
allowed_users=anybody
needs_root_rights=yes
```

## Menjalankan chromium dalam KIOSK Mode

Dalam KIOSK system ini menggunakan browser chromium, sehingga harus install dulu chromium:

    sudo apt install chromium xterm

Buatkan script untuk menjalankan window manager & chromium dalam mode KIOSK:

    nano startkiosk.sh

Masukkan script dalam file **startkiosk.sh** dengan script berikut:

    #!/bin/sh
    xset -dpms      # disable DPMS (Energy Star) features.
    xset s off      # disable screen saver
    xset s noblank  # don't blank the video device
    i3 & # starts the WM
    xterm &         # launches a helpful terminal
    chromium --kiosk --noerrdialogs --disable-pinch --check-for-update-interval=604800 http://yourwebappaddress

Jalankan script secara otomatis menggunakan **.bash_profile**, edit bash_profile seperti berikut:

    nano .bash_profile

Rubah isi bash_profile seperti berikut:

    # ~/.bash_profile

    [[ -f ~/.bashrc ]] && . ~/.bashrc
    [[ -z $DISPLAY && $XDG_VTNR -eq 1 ]] && xinit ./startkiosk.sh

## Menjalankan python flask server untuk keperluan shutdown

Buat script python dalam folder `/home/new_user` dengan nama **app.py** dengan isi sesuai sample file app.py.

install python pip:

`sudo apt install python3-pip`

Install semua python package yang diperlukan sesuai daftar dalam file **requirements.txt** dengan cara:

    sudo pip install -r requirements.txt

Jalankan flask app.py sebagai service:

    sudo nano /etc/systemd/system/myscript.service

Kemudian masukkan script berikut:

    [Unit]
    Description=Script

    [Service]
    ExecStart=sudo python3 /home/new_user/app.py
    RemainAfterExit=true

    [Install]
    WantedBy=multi-user.target

Jalankan script sebagai service sehingga otomatis jalan saat system start:

    sudo systemctl start myscript.service
    sudo systemctl enable myscript.service
