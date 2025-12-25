import allure, os, re
import pytest
from playwright.sync_api import expect
from Pages.LoginPage.LoginPage import LoginPage
from Utils.read_yaml import ReadYaml
from Common.AllurePretty import AllurePretty
from Config.Config import Config


class TestLogin:
    test_data=ReadYaml(os.path.join(Config.test_datas_dir,"TestCase.yml")).read()
    #验证数据是否读取成功
    print(f"参数化用例数据：{test_data}")

    @pytest.mark.run(order=1)
    @AllurePretty.AllurePretty_Warpper
    @pytest.mark.parametrize("CaseData",ReadYaml(os.path.join(Config.test_datas_dir,"TestCase.yml")).read())
    def test_login(self,page,CaseData):
        new_page=LoginPage(page)
        AllurePretty(page,CaseData).AllurePretty()
        new_page.goto_login_page(CaseData["url"])
        new_page.fill_username(CaseData["账号"])
        new_page.fill_password(CaseData["密码"])
        new_page.click_login_button()
        #判断是否登陆成功
        if "登录成功" in CaseData.get("用例标题",""):
            expect(new_page.page).not_to_have_url(re.compile(r".*/login"),timeout=15000)
        else:
            expect(new_page.page).to_have_url(re.compile(r".*/login"),timeout=10000)