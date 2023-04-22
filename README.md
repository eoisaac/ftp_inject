# FTP Inject

## How to run

### Configure vsftpd server

1. Install vsftpd

    ```
    sudo apt install vsftpd
    ```

2. Configure the server

    ```
    sudo mv /etc/vsftpd.conf /etc/vsftpd.conf_orig
    ```

    1. Create a config file:

        ```
        sudo nano /etc/vsftpd.conf
        ```

    2. Copy the following base config

        ```
        listen=NO
        listen_ipv6=YES
        anonymous_enable=NO
        local_enable=YES
        write_enable=YES
        local_umask=022
        dirmessage_enable=YES
        use_localtime=YES
        xferlog_enable=YES
        connect_from_port_20=YES
        chroot_local_user=YES
        secure_chroot_dir=/var/run/vsftpd/empty
        pam_service_name=vsftpd
        rsa_cert_file=/etc/ssl/certs/ssl-cert-snakeoil.pem
        rsa_private_key_file=/etc/ssl/private/ssl-cert-snakeoil.key
        ssl_enable=NO
        pasv_enable=Yes
        pasv_min_port=10000
        pasv_max_port=10100
        allow_writeable_chroot=YES
        ```

3. Create an exception in UFW

    ```
    sudo ufw allow from any to any port 20,21,10000:10100 proto tcp
    ```

4. Restart the server to apply the changes:

    ```
    sudo systemctl restart vsftpd
    ```

### Create a FTP user

1. Create a new account

    ```
    sudo useradd -m <your_ftp_username>
    sudo passwd <your_ftp_username>
    ```

2. Check if everything's working

    ```
    sudo bash -c "echo FTP TESTING > /home/<your_ftp_username>/FTP-TEST"
    ```

### Run the code

1. Activate enviroment:

    ```
    source .venv/bin/activate
    ```

2. Install the dependencies

    ```
    pip install -r requirements.txt
    ```

3. Run

    ```
    python3 main.py -H localhost -c ./src/data/passwords.txt
    ```