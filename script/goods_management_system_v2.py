import PySimpleGUI as sg
from enum import Enum
import os
import shutil
import csv
import pprint
import pyqrcode
import pandas
import time
import nfc
import cv2
from PIL import Image, ImageTk
from pyzbar.pyzbar import decode
import pymsteams
import png
    
class LEND_BORROW():
    #初期化
    def __init__(self):
        self.student_number = ''
        self.goods_name_list = []
        self.error_goods_name_list = []
        #Teamsと連携しているWebhookのURL
        self.send_to_tems_url = 'https://utokai.webhook.office.com/webhookb2/bdec44b3-374b-4b51-91d9-0c2310e85765@8283096f-bcce-44d0-8f54-e57aa84d1a22/IncomingWebhook/0bf4493eff1e412b966d583a6c869938/5f22c588-8faa-4953-9c40-60a6ce150147'
    
    #学生証読み込み
    def get_student_number(self, timeout):
        nfc_loop = True
        number = ''
        with nfc.ContactlessFrontend("usb")  as clf:
            start_time = time.time()
            tag = clf.connect(rdwr={'on-connect': lambda tag: False}, terminate=lambda: time.time() - start_time > 0.01)
            try:
                number = str(tag.dump())
                number = number.split('|')[9].split('.')[0]
                nfc_loop = False
            except:
                number = 'ERROR'
            #print(number)
        return number
    
    #QR読み込み
    def get_qr_code(self, frame):
        qr_code_texts = []
        for barcode in decode(frame):
            code_data = barcode.data.decode('utf-8')
            qr_code_texts.append(code_data)
        return qr_code_texts
    
    #情報の更新
    def update_info(self, goods_name, student_number):
        return_flug = False
        update_lab = goods_name.split('/')[0]
        #print('update_lab : ' + update_lab)
        update_category = goods_name.split('/')[1]
        #print('update_category : ' + update_category)
        update_goods = goods_name.split('/')[2]
        #print('update_goods : ' + update_goods)
        #情報の更新
        #ファイルパス
        current_directory = os.path.dirname(os.path.abspath(__file__))
        current_directory = current_directory.split('script')[0]
        path = os.path.join(current_directory, ('data_tables' + '/' + update_lab  + '/' + update_category + '/' + update_goods))
        csv_file_path = (path + '/' + update_goods) + '.csv'
        #csvファイルを取得
        goods_info = pandas.read_csv(csv_file_path).values.tolist()
        print(goods_info)
        #在庫状態を確認
        if goods_info[0][3] == 'x':
            #貸出者と操作者と同一人物か
            if goods_info[0][4] == student_number:
                goods_info[0][3] = 'o'
                goods_info[0][4] = '--------'
                return_flug = True
            else:
                return_flug = False
        else:
            goods_info[0][3] = 'x'
            goods_info[0][4] = student_number
        #上書き保存
        goods_list = [
            ['物品名','研究室', 'カテゴリー', '在庫', '貸出者'],
            goods_info[0]
        ]
        df = pandas.DataFrame(goods_list[1:], columns=goods_list[0])
        df.to_csv(csv_file_path, index=False)
        
        
class REGISTRATION():
    #初期化
    def __init__(self):
        self.select_lab = ''
        self.select_category = ''
        self.select_goods = ''
        self.add_goods_name = '' 
        self.code_scale = 5
        #物品フォルダを管理しているトップフォルダ名
        self.LAB_FOLDER = 'data_tables'
        #QRコードを管理しているトップフォルダ名
        self.QR_FOLDER = 'qr_codes'

    def get_lab_names(self, arrange = True):
        lab_names = self.get_folder_names(self.LAB_FOLDER, arrange)
        return lab_names
    
    def make_lab(self, lab_name):
        #物品フォルダ作成
        self.make_folder(self.LAB_FOLDER, lab_name)
        #QRコードフォルダ
        self.make_folder(self.QR_FOLDER, lab_name)

    def rename_lab(self, lab_name, lab_rename):
        #物品フォルダ作成
        self.rename_folder(self.LAB_FOLDER, lab_name, lab_rename)
        #QRコードフォルダ
        self.rename_folder(self.QR_FOLDER, lab_name, lab_rename)
        self.select_lab = lab_rename
        self.update_goods_info()

    def remove_lab(self, lab_name):
        #物品フォルダ作成
        self.remove_folder(self.LAB_FOLDER, lab_name)
        #QRコードフォルダ
        self.remove_folder(self.QR_FOLDER, lab_name)
        
    def get_category_names(self, arrange = True):
        category_names = self.get_folder_names(self.LAB_FOLDER + '/' + self.select_lab, arrange)
        return category_names
    
    def make_category(self, category_name):
        #物品フォルダ
        self.make_folder(self.LAB_FOLDER + '/' + self.select_lab, category_name)
        #QRコードフォルダ
        self.make_folder(self.QR_FOLDER+ '/' + self.select_lab, category_name)

    def rename_category(self, category_name, category_rename):
        #物品フォルダ
        self.rename_folder(self.LAB_FOLDER + '/' + self.select_lab, category_name, category_rename)
        #QRコードフォルダ
        self.rename_folder(self.QR_FOLDER + '/' + self.select_lab, category_name, category_rename)
        self.select_category = category_rename
        self.update_goods_info()

    def remove_category(self, category_name):
        #物品フォルダ
        self.remove_folder(self.LAB_FOLDER + '/' + self.select_lab, category_name)
        #QRコードフォルダ
        self.remove_folder(self.QR_FOLDER + '/' + self.select_lab, category_name)
        
    def get_goods_names(self, arrange = True):
        goods_names = self.get_folder_names(self.LAB_FOLDER + '/' + self.select_lab + '/' + self.select_category, arrange)
        return goods_names
    
    def make_goods(self, goods_name):
        #物品フォルダ
        self.make_folder(self.LAB_FOLDER + '/' + self.select_lab + '/' + self.select_category, goods_name)
                
    def remove_goods(self, goods_name):
        #物品フォルダ
        self.remove_folder(self.LAB_FOLDER + '/' + self.select_lab + '/' + self.select_category, goods_name)
        #QRコードフォルダ
        os.remove(self.QR_FOLDER + '/' + self.select_lab + '/' + self.select_category + '/' + goods_name + '.png')

    def get_folder_names(self, path, arrange = True):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        current_directory = current_directory.split('script')[0]
        data_list_path = os.path.join(current_directory, path)
        return_names = [
            f for f in os.listdir(data_list_path) if os.path.isdir(os.path.join(data_list_path, f))
        ]
        return_names.sort()
        if arrange == True:
            while len(return_names) % 3 != 0:
                return_names.append('')
            if len(return_names) == 0:
                for i in range(3):
                    return_names.append('')
        return return_names
    
    def add_new_goods_file(self, lab_name, category_name, goods_name):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        current_directory = current_directory.split('script')[0]
        path = os.path.join(current_directory, (self.LAB_FOLDER  + '/' + lab_name + '/' + category_name + '/' + goods_name))
        
        csv_path = (path + '/' + goods_name) + '.csv'
        goods_list = [
            ['物品名','研究室', 'カテゴリー', '在庫', '貸出者'],
            [goods_name, lab_name, category_name, 'o', '--------']
        ]
        df = pandas.DataFrame(goods_list[1:], columns=goods_list[0])
        df.to_csv(csv_path, index=False)
        
    def add_new_qr_code(self, lab_name, category_name, goods_name):
        code = pyqrcode.create(lab_name + '/' + category_name + '/' + goods_name, error='L', version=3, mode='binary')
        #物品フォルダに保存
        current_directory = os.path.dirname(os.path.abspath(__file__))
        current_directory = current_directory.split('script')[0]
        path = os.path.join(current_directory, (self.LAB_FOLDER  + '/' + lab_name + '/' + category_name + '/' + goods_name))
        code.png((path + '/' + goods_name+ '.png'), scale=self.code_scale, module_color=[0, 0, 0, 128], background=[255, 255, 255])
        #qrコードフォルダに保存
        current_directory = os.path.dirname(os.path.abspath(__file__))
        current_directory = current_directory.split('script')[0]
        path = os.path.join(current_directory, (self.QR_FOLDER  + '/' + lab_name + '/' + category_name))
        code.png((path + '/' + goods_name + '.png'), scale=self.code_scale, module_color=[0, 0, 0, 128], background=[255, 255, 255])
    
    def rename_goods(self, goods_name, goods_rename):
        path_goods  = self.LAB_FOLDER + '/' + self.select_lab + '/' + self.select_category
        path_qr  = self.QR_FOLDER + '/' + self.select_lab + '/' + self.select_category
        #物品フォルダ
        self.rename_folder(path_goods, goods_name, goods_rename)
        self.select_goods = goods_rename
        #物品ファイル
        current_directory = os.path.dirname(os.path.abspath(__file__))
        current_directory = current_directory.split('script')[0]
        normal_path_goods = os.path.join(current_directory, (path_goods + '/' + goods_rename))
        os.rename((normal_path_goods + '/' + goods_name + '.csv'), (normal_path_goods + '/' + goods_rename + '.csv'))
        #QRフォルダ
        normal_path_qr = os.path.join(current_directory, (path_qr))
        os.rename((normal_path_goods + '/' + goods_name + '.png'), (normal_path_goods + '/' + goods_rename + '.png'))
        os.rename((normal_path_qr + '/' + goods_name + '.png'), (normal_path_qr + '/' + goods_rename + '.png'))
        self.update_goods_info()
    
    def make_folder(self, path, name):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        current_directory = current_directory.split('script')[0]
        normal_path = os.path.join(current_directory, path)
        new_folder_paht = normal_path + '/' + name
        os.mkdir(new_folder_paht)

    def rename_folder(self, path, befor_name, after_name):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        current_directory = current_directory.split('script')[0]
        normal_path = os.path.join(current_directory, path)
        os.rename((normal_path + '/' + befor_name), (normal_path + '/' + after_name))

    def remove_folder(self, path, name):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        current_directory = current_directory.split('script')[0]
        normal_path = os.path.join(current_directory, path)
        remove_folder_paht = normal_path + '/' + name
        shutil.rmtree(remove_folder_paht)
        
    def update_goods_info(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        current_directory = current_directory.split('script')[0]
        #csvファイル
        befor_select_lab = self.select_lab
        befor_select_category = self.select_category
        befor_select_goods = self.select_goods
        print(self.get_lab_names(False))
        for lab in self.get_lab_names(False):
            self.select_lab = lab
            for category in self.get_category_names(False):
                self.select_category = category
                for goods in self.get_goods_names(False):
                    self.select_goods = goods
                    #元情報を保存
                    path = os.path.join(current_directory, (self.LAB_FOLDER  + '/' + self.select_lab + '/' + self.select_category + '/' + self.select_goods))
                    csv_file_path = (path + '/' + goods) + '.csv'
                    goods_info = pandas.read_csv(csv_file_path).values.tolist()
                    print(goods_info)
                    #物品名の変更
                    goods_info[0][0] = goods
                    #研究室名の変更
                    goods_info[0][1] = lab
                    #カテゴリー名の変更
                    goods_info[0][2] = category
                    #上書き保存
                    goods_list = [
                        ['物品名','研究室', 'カテゴリー', '在庫', '貸出者'],
                        goods_info[0]
                    ]
                    df = pandas.DataFrame(goods_list[1:], columns=goods_list[0])
                    df.to_csv(csv_file_path, index=False)
                    
        #qr_code
        for lab in self.get_lab_names(False):
            self.select_lab = lab
            for category in self.get_category_names(False):
                self.select_category = category
                for goods in self.get_goods_names(False):
                    self.select_goods = goods
                    #元情報を保存
                    path_goods = os.path.join(current_directory, (self.LAB_FOLDER  + '/' + lab + '/' + category + '/' + goods))
                    path_qr = os.path.join(current_directory, (self.QR_FOLDER  + '/' + lab + '/' + category))
                    #以前のQRコードを削除
                    os.remove(path_goods + '/' + goods + '.png')
                    os.remove(path_qr + '/' + goods + '.png')
                    #新たにQRコードを作成
                    code = pyqrcode.create(lab + '/' + category + '/' + goods, error='L', version=3, mode='binary')
                    #上書き保存
                    code.png((path_goods + '/' + goods + '.png'), scale=self.code_scale, module_color=[0, 0, 0, 128], background=[255, 255, 255])
                    code.png((path_qr + '/' + goods + '.png'), scale=self.code_scale, module_color=[0, 0, 0, 128], background=[255, 255, 255])
        self.select_lab = befor_select_lab
        self.select_category = befor_select_category
        self.select_goods = befor_select_goods
    
class GMS_GUI(LEND_BORROW, REGISTRATION):
    #列挙型
    class PAGE(Enum):
        MENU_PAGE = 1
        SELECT_LAB_PAGE = 2
        ADD_LAB_PAGE = 3
        RENAME_LAB_PAGE = 4
        REMOVE_LAB_PAGE = 5
        SELECT_CATEGORY_PAGE = 6
        ADD_CATEGORY_PAGE = 7
        RENAME_CATEGORY_PAGE = 8
        REMOVE_CATEGORY_PAGE = 9
        SELECT_GOODS_PAGE = 10
        ADD_GOODS_PAGE_0 = 11
        RENAME_GOODS_PAGE = 12
        REMOVE_GOODS_PAGE = 13
        ADD_GOODS_PAGE_1 = 14
        INPUT_NUMBER = 15
        HOW_TO_USE = 16
        INPUT_CODE = 17
        UPDATE_GOODS = 18
        SENT_COMPLETED = 19

    #初期化
    def __init__(self):
        self.max_windows_size = (123, 78)
        self.biggest_char_font = ('Arial, 40') 
        self.bigger_cahr_font = ('Arial, 30') 
        self.normal_cahr_font = ('Arial, 20')
        self.smallest_cahr_font = ('Arial, 15')
        self.select_button_size = (50, 1)
        self.category_max = 3
        self.runtime = True
        self.page = GMS_GUI.PAGE.MENU_PAGE
        self.lend_borrow = LEND_BORROW()
        self.registration = REGISTRATION()
        self.web_camera = cv2.VideoCapture(0)
    
    #初期メニュー画面
    def menu_windows(self):
        layout = [ 
            [sg.Text('', font=self.biggest_char_font, justification='center')],
            [sg.Text('物品管理システム', font = self.biggest_char_font, justification='center')],
            [sg.Text('', font=self.biggest_char_font, justification='center')],
            [sg.Button('貸出・返却', font=self.normal_cahr_font, button_color=('#0000CD', '#B0E0E6')), sg.Button('物品登録追加・削除', font=self.normal_cahr_font, button_color=('#006400', '#AFEEEE')), sg.Button('シャットダウン', font=self.normal_cahr_font, button_color=('#FF0000', '#FFFFFF'))]
        ]
        windows = sg.Window('Goods_management_system_v2(GMS)', layout, self.max_windows_size)
        while True:
            event, values = windows.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                self.runtime = False
                break
            elif event == '貸出・返却':
                self.runtime = True
                self.page = GMS_GUI.PAGE.INPUT_NUMBER
                break
            elif event == '物品登録追加・削除':
                self.runtime = True
                self.page = GMS_GUI.PAGE.SELECT_LAB_PAGE
                break
            elif event == 'シャットダウン':
                self.runtime = False
                break
        windows.close()
        return self.runtime
    
    #学生証読み込み処理画面
    def input_number_windows(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        current_directory = current_directory.split('script')[0]
        left_img_path = os.path.join(current_directory, 'img/ic_card_befor.png')
        right_img_path = os.path.join(current_directory, 'img/ic_card_after.png')
        layout = [ 
            [sg.Text('学生証読み込み', font = self.biggest_char_font, justification='center')],
            [sg.Text('学生証を以下の図のようにおいてください', font = self.normal_cahr_font, justification='center')],
            [sg.Image(filename=left_img_path), sg.Image(filename=right_img_path)],
            [sg.Button('戻る', font=self.normal_cahr_font)]
        ]
        windows = sg.Window('Goods_management_system_v2(GMS)', layout, self.max_windows_size)
        out_time = 0.01
        while True:
            event, values = windows.read(timeout=out_time)
            if event == sg.WIN_CLOSED or event == 'Cancel':
                self.runtime = False
                break
            elif event == '戻る':
                self.runtime = True
                self.page = GMS_GUI.PAGE.MENU_PAGE
                break
            else:
                self.lend_borrow.student_number = self.lend_borrow.get_student_number(out_time)
                if self.lend_borrow.student_number != 'ERROR':
                    self.runtime = True
                    self.page = GMS_GUI.PAGE.HOW_TO_USE
                    break
        windows.close()
        return self.runtime
    
    #動作確認画面   
    def how_to_use_windows(self):
        self.lend_borrow.goods_name_list = ['', '', '']
        current_directory = os.path.dirname(os.path.abspath(__file__))
        current_directory = current_directory.split('script')[0]
        reader_img_path = os.path.join(current_directory, 'img/QR_code_read.png')
        out_img_path = os.path.join(current_directory, 'img/ic_card_out.png')
        layout = [ 
            [sg.Text('使用方法', font = self.biggest_char_font, justification='center')],
            [sg.Text('1.返品・返却する物品に貼り付けたQRコード', font = self.normal_cahr_font, justification='center')],
            [sg.Text('をカメラで読み取る', font = self.normal_cahr_font, justification='center')],
            [sg.Text('2.QRコードを読み取り終わったら学生証を取る', font = self.normal_cahr_font, justification='center')],
            [sg.Image(filename=reader_img_path), sg.Image(filename=out_img_path)],
            [sg.Button('確認完了', font=self.normal_cahr_font)]
        ]
        windows = sg.Window('Goods_management_system_v2(GMS)', layout, self.max_windows_size)
        while True:
            event, values = windows.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                self.runtime = False
                break
            elif event == '確認完了':
                self.runtime = True
                self.page = GMS_GUI.PAGE.INPUT_CODE
                break
        windows.close()
        return self.runtime
    
    #QRコード読み込み
    def input_qr_code(self):
        page_num = 0
        goods_list = 0
        layout = [ 
            [sg.Text('QRコードを読み込み', font = self.biggest_char_font, justification='center')],
            [sg.Text('読み取った物品', font = self.normal_cahr_font, justification='center')],
            [sg.Button(self.lend_borrow.goods_name_list[(3 * page_num) + 0], font = self.normal_cahr_font, size=self.select_button_size, key='first_select')],
            [sg.Button(self.lend_borrow.goods_name_list[(3 * page_num) + 1], font = self.normal_cahr_font, size=self.select_button_size, key='seccond_select')],
            [sg.Button(self.lend_borrow.goods_name_list[(3 * page_num) + 2], font = self.normal_cahr_font, size=self.select_button_size, key='third_select')],
            [sg.Text(str(page_num + 1), font=self.normal_cahr_font, justification='center', key='number'), sg.Text('/' + str(int(len(self.lend_borrow.goods_name_list) / 3)), font=self.normal_cahr_font, justification='center', key = 'max_number'), sg.Button('前', font=self.normal_cahr_font), sg.Button('後',font=self.normal_cahr_font)],
            [sg.Image(key='camera_img')]
        ]
        windows = sg.Window('Goods_management_system_v2(GMS)', layout, self.max_windows_size)
        while True:
            event, values = windows.read(timeout=0.5)
            if event == sg.WIN_CLOSED or event == 'Cancel':
                self.runtime = False
                break
            elif event == '前':
                if page_num > 0:
                    page_num = page_num - 1
                else:
                    page_num = int((len(self.lend_borrow.goods_name_list) / 3) - 1)
                windows['first_select'].update(self.lend_borrow.goods_name_list[(3 * page_num) + 0])
                windows['seccond_select'].update(self.lend_borrow.goods_name_list[(3 * page_num) + 1])
                windows['third_select'].update(self.lend_borrow.goods_name_list[(3 * page_num) + 2])
                windows['number'].update(str(page_num + 1))
            elif event == '後':
                if page_num < ((len(self.lend_borrow.goods_name_list) / 3) - 1):
                    page_num = page_num + 1
                else:
                    page_num = 0
                windows['first_select'].update(self.lend_borrow.goods_name_list[(3 * page_num) + 0])
                windows['seccond_select'].update(self.lend_borrow.goods_name_list[(3 * page_num) + 1])
                windows['third_select'].update(self.lend_borrow.goods_name_list[(3 * page_num) + 2])
                windows['number'].update(str(page_num + 1))
            else:
                #カメラ画像更新
                ret, frame = self.web_camera.read()
                if ret == True:
                    img_frame = cv2.resize(frame, dsize=None, fx=0.3 , fy=0.3)
                    img_frame = cv2.imencode('.png', img_frame)[1].tobytes() 
                    windows['camera_img'].update(data=img_frame)
                    #QRコード読み取り
                    qr_codese = self.lend_borrow.get_qr_code(frame)
                    for qr_code_text in qr_codese:
                        #print(qr_code_text)
                        #読み取った物品名を登録
                        #既に読み込んだ物品は当録しない
                        if (qr_code_text in self.lend_borrow.goods_name_list) == False:
                            if (goods_list % 3) != 0 or goods_list == 0:
                                self.lend_borrow.goods_name_list[goods_list] = qr_code_text
                                goods_list = goods_list + 1
                            else:
                                for i in range(3):
                                    self.lend_borrow.goods_name_list.append('')
                                self.lend_borrow.goods_name_list[goods_list] = qr_code_text
                                goods_list = goods_list + 1
                            #読み取り物品名更新
                            page_num = int(len(self.lend_borrow.goods_name_list) / 3) - 1
                            windows['first_select'].update(self.lend_borrow.goods_name_list[(3 * page_num) + 0])
                            windows['seccond_select'].update(self.lend_borrow.goods_name_list[(3 * page_num) + 1])
                            windows['third_select'].update(self.lend_borrow.goods_name_list[(3 * page_num) + 2]) 
                            windows['max_number'].update('/' + str(int(len(self.lend_borrow.goods_name_list) / 3)))
                            windows['number'].update(str(page_num + 1))
                    #学生証確認
                    target=self.lend_borrow.get_student_number(0.1)
                    if target == 'ERROR':
                        self.runtime = True
                        self.page = GMS_GUI.PAGE.UPDATE_GOODS
                        #空白部分を削除
                        index = len(self.lend_borrow.goods_name_list) - 1
                        while self.lend_borrow.goods_name_list[index] == '':
                            self.lend_borrow.goods_name_list.pop(index)
                            index = index - 1
                        break                    
                        
        windows.close()
        return self.runtime    
    
    #物品情報送信
    def update_goods_windows(self):
        all_goods_number = len(self.lend_borrow.goods_name_list)
        update_goods_number = 0
        self.lend_borrow.error_goods_name_list = []
        layout = [ 
            [sg.Text('物品情報', font = self.biggest_char_font, justification='center')],
            [sg.Text('学籍番号:' + str(self.lend_borrow.student_number), font = self.normal_cahr_font, justification='center')],
            [sg.Text('', font = self.normal_cahr_font, justification='center', key='doing_task')],
        ]
        windows = sg.Window('Goods_management_system_v2(GMS)', layout, self.max_windows_size)
        #物品情報の更新
        while True:
            event, values = windows.read(timeout=0.1)
            if event == sg.WIN_CLOSED or event == 'Cancel':
                self.runtime = False
                break
            elif update_goods_number < all_goods_number:
                windows['doing_task'].update('物品情報の更新['+ str(update_goods_number) + '/' + str(all_goods_number) + ']')
                #情報更新
                result = self.lend_borrow.update_info(self.lend_borrow.goods_name_list[update_goods_number], self.lend_borrow.student_number)
                #エラーが発生した物品名を保存
                if result == False:
                    self.lend_borrow.error_goods_name_list.append(self.lend_borrow.goods_name_list[update_goods_number])
                update_goods_number = update_goods_number + 1
            elif update_goods_number >= all_goods_number:
                #情報を送信
                lab_lists = self.registration.get_lab_names(False)
                for l in lab_lists:
                    self.registration.select_lab = l
                    sent_goods_infos = ['|物品名|研究室|カテゴリー|現在の在庫状況|貸出者|']
                    category_lists = self.registration.get_category_names(False)
                    for c in category_lists:
                        self.registration.select_category = c
                        goods_lists = self.registration.get_goods_names(False)
                        for g in goods_lists:
                            #物品の在庫状況を読み取り
                            #ファイルパス
                            self.registration.select_goods = g
                            current_directory = os.path.dirname(os.path.abspath(__file__))
                            current_directory = current_directory.split('script')[0]
                            path = os.path.join(current_directory, ('data_tables' + '/' + self.registration.select_lab  + '/' + self.registration.select_category + '/' + self.registration.select_goods))
                            csv_file_path = (path + '/' + self.registration.select_goods) + '.csv'
                            #csvファイルを取得
                            goods_info = pandas.read_csv(csv_file_path).values.tolist()
                            goods_str = '|'
                            for s in goods_info[0]:
                                goods_str = goods_str + s + '|'
                            goods_str = goods_str + '<br>'
                            sent_goods_infos.append(goods_str)
                    #teams = pymsteams.connectorcard(self.lend_borrow.send_to_tems_url)
                    #teams.title("最新の在庫情報")
                    #teams.text(list_texts)
                    #teams.send()
                    print('Title : ' + self.registration.select_lab + 'の最新物品情報')
                    for ps in sent_goods_infos:
                        print(ps)
                    print('')
                #更新終了
                self.page = GMS_GUI.PAGE.SENT_COMPLETED
                self.runtime = True
                break
        windows.close()
        return self.runtime
            
    #送信完了画面
    def sent_completed_windows(self):
        layout = [ 
            [sg.Text('送信完了', font = self.biggest_char_font, justification='center')],
            [sg.Text('下記に表示された物品の情報更新はできませんでした', font = self.normal_cahr_font, justification='center')],
            [sg.Text('エラーが起きた理由として「QRコードが未登録」、「貸出者と返却者が異なる」などが考えられます', font = self.smallest_cahr_font, justification='center')],
            [sg.Text(self.lend_borrow.error_goods_name_list, font = self.normal_cahr_font, justification='center')],
            [sg.Button('OK', font=self.normal_cahr_font)]
        ]
        windows = sg.Window('Goods_management_system_v2(GMS)', layout, self.max_windows_size)
        while True:
            event, values = windows.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                self.runtime = False
                break
            elif event == 'OK':
                self.runtime = True
                self.page = GMS_GUI.PAGE.MENU_PAGE
                break
        windows.close()
        return self.runtime
        
    #物品登録追加・削除画面(研究室選択)
    def select_lab_windows(self):
        #保持研究室名を初期化
        self.registration.select_lab = ''
        lab_names = self.registration.get_lab_names()
        self.runtime, self.registration.select_lab = self.general_purpose_selection_windows_0(
            '研究室を選択',
            '研究室を選択してください',
            lab_names,
            ('新たな研究室を追加', GMS_GUI.PAGE.ADD_LAB_PAGE),
            ('研究室名を変更', GMS_GUI.PAGE.RENAME_LAB_PAGE),
            ('既存の研究室を削除', GMS_GUI.PAGE.REMOVE_LAB_PAGE),
            GMS_GUI.PAGE.SELECT_CATEGORY_PAGE,
            GMS_GUI.PAGE.MENU_PAGE
        )
        return self.runtime
    
    #研究室追加
    def add_lab_windows(self):
        lab_names = self.registration.get_lab_names()
        self.runtime, new_lab_name = self.general_purpose_input_windows_0(
            '研究室の追加',
            '追加する研究室名を入力してください',
            lab_names, 
            GMS_GUI.PAGE.SELECT_LAB_PAGE
        )
        if self.page == GMS_GUI.PAGE.ADD_LAB_PAGE:
            if new_lab_name != '':
                self.registration.make_lab(new_lab_name)
            self.page = GMS_GUI.PAGE.SELECT_LAB_PAGE
        return self.runtime
    
    #研究室名変更
    def rename_lab_windows(self):
        lab_names = self.registration.get_lab_names()
        self.runtime, self.registration.select_lab = self.general_purpose_selection_windows_1(
            '研究室名の変更',
            '変更する研究室名を選択してください',
            lab_names, 
            GMS_GUI.PAGE.SELECT_LAB_PAGE
        )
        if self.page == GMS_GUI.PAGE.RENAME_LAB_PAGE:
            self.runtime, new_lab_name = self.general_purpose_input_windows_0(
                '研究室名の変更',
                (self.registration.select_lab + 'の変更名を入力してください'),
                lab_names, 
                GMS_GUI.PAGE.SELECT_LAB_PAGE
            )
            if self.page == GMS_GUI.PAGE.RENAME_LAB_PAGE:
                self.registration.rename_lab(self.registration.select_lab, new_lab_name)
                self.page = GMS_GUI.PAGE.SELECT_LAB_PAGE
        return self.runtime
    
    #研究室削除
    def remove_lab_windows(self):
        lab_names = self.registration.get_lab_names()
        self.runtime, self.registration.select_lab = self.general_purpose_selection_windows_1(
            '研究室の削除',
            '削除する研究室名を選択してください',
            lab_names, 
            GMS_GUI.PAGE.SELECT_LAB_PAGE
        )
        if self.page == GMS_GUI.PAGE.REMOVE_LAB_PAGE:
            self.runtime, cheack = self.general_confirm_input_windows_0(
                '確認！',
                self.registration.select_lab + 'を削除してよろしいでしょうか',
            )
            if self.page == GMS_GUI.PAGE.REMOVE_LAB_PAGE:
                if cheack == True:
                    self.registration.remove_lab(self.registration.select_lab)
                self.page = GMS_GUI.PAGE.SELECT_LAB_PAGE
        return self.runtime
    
    #物品登録追加・削除画面(カテゴリー選択)
    def select_category_windows(self):
        #保持カテゴリー名を初期化
        self.registration.select_category = ''
        category_names = self.registration.get_category_names()
        self.runtime, self.registration.select_category = self.general_purpose_selection_windows_0(
            'カテゴリーを選択',
            'カテゴリーを選択してください',
            category_names,
            ('新たなカテゴリーを追加', GMS_GUI.PAGE.ADD_CATEGORY_PAGE),
            ('カテゴリー名を変更', GMS_GUI.PAGE.RENAME_CATEGORY_PAGE),
            ('既存のカテゴリーを削除', GMS_GUI.PAGE.REMOVE_CATEGORY_PAGE),
            GMS_GUI.PAGE.SELECT_GOODS_PAGE,
            GMS_GUI.PAGE.SELECT_LAB_PAGE
        )
        return self.runtime
    
    #カテゴリー追加
    def add_category_windows(self):
        category_names = self.registration.get_category_names()
        self.runtime, new_category_name = self.general_purpose_input_windows_0(
            'カテゴリーの追加',
            '追加するカテゴリー名を入力してください',
            category_names, 
            GMS_GUI.PAGE.SELECT_CATEGORY_PAGE
        )
        if self.page == GMS_GUI.PAGE.ADD_CATEGORY_PAGE:
            if new_category_name != '':
                self.registration.make_category(new_category_name)
            self.page = GMS_GUI.PAGE.SELECT_CATEGORY_PAGE
        return self.runtime
    
    #カテゴリー名変更
    def rename_category_windows(self):
        category_names = self.registration.get_category_names()
        self.runtime, self.registration.select_category = self.general_purpose_selection_windows_1(
            'カテゴリー名の変更',
            '変更するカテゴリー名を選択してください',
            category_names, 
            GMS_GUI.PAGE.SELECT_CATEGORY_PAGE
        )
        if self.page == GMS_GUI.PAGE.RENAME_CATEGORY_PAGE:
            self.runtime, new_category_name = self.general_purpose_input_windows_0(
                'カテゴリー名の変更',
                (self.registration.select_category + 'の変更名を入力してください'),
                category_names, 
                GMS_GUI.PAGE.SELECT_CATEGORY_PAGE
            )
            if self.page == GMS_GUI.PAGE.RENAME_CATEGORY_PAGE:
                self.registration.rename_category(self.registration.select_category, new_category_name)
                self.page = GMS_GUI.PAGE.SELECT_CATEGORY_PAGE
        return self.runtime
    
    #カテゴリー削除
    def remove_category_windows(self):
        category_names = self.registration.get_category_names()
        self.runtime, self.registration.select_category = self.general_purpose_selection_windows_1(
            'カテゴリーの削除',
            '削除するカテゴリー名を選択してください',
            category_names, 
            GMS_GUI.PAGE.SELECT_CATEGORY_PAGE
        )
        if self.page == GMS_GUI.PAGE.REMOVE_CATEGORY_PAGE:
            self.runtime, cheack = self.general_confirm_input_windows_0(
                '確認！',
                self.registration.select_category + 'を削除してよろしいでしょうか',
            )
            if self.page == GMS_GUI.PAGE.REMOVE_CATEGORY_PAGE:
                if cheack == True:
                    self.registration.remove_category(self.registration.select_category)
                self.page = GMS_GUI.PAGE.SELECT_CATEGORY_PAGE
        return self.runtime
    
    #物品登録追加・削除画面(物品選択)
    def select_goods_windows(self):
        #保持物品名を初期化
        self.registration.select_goods = ''
        self.runtime, self.registration.select_goods = self.general_purpose_selection_windows_2(
            '物品情報の編集',
            '編集操作を選択してください',
            ('新たな物品情報を追加', GMS_GUI.PAGE.ADD_GOODS_PAGE_0),
            ('既存の物品情報を変更', GMS_GUI.PAGE.RENAME_GOODS_PAGE),
            ('既存の物品情報を削除', GMS_GUI.PAGE.REMOVE_GOODS_PAGE),
            GMS_GUI.PAGE.SELECT_CATEGORY_PAGE
        )
        return self.runtime
    
    #物品の追加_0
    def add_goods_windows_0(self):
        self.registration.add_goods_name = '' 
        goods_names = self.registration.get_goods_names()
        self.runtime, self.registration.add_goods_name = self.general_purpose_input_windows_0(
            '物品の追加',
            '追加するカテゴリー名を入力してください',
            goods_names, 
            GMS_GUI.PAGE.SELECT_GOODS_PAGE
        )
        if self.registration.add_goods_name != '':
            self.registration.make_goods(self.registration.add_goods_name)
            self.page = GMS_GUI.PAGE.ADD_GOODS_PAGE_1
        return self.runtime
    
    #物品の追加_1
    def add_goods_windows_1(self):
        self.registration.add_new_goods_file(self.registration.select_lab, self.registration.select_category, self.registration.add_goods_name)
        self.registration.add_new_qr_code(self.registration.select_lab, self.registration.select_category, self.registration.add_goods_name)
        self.general_message_windows_0(
           self.registration.add_goods_name + 'を追加しました',
           GMS_GUI.PAGE.SELECT_GOODS_PAGE
        )
    
    #物品情報の変更
    def rename_goods_windows(self):
        goods_names = self.registration.get_goods_names()
        self.runtime, self.registration.select_goods = self.general_purpose_selection_windows_1(
            '物品名の変更',
            '変更する物品名を選択してください',
            goods_names, 
            GMS_GUI.PAGE.SELECT_GOODS_PAGE
        )
        self.runtime, new_goods_name = self.general_purpose_input_windows_0(
            '物品名の変更',
            (self.registration.select_goods + 'の変更名を入力してください'),
            goods_names, 
            GMS_GUI.PAGE.SELECT_GOODS_PAGE
        )
        self.registration.rename_goods(self.registration.select_goods, new_goods_name)
        self.page = GMS_GUI.PAGE.SELECT_GOODS_PAGE
        return self.runtime
    
    #物品削除
    def remove_goods_windows(self):
        category_names = self.registration.get_goods_names()
        self.runtime, self.registration.select_goods = self.general_purpose_selection_windows_1(
            '物品の削除',
            '削除する物品名を選択してください',
            category_names, 
            GMS_GUI.PAGE.SELECT_GOODS_PAGE
        )
        if self.page == GMS_GUI.PAGE.REMOVE_GOODS_PAGE:
            self.runtime, cheack = self.general_confirm_input_windows_0(
                '確認！',
                self.registration.select_goods + 'を削除してよろしいでしょうか',
            )
            if self.page == GMS_GUI.PAGE.REMOVE_GOODS_PAGE:
                if cheack == True:
                    self.registration.remove_goods(self.registration.select_goods)
                self.page = GMS_GUI.PAGE.SELECT_GOODS_PAGE
        return self.runtime
        
    
    #汎用性選択画面0
    #page_title = ページ名
    #page_explanation = 何を選択する画面化の説明文
    #name_list = 表示する名称の文字列リスト
    #button_list_0~2 = (ボタン表示名、遷移先)
    #nect_page = 選択項目を選んだ際に次に遷移するページ
    #return_page = 1つ前のページ
    def general_purpose_selection_windows_0(
        self,
        page_title,
        page_explanation,
        name_list,
        button_list_0,
        button_list_1,
        button_list_2,
        next_page,
        return_page
    ):
        page_num = 0
        return_str = ''
        layout = [
            [sg.Text(page_title, font=self.biggest_char_font, justification='center')],
            [sg.Text(page_explanation, font=self.normal_cahr_font, justification='center')],
            [sg.Button(name_list[(3 * page_num) + 0], font=self.normal_cahr_font, button_color=('#000000', '#FFFFFF'), size=self.select_button_size, key='first_select')],
            [sg.Button(name_list[(3 * page_num) + 1], font=self.normal_cahr_font, button_color=('#000000', '#FFFFFF'), size=self.select_button_size, key='seccond_select')],
            [sg.Button(name_list[(3 * page_num) + 2], font=self.normal_cahr_font, button_color=('#000000', '#FFFFFF'), size=self.select_button_size, key='third_select')],
            [sg.Text(str(page_num + 1), font=self.normal_cahr_font, justification='center', key='number'), sg.Text('/' + str(int(len(name_list) / 3)), font=self.normal_cahr_font, justification='center'), sg.Button('前', font=self.normal_cahr_font), sg.Button('後',font=self.normal_cahr_font)],
            [sg.Button(button_list_0[0], font=self.normal_cahr_font, key='button0'), sg.Button(button_list_1[0], font=self.normal_cahr_font, key='button1'), sg.Button(button_list_2[0], font=self.normal_cahr_font, key='button2')],
            [sg.Button('戻る', font=self.normal_cahr_font)]
        ]
        windows = sg.Window('Goods_management_system_v2(GMS)', layout, self.max_windows_size)
        while True:
            event, values = windows.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                self.runtime = False
                break
            elif event == '前':
                if page_num > 0:
                    page_num = page_num - 1
                else:
                    page_num = int((len(name_list) / 3) - 1)
                windows['first_select'].update(name_list[(3 * page_num) + 0])
                windows['seccond_select'].update(name_list[(3 * page_num) + 1])
                windows['third_select'].update(name_list[(3 * page_num) + 2])
                windows['number'].update(str(page_num + 1))
            elif event == '後':
                if page_num < ((len(name_list) / 3) - 1):
                    page_num = page_num + 1
                else:
                    page_num = 0
                windows['first_select'].update(name_list[(3 * page_num) + 0])
                windows['seccond_select'].update(name_list[(3 * page_num) + 1])
                windows['third_select'].update(name_list[(3 * page_num) + 2])
                windows['number'].update(str(page_num + 1))
            elif event == 'first_select':
                if name_list[(3 * page_num) + 0] != '':
                    return_str = name_list[(3 * page_num) + 0]
                    self.runtime = True
                    self.page = next_page
                    break
            elif event == 'seccond_select':
                if name_list[(3 * page_num) + 1] != '':
                    return_str = name_list[(3 * page_num) + 1]
                    self.runtime = True
                    self.page = next_page
                    break
            elif event == 'third_select':
                if name_list[(3 * page_num) + 2] != '':
                    return_str = name_list[(3 * page_num) + 2]
                    self.runtime = True
                    self.page = next_page
                    break
            elif event == 'button0':
                print(button_list_0[1])
                self.page = button_list_0[1]
                self.runtime = True
                break
            elif event == 'button1':
                self.page = button_list_1[1]
                self.runtime = True
                break
            elif event == 'button2':
                self.page = button_list_2[1]
                self.runtime = True
                break
            elif event == '戻る':
                self.page = return_page
                self.runtime = True
                break
        windows.close()
        return self.runtime, return_str
    
    #汎用性選択画面1
    #page_title = ページ名
    #page_explanation = 何を選択する画面化の説明文
    #name_list = 表示する名称の文字列リスト
    #return_page = 1つ前のページ
    def general_purpose_selection_windows_1(
        self,
        page_title,
        page_explanation,
        name_list,
        return_page
    ):
        page_num = 0
        return_str = ''
        layout = [
            [sg.Text(page_title, font=self.biggest_char_font, justification='center')],
            [sg.Text(page_explanation, font=self.normal_cahr_font, justification='center')],
            [sg.Button(name_list[(3 * page_num) + 0], font=self.normal_cahr_font, button_color=('#000000', '#FFFFFF'), size=self.select_button_size, key='first_select')],
            [sg.Button(name_list[(3 * page_num) + 1], font=self.normal_cahr_font, button_color=('#000000', '#FFFFFF'), size=self.select_button_size, key='seccond_select')],
            [sg.Button(name_list[(3 * page_num) + 2], font=self.normal_cahr_font, button_color=('#000000', '#FFFFFF'), size=self.select_button_size, key='third_select')],
            [sg.Text(str(page_num + 1), font=self.normal_cahr_font, justification='center', key='number'), sg.Text('/' + str(int(len(name_list) / 3)), font=self.normal_cahr_font, justification='center'), sg.Button('前', font=self.normal_cahr_font), sg.Button('後',font=self.normal_cahr_font)],
            [sg.Button('戻る', font=self.normal_cahr_font)]
        ]
        windows = sg.Window('Goods_management_system_v2(GMS)', layout, self.max_windows_size)
        while True:
            event, values = windows.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                self.runtime = False
                break
            elif event == '前':
                if page_num > 0:
                    page_num = page_num - 1
                else:
                    page_num = int((len(name_list) / 3) - 1)
                windows['first_select'].update(name_list[(3 * page_num) + 0])
                windows['seccond_select'].update(name_list[(3 * page_num) + 1])
                windows['third_select'].update(name_list[(3 * page_num) + 2])
                windows['number'].update(str(page_num + 1))
            elif event == '後':
                if page_num < ((len(name_list) / 3) - 1):
                    page_num = page_num + 1
                else:
                    page_num = 0
                windows['first_select'].update(name_list[(3 * page_num) + 0])
                windows['seccond_select'].update(name_list[(3 * page_num) + 1])
                windows['third_select'].update(name_list[(3 * page_num) + 2])
                windows['number'].update(str(page_num + 1))
            elif event == '戻る':
                self.page = return_page
                self.runtime == True
                break
            elif event == 'first_select':
                if name_list[(3 * page_num) + 0] != '':
                    return_str = name_list[(3 * page_num) + 0]
                    self.runtime = True
                    break
            elif event == 'seccond_select':
                if name_list[(3 * page_num) + 1] != '':
                    return_str = name_list[(3 * page_num) + 1]
                    self.runtime = True
                    break
            elif event == 'third_select':
                if name_list[(3 * page_num) + 2] != '':
                    return_str = name_list[(3 * page_num) + 2]
                    self.runtime = True
                    break
        windows.close()
        return self.runtime, return_str
    
    #汎用性選択画面2
    #page_title = ページ名
    #page_explanation = 何を選択する画面化の説明文
    #button_list_0~2 = (ボタン表示名、遷移先)
    #return_page = 1つ前のページ
    def general_purpose_selection_windows_2(
        self,
        page_title,
        page_explanation,
        button_list_0,
        button_list_1,
        button_list_2,
        return_page
    ):
        return_str = ''
        layout = [
            [sg.Text(page_title, font=self.biggest_char_font, justification='center')],
            [sg.Text(page_explanation, font=self.normal_cahr_font, justification='center')],
            [sg.Button(button_list_0[0], font=self.normal_cahr_font, key='button0'), sg.Button(button_list_1[0], font=self.normal_cahr_font, key='button1'), sg.Button(button_list_2[0], font=self.normal_cahr_font, key='button2')],
            [sg.Button('戻る', font=self.normal_cahr_font)]
        ]
        windows = sg.Window('Goods_management_system_v2(GMS)', layout, self.max_windows_size)
        while True:
            event, values = windows.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                self.runtime = False
                break
            elif event == 'button0':
                print(button_list_0[1])
                self.page = button_list_0[1]
                self.runtime = True
                break
            elif event == 'button1':
                self.page = button_list_1[1]
                self.runtime = True
                break
            elif event == 'button2':
                self.page = button_list_2[1]
                self.runtime = True
                break
            elif event == '戻る':
                self.page = return_page
                self.runtime = True
                break
        windows.close()
        return self.runtime, return_str
    
    #汎用入力画面0
    #page_title = ページ名
    #page_explanation = 何を選択する画面化の説明文
    #name_list = 表示する名称の文字列リスト
    #return_page = 1つ前のページ
    def general_purpose_input_windows_0(
        self,
        page_title,
        page_explanation,
        name_list,
        return_page
    ):
        return_str = ''
        layout = [
            [sg.Text(page_title, font=self.biggest_char_font, justification='center')],
            [sg.Text(page_explanation, font=self.normal_cahr_font, justification='center')],
            [sg.InputText(key='input_str', font=self.bigger_cahr_font, size=(self.max_windows_size[1] - 40, 1))],
            [sg.Text('', font=self.smallest_cahr_font, justification='center', key='error_mes')],
            [sg.Button('決定', font=self.normal_cahr_font)],
            [sg.Button('戻る', font=self.normal_cahr_font)]
        ]
        windows = sg.Window('Goods_management_system_v2(GMS)', layout, self.max_windows_size)
        while True:
            event, values = windows.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                self.runtime = False
                break
            elif event == '決定':
                if values['input_str'] == '':
                    windows['error_mes'].update('空白です')
                elif ('/' in values['input_str']) == True:
                    windows['error_mes'].update('「/」は使用できません')
                else:
                    equuality = False
                    for a in name_list:
                        if a == values['input_str']:
                            equuality = True
                    if equuality == True:
                        windows['error_mes'].update('同じ名前が既に登録されています')
                    else:
                        return_str = values['input_str']
                        break
            elif event == '戻る':
                self.page = return_page
                self.runtime = True
                break
        windows.close()
        return [self.runtime, return_str]
    
    #汎用確認画面0
    #page_title = ページ名
    #page_explanation = 何を選択する画面化の説明文
    def general_confirm_input_windows_0(
        self,
        page_title,
        page_explanation
    ):
        confirm = False
        layout = [
            [sg.Text(page_title, font=self.biggest_char_font, justification='center')],
            [sg.Text(page_explanation, font=self.normal_cahr_font, justification='center')],
            [sg.Button('はい', font=self.normal_cahr_font), sg.Button('いいえ', font=self.normal_cahr_font)]
        ]
        windows = sg.Window('Goods_management_system_v2(GMS)', layout, self.max_windows_size)
        while True:
            event, values = windows.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                self.runtime = False
                break
            elif event == 'はい':
                confirm = True
                self.runtime = True
                break
            elif event == 'いいえ':
                self.runtime = True
                break
        windows.close()
        return [self.runtime, confirm]
    
    #汎用メッセージ画面0
    #message=メッセージ
    #next_page=次の遷移先
    def general_message_windows_0(
        self,
        message,
        next_page
    ):
        layout = [
            [sg.Text(message, font=self.bigger_cahr_font, justification='center')],
            [sg.Button('OK', font=self.normal_cahr_font)]
        ]
        windows = sg.Window('Goods_management_system_v2(GMS)', layout, self.max_windows_size)
        while True:
            event, values = windows.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                self.runtime = False
                break
            elif event == 'OK':
                self.page = next_page
                self.runtime = True
                break
        windows.close()
        return self.runtime
    
    
