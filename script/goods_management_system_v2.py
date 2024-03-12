import PySimpleGUI as sg
from enum import Enum
    
class LEND_BORROW():
    pass

class REGISTRATION():
    pass

class GMS_GUI(LEND_BORROW, REGISTRATION):
    #列挙型
    class PAGE(Enum):
        MENU_PAGE = 1
        SELECT_LAB_PAGE = 2

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
                break
            elif event == 'シャットダウン':
                self.runtime = False
                break
    
    #汎用性選択画面1
    #page_title = ページ名
    #page_explanation = 何を選択する画面化の説明文
    #name_list = 表示する名称の文字列リスト
    #button_list = (ボタン表示名、遷移先)
    #return_page = 1つ前のページ
    def General_purpose_selection_windows(
            self,
            page_title,
            page_explanation,
            name_list,
            button_list_0,
            button_list_1,
            button_list_2,
            return_page
    ):
        page = 0
        layout = [
            [sg.Text(page_title, font=self.biggest_char_font, justification='center')],
            [sg.Text('', font=self.smallest_cahr_font, justification='center', key='error_message')],
            [sg.Text(page_explanation, font=self.normal_cahr_font, justification='center')],
            [sg.Button(name_list[(3 * page) + 0], font=self.normal_cahr_font, button_color=('#000000', '#FFFFFF'), size=self.select_button_size, key='first_select')],
            [sg.Button(name_list[(3 * page) + 1], font=self.normal_cahr_font, button_color=('#000000', '#FFFFFF'), size=self.select_button_size, key='seccond_select')],
            [sg.Button(name_list[(3 * page) + 2], font=self.normal_cahr_font, button_color=('#000000', '#FFFFFF'), size=self.select_button_size, key='third_select')],
            [sg.Button(button_list_0[0], font=self.normal_cahr_font, key='button0'), sg.Button(button_list_1[0], font=self.normal_cahr_font, key='button1'), sg.Button(button_list_2[0], font=self.normal_cahr_font, key='button2')],
            [sg.Button('戻る', font=self.normal_cahr_font)]
        ]
        windows = sg.Window('Goods_management_system_v2(GMS)', layout, self.max_windows_size)
        while True:
            event, values = windows.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                self.runtime = False