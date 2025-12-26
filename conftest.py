# conftest.py（项目根目录）
import pytest
import os
import uuid
import allure
from playwright.sync_api import sync_playwright, expect, Browser, BrowserContext, Page
from Config.Config import Config

# 初始化必要目录
Config.create_directories()
os.makedirs("tracing_files", exist_ok=True)
AUTH_PATH = os.path.join(Config.auth_dir, "auth.json")


# -------------------------- 核心修复：自定义session级context和page --------------------------
@pytest.fixture(scope="session")
def browser():
    """会话级浏览器（全局唯一）"""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            channel=Config.browser if hasattr(Config, 'browser') else "chrome",
            args=['--start-maximized']
        )
        yield browser
        browser.close()


@pytest.fixture(scope="session")
def context(browser: Browser):
    """会话级上下文（保存登录态，全局唯一）"""
    context = browser.new_context(no_viewport=True)
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield context
    context.tracing.stop()
    context.close()


# 全局变量，用于存储已登录的page（延迟初始化）
_logged_in_page_instance = None

@pytest.fixture(scope="session")
def logged_in_page(context: BrowserContext):
    """会话级已登录page（复用登录态）
    注意：此fixture使用延迟初始化，只在第一次被请求时才创建page
    如果context中已有登录态（cookies），直接使用；否则执行登录
    """
    global _logged_in_page_instance
    if _logged_in_page_instance is None:
        from Pages.LoginPage.LoginPage import LoginPage
        from Utils.read_yaml import ReadYaml
        import re
        
        # 延迟初始化：只在第一次被请求时创建page
        page = context.new_page()
        
        # 检查context中是否已有登录态（通过检查cookies数量）
        # 如果context中已有cookies，说明登录测试用例已经执行过，登录态已保存
        cookies = context.cookies()
        has_auth_cookies = len(cookies) > 0
        
        if not has_auth_cookies:
            # 如果没有登录态，执行登录
            print("⚠️ context中未检测到登录态，执行自动登录...")
            login_page = LoginPage(page)
            login_data = ReadYaml(os.path.join(Config.test_datas_dir, "TestLogin.yaml")).read()
            login_case = next((case for case in login_data if case["用例标题"] == "账号密码正确，登录成功"), None)
            if not login_case:
                raise Exception("未找到登录成功的测试用例！")
            
            # 执行登录
            login_page.goto_login_page(login_case["url"])
            login_page.fill_username(login_case["账号"])
            login_page.fill_password(login_case["密码"])
            login_page.click_login_button()
            
            # 验证登录成功
            page.wait_for_load_state("networkidle", timeout=15000)
            expect(page).not_to_have_url(re.compile(r".*/login"), timeout=15000)
            print(f"✅ 自动登录成功，当前URL：{page.url}")
        else:
            print(f"✅ 检测到context中已有登录态，复用登录态")
            # 导航到默认页面（登录后的首页），确保页面已加载
            default_url = Config.Base_url + "/recent"
            try:
                page.goto(default_url, wait_until="domcontentloaded", timeout=30000)
                page.wait_for_load_state("networkidle", timeout=15000)
                print(f"✅ 已导航到默认页面：{page.url}")
            except Exception as e:
                print(f"⚠️ 导航到默认页面失败：{e}，当前URL：{page.url}")
        
        _logged_in_page_instance = page
    
    yield _logged_in_page_instance
    # 注意：session结束时，context会自动关闭，page也会被关闭


# -------------------------- 兼容原有逻辑：function级page --------------------------
@pytest.fixture(scope="function")
def page(request, context: BrowserContext):
    """函数级page fixture
    - 登录测试用例（order=1）：使用共享context的新page，登录态会被保存到context中
    - 其他测试用例：延迟获取logged_in_page（避免在登录测试前执行自动登录）
    """
    # 检查是否是登录测试用例
    is_login_test = False
    for marker in request.node.iter_markers("order"):
        if marker.args and marker.args[0] == 1:
            is_login_test = True
            break
    
    if is_login_test:
        # 登录测试用例使用共享context的新page（登录态会保存到context中）
        page = context.new_page()
        yield page
        # 保存录制文件
        case_data = request.node.funcargs.get("CaseData", {})
        case_title = case_data.get("用例标题", "未命名标题")
        safe_title = "".join([c for c in case_title if c not in r'\/:*?"<>|'])
        try:
            trace_filename = f"trace_{safe_title}_{uuid.uuid4().hex[:8]}.zip"
            trace_path = os.path.join("tracing_files", trace_filename)
            context.tracing.stop(path=trace_path)
            context.tracing.start(screenshots=True, snapshots=True, sources=True)  # 重启追踪
            print(f"录制文件已保存:{trace_path}")
        except Exception as e:
            print(f"录制文件保存失败：{e}")
        page.close()
    else:
        # 其他测试用例：延迟获取logged_in_page（此时登录测试应该已经执行完毕）
        # 通过request.getfixturevalue延迟获取，避免在登录测试前执行
        logged_in_page = request.getfixturevalue("logged_in_page")
        page = logged_in_page
        yield page
        # 保存录制文件
        case_data = request.node.funcargs.get("CaseData", {})
        case_title = case_data.get("用例标题", "未命名标题")
        safe_title = "".join([c for c in case_title if c not in r'\/:*?"<>|'])
        try:
            trace_filename = f"trace_{safe_title}_{uuid.uuid4().hex[:8]}.zip"
            trace_path = os.path.join("tracing_files", trace_filename)
            page.context.tracing.stop(path=trace_path)
            page.context.tracing.start(screenshots=True, snapshots=True, sources=True)  # 重启追踪
            print(f"录制文件已保存:{trace_path}")
        except Exception as e:
            print(f"录制文件保存失败：{e}")


# -------------------------- 原有清理/钩子逻辑（保留） --------------------------
@pytest.fixture(scope="session", autouse=True)
def clear_auth():
    if os.path.exists(AUTH_PATH):
        os.remove(AUTH_PATH)
    yield
    if os.path.exists(AUTH_PATH):
        os.remove(AUTH_PATH)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call":
        # 失败截图+日志
        if rep.failed:
            log_path = os.path.join(Config.logs, 'failure_logs.log')
            with open(log_path, "a", encoding="utf-8") as f:
                case_data = item.funcargs.get("CaseData", {})
                case_id = case_data.get("用例编号", "未知编号")
                f.write(f"失败用例:{rep.nodeid}(编号：{case_id})\n")

            with allure.step("添加失败截图"):
                # 支持page和logged_in_page两种参数名
                page = item.funcargs.get("page") or item.funcargs.get("logged_in_page")
                if page:
                    try:
                        page.wait_for_load_state("networkidle", timeout=5000)
                        screenshot_path = os.path.join(Config.test_screenshots_dir, f"{case_id}_失败截图.png")
                        page.screenshot(path=screenshot_path, timeout=5000)
                        with open(screenshot_path, "rb") as img:
                            allure.attach(img.read(), "失败截图:", allure.attachment_type.PNG)
                    except Exception as e:
                        allure.attach(f"截图失败:{str(e)}", "错误信息")

        # 所有用例写入whole.log
        whole_log_path = os.path.join(Config.logs, "whole.log")
        case_data = item.funcargs.get("CaseData", {})
        case_id = case_data.get("用例编号", "未知编号")
        if rep.failed:
            line = f"失败用例：{rep.nodeid}(编号：{case_id})\n"
        elif rep.skipped:
            line = f"跳过用例：{rep.nodeid}(编号：{case_id})\n"
        else:
            line = f"通过用例：{rep.nodeid}(编号：{case_id})\n"
        try:
            with open(whole_log_path, "a", encoding="utf-8") as wf:
                wf.write(line)
        except Exception as e:
            print(f"写入whole.log失败：{e}")