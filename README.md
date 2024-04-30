# GOODS_MANAGEMENT_SYSTEM_v2
## 動作に必要な準備
- PySimpleGUI バージョン5未満(5以降はライセンス登録が必要になる)
  - Ubuntの場合
  ```
  pip install PySimpleGUI==4.60.5
  ```
- PyQRCode
  - Ubuntの場合
  ```
  pip install PyQRCode
  ```
- pypng
  - Ubuntの場合
  ```
  pip install pypng
  ```
- pandas
  - Ubuntの場合
  ```
  pip install pandas
  ```
- nfcpy
  - Ubuntの場合
  ```
  sudo apt install libusb-dev python3-usb
  sudo pip3 install nfcpy
  ```
- ImageTk(PIL)
  - Ubuntの場合
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
- pymsteams
  - Ubuntの場合
  ```
  pip install pymsteams
  ```
## 起動に必要なフォルダ
本フォルダ内に`data_tables`と`qr_codes`という名前のファルダを作成してください。(登録情報を保存するフォルダなのでgitの対象にしていません)
## 起動方法
本フォルダ内(Goods_management_system_v2)で下記のコマンドを実行する。
```
python3 -m script
```

