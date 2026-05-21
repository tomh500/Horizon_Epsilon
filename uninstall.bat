@echo off
:: 开启 UTF-8 编码支持，防止删除带中文或特殊符号的路径时出错
chcp 65001 >nul
cls

echo ======================================================
echo          Horizon 自动部署脚本 - 正在全面卸载...
echo ======================================================
echo.

:: ------------------ 1. 权限与路径检查 ------------------
:: 检查当前脚本是否在 game/csgo/cfg/Horizon 目录下
set "CURRENT_DIR=%~dp0"
echo [INFO] 当前运行路径：%CURRENT_DIR%

echo "%CURRENT_DIR%" | findstr /i "game\\csgo\\cfg\\horizon" >nul
if errorlevel 1 (
    echo [ERROR] 错误：请将此卸载脚本放入 game/csgo/cfg/Horizon 目录下运行！
    echo.
    pause
    exit /b
)

:: ------------------ 2. 清理计划任务与后台守护进程 ------------------
echo [INFO] 正在停止并删除开机自启计划任务...
schtasks /delete /tn "Horizon_Guard_Launcher" /f >nul 2>&1

echo [INFO] 正在强制结束守护进程与游戏环境...
taskkill /f /im guard.exe >nul 2>&1
taskkill /f /im cs2.exe >nul 2>&1
taskkill /f /im steam.exe >nul 2>&1
taskkill /f /im steamwebhelper.exe >nul 2>&1
timeout /t 1 /nobreak >nul

:: ------------------ 3. 反向清理复制到游戏目录的资源 ------------------
:: 定位 game/csgo 目录
for %%I in ("%CURRENT_DIR%..\..") do set "TARGET_BASE=%%~fI"
set "TARGET_RESOURCE=%TARGET_BASE%\resource"
set "TARGET_SOUNDS=%TARGET_BASE%\sounds"

:: 定位 game/cfg 目录
for %%I in ("%CURRENT_DIR%..\..\..\cfg") do set "TARGET_CFG=%%~fI"

echo [INFO] 正在清理复制出的资源资产...
:: 删除 resource 下的 keybindings_ 文件
if exist "%TARGET_RESOURCE%" (
    pushd "%TARGET_RESOURCE%"
    for /f "delims=" %%F in ('dir /b keybindings_* 2^>nul') do (
        del /f /q "%%F" >nul 2>&1
        echo   - 已移除资源: resource/%%F
    )
    popd
)

:: 删除 boot.vsnd_c
if exist "%TARGET_SOUNDS%\boot.vsnd_c" (
    del /f /q "%TARGET_SOUNDS%\boot.vsnd_c" >nul 2>&1
    echo   - 已移除音效: sounds/boot.vsnd_c
)

:: 删除 game/cfg 下的 installbatload_5_6.cfg
if exist "%TARGET_CFG%\installbatload_5_6.cfg" (
    del /f /q "%TARGET_CFG%\installbatload_5_6.cfg" >nul 2>&1
    echo   - 已移除配置: cfg/installbatload_5_6.cfg
)

:: ------------------ 4. 剃除 autoexec.cfg 中的 exec 引导行 ------------------
set "AUTOEXEC_PATH=%CURRENT_DIR%..\autoexec.cfg"
if exist "%AUTOEXEC_PATH%" (
    echo [INFO] 正在剔除 autoexec.cfg 中的加载项...
    :: 创建一个临时文件来过滤内容
    set "TEMP_FILE=%TEMP%\autoexec_temp.cfg"
    if exist "%TEMP_FILE%" del /f /q "%TEMP_FILE%"
    
    :: 逐行读取，只要不是 "exec Horizon/load.cfg" 就写入新文件
    for /f "delims=" %%L in ('type "%AUTOEXEC_PATH%" 2^>nul') do (
        set "LINE=%%L"
        setlocal enabledelayedexpansion
        if not "!LINE!"=="exec Horizon/load.cfg" (
            echo !LINE!>>"%TEMP_FILE%"
        )
        endlocal
    )
    
    :: 用过滤后的新文件覆盖原文件
    move /y "%TEMP_FILE%" "%AUTOEXEC_PATH%" >nul 2>&1
    echo   - autoexec.cfg 清理完成。
)

:: ------------------ 5. 自杀式清理 Horizon 文件夹自身 ------------------
echo [INFO] 正在准备清除 Horizon 核心目录...
echo ⚠️ 注意：脚本即将退出并彻底删除当前 Horizon 文件夹。

:: 延迟执行自删除，防止因为当前批处理文件被锁定而导致删除失败
start "" cmd /c "timeout /t 2 /nobreak >nul & rd /s /q \"%CURRENT_DIR%\""

echo.
echo ======================================================
echo 🎉 卸载部署已全部完成！Steam 启动项请自行根据需要恢复。
echo ======================================================
echo.
pause
exit