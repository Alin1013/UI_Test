import pytest
import os
import allure
from Common.AllurePretty import AllurePretty
from Pages.CreateModulesPage import CreateModulesPage  # 导入表单页面对象
from Config.Config import Config  # 导入配置
from Utils.read_yaml import ReadYaml  # 导入YAML读取工具


class TestCreateSampleForm:
    @pytest.mark.order(2)  # 登录用例之后执行
    def test_create_all_modules(self, logged_in_page):
        """
        创建所有模块的完整流程：
        1. 点击create_button
        2. 创建folder（填充ui_测试），点击save，截图
        3. 在folder里面创建每个组件，填充标题，返回，截图
        """
        page = logged_in_page
        
        # 读取所有测试数据
        test_data_list = ReadYaml(os.path.join(Config.test_datas_dir, "TestCreateModules.yaml")).read()
        
        # 使用第一个用例的url来导航（如果存在）
        if test_data_list and len(test_data_list) > 0:
            first_case = test_data_list[0]
            target_url = Config.Base_url + first_case.get("url", "/recent")
            
            # 导航到目标页面（如果当前不在目标页面）
            if page.url != target_url and "about:blank" in page.url:
                page.goto(target_url, wait_until="domcontentloaded", timeout=30000)
                page.wait_for_load_state("networkidle", timeout=15000)
        
        # 创建页面对象
        create_form_page = CreateModulesPage(page)
        current_url = page.url
        print(f"✅ 登录后当前页面：{current_url}")
        
        # 设置Allure报告信息（使用第一个用例的信息）
        if test_data_list and len(test_data_list) > 0:
            first_case = test_data_list[0]
            allure.dynamic.feature("创建模块")
            allure.dynamic.story("创建所有模块")
            allure.dynamic.title(f"创建所有模块_完整流程")
            allure.dynamic.description("创建folder并在其中创建所有组件")
        
        # 执行完整流程：创建folder并创建所有组件
        try:
            create_form_page.create_all_modules(test_data_list)
            print("✅ 所有模块创建完成")
        except Exception as e:
            print(f"❌ 创建模块失败：{str(e)}")
            raise