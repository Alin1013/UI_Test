import pytest
import os
import allure
from Common.AllurePretty import AllurePretty
from Pages.CreateFormPage import CreateFormPage  # 导入表单页面对象
from Config.Config import Config  # 导入配置
from Utils.read_yaml import ReadYaml  # 导入YAML读取工具


class TestCreateSampleForm:
    @pytest.mark.order(2)  # 登录用例之后执行
    @AllurePretty.AllurePretty_Warpper
    # 参数化：读取创建表单的测试数据
    @pytest.mark.parametrize(
        "CaseData",
        ReadYaml(os.path.join(Config.test_datas_dir, "TestCreateForm.yaml")).read()
    )
    def test_create_sample_form(self, logged_in_page, CaseData):
        page = logged_in_page
        # 导航到目标页面（如果当前不在目标页面）
        target_url = Config.Base_url + CaseData.get("url", "/recent")
        if page.url != target_url and "about:blank" in page.url:
            page.goto(target_url, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_load_state("networkidle", timeout=15000)
        
        create_form_page = CreateFormPage(page)
        current_url = page.url
        print(f"✅ 登录后当前页面：{current_url}")

        # 3. 执行创建表单操作（每个操作前等待元素，避免点击失败）
        try:
            # 点击创建按钮
            create_form_page.click_create_button()
            print("✅ 点击创建按钮成功")

            # 悬浮到表单按钮
            create_form_page.hover_hover_form_button()
            print("✅ 悬浮表单按钮成功")

            # 点击创建示例表单按钮
            create_form_page.click_create_sample_form_button()
            print("✅ 点击创建示例表单按钮成功")
        except Exception as e:
            raise Exception(f"❌ 表单创建操作失败，错误：{str(e)}")

        # 4. 优化截图（添加异常处理，避免截图失败导致用例报错）
        try:
            screenshot = page.screenshot(full_page=True)  # 截取全页
            allure.attach(
                screenshot,
                name=f"创建表单截图_{CaseData['用例标题']}",
                attachment_type=allure.attachment_type.PNG
            )
            print("✅ 截图已附加到Allure报告")
        except Exception as e:
            print(f"⚠️ 截图失败：{str(e)}")  # 仅打印不抛错，不阻断用例