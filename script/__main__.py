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