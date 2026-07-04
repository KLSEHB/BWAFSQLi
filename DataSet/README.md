# DataSet 目录说明

`DataSet/` 存放数据集、划分结果与预处理脚本，供灰盒与黑盒流程共同使用。

## 目录内容

- `SQLiCFG/`：作者自建数据集，包含 CFG 相关样本与划分结果
- `HPD/`：公开基准数据集及其预处理输出
- `SIK/`：公开基准数据集及其预处理输出
- `SEJ/`：语义等价验证样例集，按注入类型和请求形式组织
- `data_pre.py`：数据预处理入口脚本

## 数据文件类型

- `sqli.txt`：完整攻击样本
- `sqli_train.txt`、`sqli_val.txt`、`sqli_test.txt`：攻击样本划分
- `norm.txt`：归一化后的非攻击样本或对照样本
- `norm_train.txt`、`norm_val.txt`、`norm_test.txt`：对照样本划分
- `sqli.xlsx`、`norm.xlsx`、`SQLiV3.csv` 等：中间整理结果与辅助格式
