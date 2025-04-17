@echo off
:: 清空 PluginsLoader.cfg 文件
echo. > PluginsLoader.cfg

:: 遍历 plugins 文件夹下的所有文件（不包括文件夹）
for %%f in (plugins\*) do (
    :: 检查是否是文件
    if not "%%~ff"=="%%~dpf" (
        echo exec Horizon/plugins/%%~nxf >> PluginsLoader.cfg
    )
)

echo 完成!
