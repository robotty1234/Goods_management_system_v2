# GOODS_MANAGEMENT_SYSTEM_v2
## 動作に必要な準備
- PySimpleGUI バージョン5未満(5以降はライセンス登録が必要になる)
  - Ubuntの場合
  ```
  pip install PySimpleGUI==4.60.5
  ```
  - Raspberry pi OSの場合
  ```
  pip install --break-system-packages PySimpleGUI==4.60.5
  ```
- PyQRCode
  - Ubuntの場合
  ```
  pip install PyQRCode
  ```
  -  Raspberry pi OSの場合
  ```
  pip install --break-system-packages PyQRCode
  ```
- pypng
  - Ubuntの場合
  ```
  pip install pypng
  ```
  -  Raspberry pi OSの場合
  ```
  pip install --break-system-packages pypng
  ```
- pandas
  - Ubuntの場合
  ```
  pip install pandas
  ```
  -  Raspberry pi OSの場合
  ```
  pip install --break-system-packages pandas
  ```
- nfcpy
  - Ubuntの場合
  ```
  sudo apt install libusb-dev python3-usb
  sudo pip3 install nfcpy
  ```
  -  Raspberry pi OSの場合
  ```
  sudo apt install libusb-dev python3-usb
  sudo pip3 install --break-system-packages nfcpy
  ```
- ImageTk(PIL)
  - Ubuntの場合
  ```
  sudo apt install python3-pil.imagetk
  sudo apt install python3-pil
  ```
  -  Raspberry pi OSの場合
  ```
  sudo apt install python3-pil.imagetk
  sudo apt install python3-pil
  ```
- pyzbar
  - Ubuntの場合
  ```
  sudo apt install libzbar0
  pip install pyzbar
  ```
  -  Raspberry pi OSの場合
  ```
  sudo apt install libzbar0
  pip install --break-system-packages pyzbar
  ```
- pymsteams
  - Ubuntの場合
  ```
  pip install pymsteams
  ```
  -  Raspberry pi OSの場合
  ```
  pip install --break-system-packages pymsteams
  ```
- opencv
  - Ubuntの場合
  ```
  pip install opencv-python
  ```
  -  Raspberry pi OSの場合 
  ```
  pip install --break-system-packages opencv-python
  ```
-pypng
  -Raspberry pi  OSの場合 
  ```
  sudo pip install --break-system-packages pypng
  ```
- カードリーダーRC-S380を使用するための設定(RC-S380を本体と接続しながら下記のコマンドを入力する)
```
  sudo sh -c 'echo SUBSYSTEM==\"usb\", ACTION==\"add\", ATTRS{idVendor}==\"054c\", ATTRS{idProduct}==\"06c1\", GROUP=\"plugdev\" >> /etc/udev/rules.d/nfcdev.rules'
  sudo udevadm control -R # then re-attach device
```
## 起動に必要なフォルダ
本フォルダ内に`data_tables`と`qr_codes`という名前のファルダを作成してください。(登録情報を保存するフォルダなのでgitの対象にしていません)
## 起動方法
本フォルダ内(Goods_management_system_v2)で下記のコマンドを実行する。
```
python3 -m script
```

