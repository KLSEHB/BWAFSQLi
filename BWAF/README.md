# BWAF 目录说明

`BWAF/` 是项目的核心执行目录，负责攻击流程编排、payload 变换、语义等价验证接入以及结果记录。

## 文件与子目录

- `main.py`：主入口，负责读取参数、选择模式、加载数据并启动整体流程
- `SQLi.py`：payload 生成、变换与组合逻辑
- `Equiv.py`：语义等价验证客户端
- `global_vars.py`：全局参数、计数器与公共辅助函数
- `clients/`：灰盒客户端、黑盒客户端与防御预处理相关代码
- `cfg/`：CFG 规则与 token 级变换规则
- `entry/`：叶子节点解析、路径记录与贪心权重相关逻辑
- `text/`：辅助词表
- `CombinationAnalysis/`：路径组合统计与分析脚本
- `logs/`：运行日志输出目录

## `main.py` 参数

- `-p` / `--pattern`：运行模式，取值为 `GrayBox` 或 `BlackBox`
- `-g` / `--guide`：引导策略，常见取值包括 `random`、`greedWeight`、`greedWeightAndAllMutation` 和 `benign`
- `-ds` / `--dataset`：数据集名称，常见取值包括 `SQLiCFG`、`HPD` 和 `SIK`
- `-MLu` / `--GrayBox_url`：灰盒模型服务地址
- `-MLt` / `--GrayBox_thresh`：灰盒判定阈值
- `-WAFu` / `--BlackBox_url`：黑盒目标地址
- `-r` / `--request_method`：请求方式与参数格式
- `-status` / `--intercept_status`：黑盒拦截状态码
- `-mat` / `--max_attempts`：单个 payload 的最大尝试轮数
- `-mst` / `--max_steps`：单轮最大步数

## 运行方式

1. 确认当前工作目录为 `BWAF/`。
2. 选择灰盒模式或黑盒模式，并配置对应参数。
3. 准备好数据集路径、模型服务地址或目标 WAF 地址。
4. 启动主流程后，程序会读取相应输入并执行变换、验证和统计。

## 输出结果

每次执行后，`logs/` 会生成一个时间戳目录，常见文件包括：

- `#summary.log`
- `#detail.log`
- `#success.log`
- `#path.log`
- `#except.log`
- `#benign.log`
- `#defend.log`

## 路径要求

`main.py` 使用相对路径读取数据与词库。移动目录后，需要同步检查数据集、词库和日志路径是否仍然有效。
