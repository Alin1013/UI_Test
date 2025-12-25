#相关配置文件
import pytest
import os
import uuid
import allure
from playwright.sync_api import sync_playwright,expect    #异步playwright
from Config.Config import Config

#初始化必要目录
Config.create_directories()
#创建录制文件存放目录
os.makedirs("tracing_files",exist_ok=True)

#认证文件路径，匹配是否正确
AUTH_PATH=os.path.join(Config.auth_dir,"auth.json")

#使用装饰器和夹具，控制参数scope为function
@pytest.fixture(scope="function")
#进行相关页面配置的方法封装
def page(request):
    #使用playwright的驱动进行操作
    with sync_playwright() as play:
        browser=play.chromium.launch(
            headless=False,
            channel=Config.browser,
            args=['--start-maximized']      #开始操作时，页面窗口最大化，可以监测是否会有窗口大小自适应问题
        )
        #禁用认证状态复用，保证用例独立
        context=browser.new_context(no_viewport=True) #浏览器驱动
        context.tracing.start(screenshots=True,snapshots=True,sources=True) #在录制过程中，可以进行相关页面截屏操作
        page=context.new_page() #保证每次打开都是一个新页面

        yield page

        #在yield之后获取用例数据，确保正确获取到参数化数据
        case_data=request.node.funcargs.get("CaseData",{})
        print("当前用例数据：",case_data)
        #提取yaml文件中的用例标题前的标注，便于后续查找到对应的标题名称
        case_title=case_data.get("用例标题","未命名标题")
        #清除标题中的无效字符，避免文件名无效
        safe_title="".join([c for c in case_title if c not in r'\/:*?"<>|'])

        #安全保存tracing文件(获取到的标题名称+随机字符串）
        try:
            trace_filename=f"trace_{safe_title}_{uuid.uuid4().hex[:8]}.zip"
            trace_path=os.path.join("tracing_files",trace_filename)
            context.tracing.stop(path=trace_path)
            print(f"录制文件已保存:{trace_path}")
        except Exception as e:
            print(f"录制文件保存失败：{e}")

        #关闭相关资源
        page.close()
        context.close()
        browser.close()

@pytest.fixture(scope="session",autouse=True)
def clear_auth():
    #在开始context之前和结束之后清理认证文件
    if os.path.exists(AUTH_PATH):
        os.remove(AUTH_PATH)
    yield
    if os.path.exists(AUTH_PATH):
        os.remove(AUTH_PATH)


@pytest.hookimpl(hookwrapper=True)
#pytest运行文件
def pytest_runtest_makereport(item,call):
    outcome = yield
    rep=outcome.get_result()

    if rep.when == "call" and rep.failed:
        #记录失败日志
        log_path=os.path.join(Config.logs,'failure_logs.log')
        with open(log_path,"a",encoding="utf-8") as f:
            case_data=item.funcargs.get("CaseData",{})
            case_id=case_data.get("用例编号","未知编号")
            f.write(f"失败用例:{rep.nodeid}(编号：{case_id})\n")

        #记录失败的截图
        with allure.step("添加失败截图"):
            page=item.funcargs.get("page")
            if page:
                try:
                    page.wait_for_load_state("networkidle",timeout=5000)
                    screenshot_path=os.path.join(Config.test_screenshots_dir,f"{case_id}_失败截图.png")
                    page.screenshot(path=screenshot_path,timeout=5000)
                    with open(screenshot_path,"rb") as img:
                        allure.attach(img.read(),"失败截图:",allure.attachment_type.PNG)
                except Exception as e:
                    allure.attach(f"截图失败:{str(e)}","错误信息")

        #将每个用例的所有结果写入whole.log中
        if rep.when =="call":
            whole_log_path=os.path.join(Config.logs,"whole.log")
            case_data=item.funcargs.get("CaseData",{})
            case_id=case_data.get("用例编号","未知编号")
            if rep.failed:
                line=f"失败用例：{rep.nodeid}(编号：{case_id})\n"
            elif rep.skipped:
                line=f"跳过用例：{rep.nodeid}(编号：{case_id})\n"
            else:
                line=f"通过用例：{rep.nodeid}(编号：{case_id})\n"
            try:
                with open(whole_log_path,"a",encoding="utf-8") as wf:
                    wf.write(line)
            except Exception:
                pass

#复用登录成功的fixture
import pytest
from Pages.LoginPage.LoginPage import LoginPage
from Utils.read_yaml import ReadYaml

@pytest.fixture(scope="function")
def login_success_fixture(page):
    #读取登陆成功用例
    test_data=ReadYaml(os.path.join(Config.test_datas_dir,"TestLoginData.yaml")).read()
    #遍历一遍用例
    for case in test_data:
        if case.get("用例标题")=="账号密码正确，登录成功":
            login_page=LoginPage(page)
            login_page.goto_login(case["url"])
            login_page.fill_username(case["账号"])
            login_page.fill_password(case["密码"])
            login_page.click_login_button()
            #使用url验证离开登录页
            import re
            expect(login_page.page).not_to_have_url(re.compile(r".*/#/login$"),timeout=15000)
            return login_page.page
    raise Exception("未找到成功登陆的测试用例")

