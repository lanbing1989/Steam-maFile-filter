# Steam-maFile-filter

## 简介
Steam-maFile-filter 是一个用于过滤和管理 Steam 账户 maFile 文件的小工具。通过本工具，用户可以批量处理 maFile 文件，实现自动筛选、整理和管理，大幅提升 Steam 账户批量运维的效率。

## 特性
- 批量筛选 maFile 文件
- 按多种条件（如账户状态、文件内容等）过滤
- 支持导出或移动符合条件的文件
- 兼容常见的 maFile 目录结构
- 简洁易用的命令行界面

## 使用方法

### 1. 克隆项目
```bash
git clone https://github.com/lanbing1989/Steam-maFile-filter.git
cd Steam-maFile-filter
```

### 2. 安装依赖（如有）
如果项目使用 Python 依赖，请运行：
```bash
pip install -r requirements.txt
```
> 具体依赖请参考项目内 requirements.txt 或相关文档。

### 3. 运行工具
假设主程序为 `main.py`，可执行如下命令：
```bash
python main.py --source ./maFiles --filter valid --output ./filtered
```
参数说明：
- `--source`：原始 maFile 文件夹路径
- `--filter`：过滤条件（如 valid、invalid、by-login 等）
- `--output`：输出文件夹路径

> 具体参数和用法，请参考代码或执行 `python main.py --help` 获取帮助。

## 注意事项
- 请确保在操作前备份好 maFile 文件，避免数据丢失。
- 本工具为开源项目，欢迎提交 Issue 或 PR 参与完善。

## 贡献
欢迎任何形式的贡献！如有建议或 Bug，欢迎提交 Issue 反馈。

## 许可证
本项目采用 MIT License 进行开源，详见 [LICENSE](./LICENSE)。

## 联系方式
如有问题，可通过 GitHub Issues 联系作者。

---

感谢使用 Steam-maFile-filter，祝您管理愉快！
