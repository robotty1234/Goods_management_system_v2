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
        self.select_lab = ''
        self.select_category = ''
        self.select_goods = ''
        self.add_goods_name = '' 
        #物品フォルダを管理しているトップフォルダ名
        self.LAB_FOLDER = 'data_tables'

    def get_lab_names(self):
        lab_names = self.get_folder_names(self.LAB_FOLDER)
        return lab_names
    
    def make_lab(self, lab_name):
        self.make_folder(self.LAB_FOLDER, lab_name)

    def rename_lab(self, lab_name, lab_rename):
        self.rename_folder(self.LAB_FOLDER, lab_name, lab_rename)

    def remove_lab(self, lab_name):
        self.remove_folder(self.LAB_FOLDER, lab_name)
        
    def get_category_names(self):
        category_names = self.get_folder_names(self.LAB_FOLDER + '/' + self.select_lab)
        return category_names
    
    def make_category(self, category_name):
        self.make_folder(self.LAB_FOLDER + '/' + self.select_lab, category_name)

    def rename_category(self, category_name, category_rename):
        self.rename_folder(self.LAB_FOLDER + '/' + self.select_lab, category_name, category_rename)

    def remove_category(self, category_name):
        self.remove_folder(self.LAB_FOLDER + '/' + self.select_lab, category_name)
        
    def get_goods_names(self):
        goods_names = self.get_folder_names(self.LAB_FOLDER + '/' + self.select_lab + '/' + self.select_category)
        return goods_names
    
    def make_goods(self, goods_name):
        self.make_folder(self.LAB_FOLDER + '/' + self.select_lab + '/' + self.select_category, goods_name)

    def rename_goods(self, goods_name, goods_rename):
        self.rename_folder(self.LAB_FOLDER + '/' + self.select_lab + '/' + self.select_category, goods_name, goods_rename)

    def remove_goods(self, goods_name):
        self.remove_folder(self.LAB_FOLDER + '/' + self.select_lab + '/' + self.select_category, goods_name)

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
        RENAME_GOODS_PAGE_0 = 12
        REMOVE_GOODS_PAGE = 13
        ADD_GOODS_PAGE_1 = 14

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
    def select_category_windows(self):
        #保持物品名を初期化
        self.registration.select_goods = ''
        self.runtime, self.registration.select_goods = self.general_purpose_selection_windows_2(
            '物品情報の編集',
            '編集操作を選択してください',
            ('新たな物品情報を追加', GMS_GUI.PAGE.ADD_GOODS_PAGE_0),
            ('既存の物品情報を変更', GMS_GUI.PAGE.RENAME_GOODS_PAGE_0),
            ('既存の物品情報を削除', GMS_GUI.PAGE.REMOVE_GOODS_PAGE),
            GMS_GUI.PAGE.SELECT_CATEGORY_PAGE
        )
        return self.runtime
    
    #物品の追加_0
    def add_goods_windows_0(self):
        self.registration.add_goods_name = '' 
        goods_names = self.registration.get_goods_names()
        self.runtime, new_goods_name = self.general_purpose_input_windows_0(
            '物品の追加',
            '追加するカテゴリー名を入力してください',
            goods_names, 
            GMS_GUI.PAGE.SELECT_GOODS_PAGE
        )
        if new_goods_name != '':
            self.registration.make_category(new_goods_name)
        self.page = GMS_GUI.PAGE.ADD_GOODS_PAGE_1
        return self.runtime
    
    #物品の追加_1
    def add_goods_windows_1(self):
        pass
    
    #物品情報の変更0
    def rename_goods_windows_0(self):
        category_names = self.registration.get_category_names()
        self.runtime, self.registration.select_category = self.general_purpose_selection_windows_1(
            'カテゴリー名の変更',
            '変更するカテゴリー名を選択してください',
            category_names, 
            GMS_GUI.PAGE.SELECT_CATEGORY_PAGE
        )
        self.runtime, new_category_name = self.general_purpose_input_windows_0(
            'カテゴリー名の変更',
            (self.registration.select_category + 'の変更名を入力してください'),
            category_names, 
            GMS_GUI.PAGE.SELECT_CATEGORY_PAGE
        )
        self.registration.rename_category(self.registration.select_category, new_category_name)
        self.page = GMS_GUI.PAGE.SELECT_CATEGORY_PAGE
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
                return_str = name_list[(3 * page_num) + 0]
                self.runtime = True
                self.page = next_page
                break
            elif event == 'seccond_select':
                return_str = name_list[(3 * page_num) + 1]
                self.runtime = True
                self.page = next_page
                break
            elif event == 'third_select':
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
                return_str = name_list[(3 * page_num) + 0]
                self.runtime = True
                break
            elif event == 'seccond_select':
                return_str = name_list[(3 * page_num) + 1]
                self.runtime = True
                break
            elif event == 'third_select':
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
