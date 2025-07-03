"""pytest 설정 파일"""


def pytest_ignore_collect(path, config):
    """특정 경로의 conftest 파일들을 제외"""
    path_str = str(path)
    
    # numpy, pandas, IPython 관련 경로 제외
    exclude_patterns = [
        "deployment/tests",
        "numpy/conftest.py",
        "pandas/conftest.py", 
        "pandas/tests/",
        "IPython/conftest.py",
        "venv/lib/python3.12/site-packages/numpy/",
        "venv/lib/python3.12/site-packages/pandas/",
        "venv/lib/python3.12/site-packages/IPython/"
    ]
    
    if any(exclude in path_str for exclude in exclude_patterns):
        return True
    return False


def pytest_configure(config):
    """pytest 설정 시 호출되는 함수"""
    # numpy, pandas conftest 충돌 방지
    # 이미 등록된 플러그인 제거
    plugin_manager = config.pluginmanager
    
    # numpy, pandas 관련 플러그인 제거
    plugins_to_remove = []
    for plugin_name, plugin in plugin_manager.list_plugin_distinfo():
        if plugin and hasattr(plugin, 'location'):
            location = str(plugin.location)
            if any(pattern in location for pattern in [
                'numpy/conftest.py', 'pandas/conftest.py'
            ]):
                plugins_to_remove.append(plugin_name)
    
    for plugin_name in plugins_to_remove:
        try:
            plugin_manager.set_blocked(plugin_name)
        except Exception:
            pass


def pytest_collection_modifyitems(config, items):
    """테스트 수집 시 호출되는 함수"""
    # numpy, pandas 관련 conftest 제외
    pass


def pytest_plugin_registered(plugin, manager):
    """플러그인 등록 시 호출되는 함수"""
    # numpy, pandas conftest 플러그인 등록 방지
    if hasattr(plugin, '__file__'):
        plugin_file = str(plugin.__file__)
        if any(pattern in plugin_file for pattern in [
            'numpy/conftest.py', 'pandas/conftest.py'
        ]):
            # 플러그인 등록 차단
            return False 