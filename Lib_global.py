# Lib_global.py
# глобальные переменные (значения изменяются в read_ini_file)
_path_ini_file: str = "BCS_XP.ini"  # или лучше назвать "settings.ini"?
_path_log: str = "."  # задаётся в ini-файле в секции [LogFiles]
_path_err_log: str = "."
_analyzer_id: int = 911  # задаётся в ini-файле в секции [Connection]
_com_port_name: str = 'no!'
_sql_connect: str = 'yes'
_server: str = 'Asu-911'  # 'tcp:myserver._database.windows.net'
_database: str = 'LabAutoResult'
_username: str = 'sa'
_password: str = '1'
_err_date: str = 'd-m-y'  # задаётся в ini-файле в секции [Statistics]
_err_msg: str = 'xx-x'
_run_count: int = 911
_list_modes: str = '-'  # задаётся в ini-файле в секции [Modes]
_debug: bool = False

