# BWAFSQLi

`BWAFSQLi: Bypassing Web Application Firewall with Adversarial SQL Injections` 的项目实现与实验资料。项目围绕 SQL 注入样本生成、WAF 绕过评估和语义等价验证三个环节组织。

## 论文引用

- 论文标题：`BWAFSQLi: Bypassing Web Application Firewall with Adversarial SQL Injections`
- DOI：`10.1145/3788286`
- 论文链接：[ACM DOI](https://dl.acm.org/doi/10.1145/3788286)

## 声明

本项目仅限于已授权的学术研究、教学验证和受控实验环境。不得用于未授权测试、生产防护绕过或批量攻击。使用、转载或二次整理时应保留论文引用与项目来源。

## 参考来源

本项目的代码结构参考了 [u21h2/AutoSpear](https://github.com/u21h2/AutoSpear)。

## 功能概览

- Payload 生成与变换
- CFG 规则驱动的变异与 token 级重写
- 灰盒模型服务评估
- 黑盒模型服务评估
- `WebSETest` 语义等价验证
- 运行日志、路径与成功结果记录

## 目录结构

- `BWAF/`：核心攻击框架与主入口
- `DataSet/`：数据集、划分结果与预处理脚本
- `WebSETest/`：语义等价验证站点
- `灰盒/`：灰盒模型服务、数据与权重

## 模块说明

### `BWAF/`

核心执行目录，负责参数解析、payload 生成、变换控制、等价验证接入和日志记录。

### `DataSet/`

存放用于训练、验证和测试的数据文件，以及生成这些数据的辅助脚本。

### `WebSETest/`

语义等价验证站点，采用 PHP + MySQL 组织不同注入类型的测试页面。

### `GraykBox/`

灰盒模式所需的模型服务与配套文件，包含 CNN、GRU 和 LSTM 三类实现。

## 日志输出

每次执行后，`BWAF/logs/` 会生成一个时间戳目录。常见文件包括：

- `#summary.log`
- `#detail.log`
- `#success.log`
- `#path.log`
- `#except.log`
- `#benign.log`
- `#defend.log`
