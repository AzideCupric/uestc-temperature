<h1 align="center">UESTC 自动健康打卡</h1>

<p align="center">
  <img src="https://img.shields.io/github/license/mrcaidev/uestc-temperature"/>
  <img src="https://img.shields.io/github/issues/AzideCupric/uestc-temperature?color=green"/>
</p>

[电子科技大学本科生自动健康打卡](https://github.com/mrcaidev/uestc-temperature)的nonebot-plugin版本

## 简介
本项目可以作为您的nonebot机器人插件使用，根据您提供的 _SessionId_ 进行打卡服务

基于[`NoneBot2`](https://github.com/nonebot/nonebot2) 与[`uestc-temperature`](https://github.com/mrcaidev/uestc-temperature)开发

开发初衷源于懒得点开小程序打卡，故直接将步骤在QQ内完成（躺）

修改很少，只是将源程序接入nonebot之中

## 使用须知

1. 本项目创立的初衷在于技术交流、相互学习，而并非为学生提供打卡服务。因此，该项目不对提供的服务质量作出保障。
2. 请牢记：疫情防控始终是一个敏感且重要的话题。如果您决定使用该项目所提供的服务，那么其带来的一切后果，均将由您个人承担，与原作者、贡献者无关。

## 使用方法

- 部署您的 _nonebot_机器人：前往nonebot的[官方网站](https://v2.nonebot.dev)
- 将本仓库中的`src/plugins`目录下的`nonebot_plugin_uestc_temperature`文件夹拷贝至您部署好的nonebot的插件目录下
- 在nonebot部署目录下的`bot.py`文件中启用该插件（请到nonebot的[官方网站](https://v2.nonebot.dev)学习启用方法）
- 向机器人发送`体温上报 user_name`命令，并提供SessionId完成体温填报，例：`体温上报 kaltsit`
- 向机器人发送
## FAQ

- 如果你遇到了任何问题，请先查看源项目的 [FAQ](https://github.com/mrcaidev/uestc-temperature/wiki/FAQ)
- 功能出现问题基本上不会是插件部分的问题，因为插件套壳的部分写的很少（原作者已经做的很好了）

## 咕咕咕清单
- [ ] 实现Session Id的储存，不需要每次上报都提供
- [ ] 机器人定时提醒填报，定时复查

## 许可证

[MIT](https://github.com/AzideCupric/uestc-temperature/blob/master/LICENSE)

## 鸣谢
- [`go-cqhttp`](https://github.com/Mrs4s/go-cqhttp)：简单又完善的 cqhttp 实现
- [`NoneBot2`](https://github.com/nonebot/nonebot2)：超好用的开发框架
- [`uestc-temperature`](https://github.com/mrcaidev/uestc-temperature): 实现完整功能的源项目，我所做的不过是小小的修改
