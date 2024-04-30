from . import goods_management_system_v2 as gms

if __name__=='__main__':
    gms_obj = gms.GMS_GUI()
    while gms_obj.runtime == True:
        if gms_obj.page == gms_obj.PAGE.MENU_PAGE:
            gms_obj.menu_windows()
        elif gms_obj.page == gms_obj.PAGE.SELECT_LAB_PAGE:
            gms_obj.select_lab_windows()
        elif gms_obj.page == gms_obj.PAGE.ADD_LAB_PAGE:
            gms_obj.add_lab_windows()
        elif gms_obj.page == gms_obj.PAGE.RENAME_LAB_PAGE:
            gms_obj.rename_lab_windows()
        elif gms_obj.page == gms_obj.PAGE.REMOVE_LAB_PAGE:
            gms_obj.remove_lab_windows()
        elif gms_obj.page == gms_obj.PAGE.SELECT_CATEGORY_PAGE:
            gms_obj.select_category_windows()
        elif gms_obj.page == gms_obj.PAGE.ADD_CATEGORY_PAGE:
            gms_obj.add_category_windows()
        elif gms_obj.page == gms_obj.PAGE.RENAME_CATEGORY_PAGE:
            gms_obj.rename_category_windows()
        elif gms_obj.page == gms_obj.PAGE.REMOVE_CATEGORY_PAGE:
            gms_obj.remove_category_windows()
        elif gms_obj.page == gms_obj.PAGE.SELECT_GOODS_PAGE:
            gms_obj.select_goods_windows()
        elif gms_obj.page == gms_obj.PAGE.ADD_GOODS_PAGE_0:
            gms_obj.add_goods_windows_0()
        elif gms_obj.page == gms_obj.PAGE.ADD_GOODS_PAGE_1:
            gms_obj.add_goods_windows_1()
        elif gms_obj.page == gms_obj.PAGE.RENAME_GOODS_PAGE:
            gms_obj.rename_goods_windows()
        elif gms_obj.page == gms_obj.PAGE.REMOVE_GOODS_PAGE:
            gms_obj.remove_goods_windows()
        elif gms_obj.page == gms_obj.PAGE.INPUT_NUMBER:
            gms_obj.input_number_windows()
        elif gms_obj.page == gms_obj.PAGE.HOW_TO_USE:
            gms_obj.how_to_use_windows()
        elif gms_obj.page == gms_obj.PAGE.INPUT_CODE:
            gms_obj.input_qr_code()
        elif gms_obj.page == gms_obj.PAGE.UPDATE_GOODS:
            gms_obj.update_goods_windows()
        elif gms_obj.page == gms_obj.PAGE.SENT_COMPLETED:
             gms_obj.sent_completed_windows()