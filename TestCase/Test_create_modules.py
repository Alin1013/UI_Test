import pytest
import os
import allure
from Common.AllurePretty import AllurePretty
from Pages.CreateModulesPage import CreateModulesPage  # 导入表单页面对象
from Config.Config import Config  # 导入配置
from Utils.read_yaml import ReadYaml  # 导入YAML读取工具


class TestCreateModules:
    @pytest.mark.order(2)
    def test_create_folder(self,page):
        new_page=CreateModulesPage(page)
        new_page.create_folder_and_save("ui_测试")

    @pytest.mark.order(3)  # 登录用例之后执行
    def test_create_word(self,page):
        new_page=CreateModulesPage(page)
        new_page.create_word("创建文档")

    @pytest.mark.order(4)
    def test_create_traditional_word(self,page):
        new_page=CreateModulesPage(page)
        new_page.create_traditional_word("创建传统文档")

    @pytest.mark.order(5)
    def test_create_excel(self,page):
        new_page=CreateModulesPage(page)
        new_page.create_excel("创建专业表格")

    @pytest.mark.order(6)
    def test_create_use_excel(self,page):
        new_page=CreateModulesPage(page)
        new_page.create_use_excel("创建应用表格")

    @pytest.mark.order(7)
    def test_create_ppt(self,page):
        new_page=CreateModulesPage(page)
        new_page.create_ppt("创建幻灯片")
