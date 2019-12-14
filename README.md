# ghost_sa
open_server for sensorsdata
感谢神策公司开源了他们的SDK，让用不起神策服务端的中小企业也可以使用大数据带来的便利。

ghost_sa(鬼策)的用途是接收 神策SDK 上报的数据，和实现神策上的短链创建与解析功能。

数据库依赖TiDB，实测1天100万事件量，查询在10毫秒左右。如果只是体验，也可以用MySQL，不过性能很差。
目前经过测试，支持IOS，JS，小程序，Python的SDK上报。SDK可以在神策的项目中下载 https://github.com/sensorsdata

需要完整的神策功能，请购买神策官方授权。https://www.sensorsdata.cn/
