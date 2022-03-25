<h1 align="center">UESTC 自动健康打卡</h1>

<p align="center">
  <img src="https://img.shields.io/github/license/mrcaidev/uestc-temperature"/>
  <img src="https://img.shields.io/github/issues/AzideCupric/uestc-temperature?color=green"/>
</p>

[电子科技大学本科生自动健康打卡](https://github.com/mrcaidev/uestc-temperature)的nonebot-plugin版本

## 简介
本项目可以作为您的nonebot2机器人插件使用，根据您提供的 _SessionId_ 进行打卡服务

基于[`NoneBot2`](https://github.com/nonebot/nonebot2) 与[`uestc-temperature`](https://github.com/mrcaidev/uestc-temperature)开发

开发初衷源于懒得点开小程序打卡，故直接将步骤在QQ内完成（躺）
故请确保使用时当前体温属于安全范围内！

修改很少，只是将源程序接入nonebot之中

## 使用须知

1. 本项目创立的初衷在于技术交流、相互学习，而并非为学生提供打卡服务。因此，该项目不对提供的服务质量作出保障。
2. 请牢记：疫情防控始终是一个敏感且重要的话题。如果您决定使用该项目所提供的服务，那么其带来的一切后果，均将由您个人承担，与原作者、贡献者无关。

## 使用方法

- 部署您的 _nonebot2_ 机器人：前往nonebot2的[官方网站](https://v2.nonebot.dev)
- 将本仓库中的`src/plugins`目录下的`nonebot_plugin_uestc_temperature`文件夹拷贝至您部署好的nonebot2的插件目录下
- 在nonebot2部署目录下的`bot.py`文件中启用该插件（请到nonebot2的[官方网站](https://v2.nonebot.dev)学习启用方法）
  - 注意：在您的nonebot2项目中的`pyproject.toml`文件中默认会加载`src/plugins`下的所有非下划线`_`开头的插件，该步骤通常可以跳过
- 向机器人发送`体温上报 user_name`命令完成体温填报，例：`体温上报 kaltsit`
  - 注意：使用该命令之前需要保证该`user_name`存在。如不存在，请看命令`更新id`
- 向机器人发送`更新id user_name`命令，并提供Session Id完成用户信息的更新，例：`更新id amiya`
  - 注意：当该需要添加的用户不存在时，会自动创建新的用户
- 向机器人发送`用户列表`命令，会列出所有当前已暂存的用户
  - 仅限SUPERUSER(nonebot2项目的拥有者，请查阅nonebot相关设置)
## FAQ

- 如果你遇到了任何问题，请先查看源项目的 [FAQ](https://github.com/mrcaidev/uestc-temperature/wiki/FAQ)
- 功能出现问题烦请提交issue
- 临时存储Session Id的部分写的很差（懒鬼是这样的），用户过多时性能应该不是很好（看到源代码轻喷
- 如果想对项目进行优化欢迎提交pr

## 咕咕咕清单
- [x] 实现Session Id的储存，不需要每次上报都提供
- [ ] 实现发送无参数的`体温上报`和`更新id`命令时，默认上报或者更新以发送者QQ为用户的信息
- [ ] 机器人定时提醒填报，定时复查
- [ ] 使用tinydb储存数据

## 许可证

[MIT](https://github.com/AzideCupric/uestc-temperature/blob/master/LICENSE)

## 鸣谢
- [`go-cqhttp`](https://github.com/Mrs4s/go-cqhttp)：简单又完善的 cqhttp 实现
- [`NoneBot2`](https://github.com/nonebot/nonebot2)：超好用的开发框架
- [`uestc-temperature`](https://github.com/mrcaidev/uestc-temperature): 已经实现完整核心功能的源项目，我所做的不过是小小的修改
