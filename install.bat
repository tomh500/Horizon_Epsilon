@echo off
chcp 65001
setlocal enabledelayedexpansion

REM 进入 RootPath 目录
pushd "%~dp0"
echo [INFO] 当前路径为：%CD%

REM 设置路径变量
set "SrcPath=%CD%\src\resources"
set "TargetBase=%CD%\..\..\"
set "TargetResource=%TargetBase%resource"
set "TargetSounds=%TargetBase%sounds"
set "TargetCfg=%CD%\..\..\..\cfg"
set "AutoexecPath=%CD%\..\autoexec.cfg"

REM 复制 keybindings 文件
echo [INFO] 准备复制 keybindings 文件到："%TargetResource%"
if not exist "%TargetResource%" (
    echo [INFO] 创建资源目录："%TargetResource%"
    mkdir "%TargetResource%"
)
copy /Y "%SrcPath%\keybindings_*.txt" "%TargetResource%"

REM 复制 boot.vsnd_c 文件
echo [INFO] 准备复制 boot.vsnd_c 到："%TargetSounds%"
if not exist "%TargetSounds%" (
    echo [INFO] 创建声音目录："%TargetSounds%"
    mkdir "%TargetSounds%"
)
copy /Y "%SrcPath%\boot.vsnd_c" "%TargetSounds%"

REM 复制 installbatload_5_6.cfg 文件
echo [INFO] 准备复制 installbatload_5_6.cfg 到："%TargetCfg%"
if not exist "%TargetCfg%" (
    echo [INFO] 创建 cfg 目录："%TargetCfg%"
    mkdir "%TargetCfg%"
)
copy /Y "%SrcPath%\installbatload_5_6.cfg" "%TargetCfg%"

REM 检查并修改 autoexec.cfg
echo [INFO] 检查 autoexec.cfg 是否存在："%AutoexecPath%"
if not exist "%AutoexecPath%" (
    echo [INFO] autoexec.cfg 不存在，创建中...
    echo. > "%AutoexecPath%"
)

set "FoundExecLine=false"
for /f "usebackq delims=" %%A in ("%AutoexecPath%") do (
    echo %%A | findstr /C:"exec Horizon_Epsilon/load.cfg" >nul
    if not errorlevel 1 (
        set "FoundExecLine=true"
    )
)

if "!FoundExecLine!"=="false" (
    echo [INFO] 追加 exec Horizon_Epsilon/load.cfg 到 autoexec.cfg
    echo exec Horizon_Epsilon/load.cfg >> "%AutoexecPath%"
) else (
    echo [INFO] autoexec.cfg 已包含目标行，无需追加
)

REM 结束
popd
echo.
echo [完成] 所有操作已执行完毕。
echo 请按 Enter 键退出...
pause >nul
exit /b
