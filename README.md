# 文明 V Mac 中文补丁配套启动器

**帮助安装中文补丁后遇到启动闪退的 Mac 玩家，顺利进入中文游戏。**

本项目配合 [weixu-cestbon/civ5-macos-simplified-chinese：文明 V macOS 简体中文补丁](https://github.com/weixu-cestbon/civ5-macos-simplified-chinese) 使用。原项目负责从玩家本机的官方 Steam 中文资源生成汉化文本和字体；本项目将一次实际排查中验证有效的启动方式整理成可复用入口。

我们已在一台 Mac 上完成“安装中文 → 通过此启动方式进入主菜单 → 快速开始进入实际对局”的验证。希望把这条可复现的操作路径分享给同样需要中文的玩家。

仓库名称：`civ5-macos-chinese-launcher`。这是独立的配套项目，未获原项目作者或游戏发行商背书；不包含汉化资源，也不会安装、恢复或修改汉化文件。

## 从英文版到中文游戏

| 你的状态 | 下一步 |
| --- | --- |
| 还没有安装中文补丁 | 先按[原汉化项目的安装说明](https://github.com/weixu-cestbon/civ5-macos-simplified-chinese#最简单的安装方法)准备官方中文资源，生成并安装补丁。 |
| 已安装中文，普通启动时退出 | 保持 Steam 登录，退出游戏和启动器，运行本项目的 `启动文明5.command`。 |
| 已通过配套入口进入主菜单 | 检查中文显示，再“快速开始”进入一局，确认文字和实际游戏画面正常。 |
| 仍然失败 | 查看[排查说明](docs/diagnosis.md)，提供脱敏错误片段；这个入口不能保证解决所有原因的闪退。 |

**需要先安装中文补丁。仅运行本启动器不会把英文游戏翻译成中文。** 如果普通入口本来就能正常运行中文版，无需为使用中文额外更换启动方式。

## 已验证到什么程度

在一台 Apple Silicon Mac、macOS 26.5.1、Steam Civ V 1.4.2（180925）上，用户确认原始启动脚本可以运行英文版；恢复中文补丁后，用户确认中文正常，并通过“快速开始”进入实际对局。

本仓库将该脚本重构为通用入口，保留相同的执行文件、工作目录和环境变量处理。通用版本有自动化测试及本机路径检查，但**尚未单独做真实游戏启动回归**。单台机器、一次进入对局不代表长时间游玩或其他系统版本均受支持。

两项变化同时发生：绕过 Aspyr 启动器、移除子进程的 `DYLD_INSERT_LIBRARIES`。尚未用逐项对照实验确定具体原因；不能据此断言某个 Steam 组件有缺陷，也不能保证它能修复所有闪退。

## 使用

需要：已拥有并安装的 Steam macOS 版《文明 V》、已启动且登录的 Steam、Python 3.10 或更高版本。无第三方 Python 依赖。

1. 点击本页 **Code → Download ZIP** 下载本项目并解压。
2. 正常退出游戏和原启动器。
3. 在终端进入解压后的项目文件夹，运行 `python3 launch.py`。

如果希望以后双击启动，先在该文件夹运行一次：

```sh
chmod +x 启动文明5.command
```

随后双击 `启动文明5.command` 即可。网页上传的源码可能不保留执行权限，因此首次使用推荐 Python 命令。

脚本默认使用当前用户的 Steam 默认安装目录。安装在其他硬盘时，指定 `.app` 路径：

```sh
python3 launch.py --game "/Volumes/Games/SteamLibrary/steamapps/common/Sid Meier's Civilization V/Civilization V.app"
```

仅检查路径、不启动游戏：

```sh
python3 launch.py --dry-run
```

如果双击时被系统阻止，先阅读代码，再按 macOS 的单个应用允许流程处理；不需要关闭系统整体安全保护。`.command` 没有执行权限时，可使用上面的 Python 命令。

## 它做了什么

- 校验应用身份是 `com.aspyr.civ5xp.steam`，并检查原版执行文件存在。
- 直接运行应用包内的 `Contents/MacOS/Civilization V`，将工作目录设为 `Contents/MacOS`。
- 仅在游戏子进程中移除 `DYLD_INSERT_LIBRARIES`，设置 `SteamAppId=8930`、`SteamGameId=8930`。
- 将运行输出写入本机 `~/Library/Logs/Civ5LaunchHelper/`，每次新建日志，文件权限仅允许当前用户读取。

该环境处理可能影响 Steam 叠加层或其他依赖注入的功能；这些功能及多人联机尚未验证。工具不退出 Steam，不修改系统环境、不重新签名游戏、不修改游戏资源、存档或缓存，也不会上传日志。退出码为 0 只代表进程正常退出。

## 与中文补丁的关系

这次测试使用的汉化生成器来自 [weixu-cestbon/civ5-macos-simplified-chinese](https://github.com/weixu-cestbon/civ5-macos-simplified-chinese)。中文文本转换与字体生成属于该项目；本仓库仅提供独立的启动辅助代码，没有重新分发其生成物。

| 项目 | 职责 |
| --- | --- |
| 原汉化项目 | 官方中文资源的本地转换、中文字体生成、汉化安装与恢复。使用方法及这些功能的维护以原项目为准。 |
| 本配套启动器 | 使用已经安装好的游戏与中文资源，调整游戏子进程的启动方式，并保留本地运行日志。 |

本项目不是原汉化项目的官方分支，也没有将汉化成果署名为自己的作品。欢迎复现同类问题的玩家补充测试环境；若将来向原项目提交改进，会单独记录实际提交与采纳状态。

Steam 更新或文件校验可能覆盖已安装的中文资源，具体恢复方法请参考汉化项目。不要将游戏资源、字体、已生成汉化包、Steam 下载资源包或个人备份提交到本仓库。

## 排查与开发

排查过程及证据边界见 [docs/diagnosis.md](docs/diagnosis.md)。

```sh
python3 -m unittest discover -s tests -v
python3 tools/check_release.py
```

测试使用临时文件和模拟子进程，不会启动真实游戏。GitHub Actions 只检查代码行为，不验证游戏内效果。

本地 `civ5-repair-diagnostics` 文件夹中的定制恢复脚本依赖特定安装备份，不属于此通用项目。需要撤销本工具时删除项目即可；它没有安装系统组件。

MIT 许可证仅适用于本仓库代码和文档，不涵盖《文明 V》、Steam、游戏文本或字体。本项目与 2K、Firaxis、Aspyr、Valve 均无隶属或背书关系。
