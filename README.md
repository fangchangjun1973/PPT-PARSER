# PPT Parser

PPT文档解析器 - 将JSON配置转换为PowerPoint演示文稿

## 功能特性

- JSON配置解析
- PPT文档生成
- 支持多种元素类型
- 灵活的插件系统

## 安装

使用 Poetry 安装项目依赖：

```bash
poetry install
```

## 开发

激活虚拟环境：

```bash
poetry shell
```

运行测试：

```bash
pytest
```

代码格式化：

```bash
black .
```

代码检查：

```bash
pylint ppt_parser
mypy ppt_parser
```

## 项目结构

```
ppt_parser/
├── core/           # 核心功能模块
├── exceptions/     # 异常定义
├── models/         # 数据模型
├── plugins/        # 插件系统
└── tests/          # 测试用例
```

## 使用示例

```python
from ppt_parser import ParserEngine

# 创建解析引擎
engine = ParserEngine()

# 解析JSON配置
with open('presentation.json', 'r', encoding='utf-8') as f:
    config = f.read()
    
document = engine.parse(config)

# 生成PPT文件
document.save('output.pptx')
```