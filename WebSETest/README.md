# WebSETest 说明

`WebSETest/` 是语义等价验证站点，采用 PHP + MySQL 组织不同注入类型的测试页面。

## 目录内容

- `index.php`：入口页面
- `union.php`、`error.php`、`bool.php`、`time.php`：不同注入类型的测试页面
- `get_*.php`、`post_*.php`：不同请求方式和参数形式的测试页面
- `config.php`：数据库连接配置
- `database/sqlidb.sql`：数据库初始化脚本
- `reset.php`：重置测试表结构与初始数据
- `global_library.php`：公共函数库

## 启动步骤

1. 准备 PHP 环境和 MySQL 环境。
2. 导入 `database/sqlidb.sql`，创建所需数据库与初始表。
3. 修改 `config.php`，使数据库地址、用户名、密码和库名与本地环境一致。
4. 将 `WebSETest/` 放到 Web 服务根目录，或使用 PHP 内置服务直接启动该目录。
5. 访问 `index.php`，检查首页与各类测试页面是否可用。

## 访问方式

站点提供 GET、POST、布尔盲注、报错注入、时间盲注和联合查询等不同页面，便于比较 payload 变换前后的返回结果。

## 初始化说明

`database/sqlidb.sql` 用于创建初始数据库结构。`reset.php` 用于恢复测试表，便于在多轮实验之间切换到一致状态。

## 作用

该站点用于判断 payload 变换前后是否仍能保持语义等价，并为框架中的验证步骤提供统一的观察入口。
