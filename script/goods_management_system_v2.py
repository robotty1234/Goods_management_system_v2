import PySimpleGUI as sg
from enum import Enum
import os
import shutil
import csv
    
class LEND_BORROW():
    pass

class REGISTRATION():
    #初期化
    def __init__(self):
        pass

    def get_lab_names(self):
        lab_names = self.get_folder_names('data_tables')
        return lab_names
    
    def make_lab(self, lab_name):
        self.make_folder('data_tables', lab_name)

    def get_folder_names(self, path):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        current_directory = current_directory.split('script')[0]
        data_list_path = os.path.join(current_directory, path)
        return_names = [
            f for f in os.listdir(data_list_path) if os.path.isdir(os.path.join(data_list_path, f))
        ]
        return_names.sort()
        while len(return_names) % 3 != 0:
            return_names.append('')
        if len(return_names) == 0:
            for i in range(3):
                return_names.append('')
        return return_names
    
    def make_folder(self, path, name):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        current_directory = current_directory.split('script')[0]
        normal_path = os.path.join(current_directory, path)
        new_folder_paht = normal_path + '/' + name
        os.mkdir(new_folder_paht)

class GMS_GUI(LEND_BORROW, REGISTRATION):
    #列挙型
    class PAGE(Enum):
        MENU_PAGE = 1
        SELECT_LAB_PAGE = 2
        ADD_LAB_PAGE = 3
        RENAME_LAB_PAGE = 4
        REMOVE_LAB_PAGE = 5

    #初期化
    def __init__(self):
        self.max_windows_size = (123, 78)
        self.biggest_char_font = ('Arial, 40') 
        self.normal_cahr_font = ('Arial, 20')
        self.smallest_cahr_font = ('Arial, 15')
        self.select_button_size = (50, 1)
        self.category_max = 3
        self.runtime = True
        self.page = GMS_GUI.PAGE.MENU_PAGE
        self.registration = REGISTRATION()
    
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

    #物品登録追加・削除画面(研究室選択)
    def select_lab_windows(self):
        lab_names = self.registration.get_lab_names()
        self.runtime = self.general_purpose_selection_windows(
            '研究室を選択',
            '研究室を選択してください',
            lab_names,
            ('新たな研究室を追加', GMS_GUI.PAGE.ADD_LAB_PAGE),
            ('研究室名を変更', GMS_GUI.PAGE.RENAME_LAB_PAGE),
            ('既存の研究室を削除', GMS_GUI.PAGE.REMOVE_LAB_PAGE),
            GMS_GUI.PAGE.MENU_PAGE
        )
        return self.runtime
    
    #研究室追加
    def add_lab_windows(self):
        lab_names = self.registration.get_lab_names()
        self.runtime, new_lab_name = self.general_purpose_input_windows(
            '研究室の追加',
            '追加する研究室名を入力してください',
            lab_names, 
            GMS_GUI.PAGE.SELECT_LAB_PAGE
        )
        if new_lab_name != '':
            self.registration.make_lab(new_lab_name)
        self.page = GMS_GUI.PAGE.SELECT_LAB_PAGE
        return self.runtime
    
    #汎用性選択画面1
    #page_title = ページ名
    #page_explanation = 何を選択する画面化の説明文
    #name_list = 表示する名称の文字列リスト
    #button_list_0~2 = (ボタン表示名、遷移先)
    #return_page = 1つ前のページ
    def general_purpose_selection_windows(
        self,
        page_title,
        page_explanation,
        name_list,
        button_list_0,
        button_list_1,
        button_list_2,
        return_page
    ):
        page_num = 0
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
            elif event == 'button0':
                print(button_list_0[1])
                self.page = button_list_0[1]
                self.runtime == True
                break
            elif event == 'button1':
                self.page = button_list_1[1]
                self.runtime == True
                break
            elif event == 'button2':
                self.page = button_list_2[1]
                self.runtime == True
                break
            elif event == '戻る':
                self.page = return_page
                self.runtime == True
                break
        windows.close()
        return self.runtime
    
    #汎用入力画面1
    #page_title = ページ名
    #page_explanation = 何を選択する画面化の説明文
    #name_list = 表示する名称の文字列リスト
    #return_page = 1つ前のページ
    def general_purpose_input_windows(
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
            [sg.InputText(key='input_str')],
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
                self.runtime == True
                break
        windows.close()
        return [self.runtime, return_str]
