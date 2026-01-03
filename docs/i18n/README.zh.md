# TickZero

**TickZero: AI驱动的CS2高光提取工具。使用免费AI自动将您的反恐精英2游戏画面转换为TikTok/Reels病毒短视频。**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![AI-Powered](https://img.shields.io/badge/AI-Google%20Gemini-orange.svg)](https://ai.google.dev/)

> 📖 **其他语言版本:** [English](../../README.md) · [Italiano](README.it.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)

## 🎯 功能特性

- **🎮 实时事件记录** - 通过CS2游戏状态集成实时捕获击杀、爆头和回合事件
- **⏱️ OBS同步** - 游戏事件与视频录制之间精确的时间戳对齐
- **🤖 AI驱动分析** - 使用Google Gemini(免费套餐)识别值得高光的时刻
- **✂️ 自动视频编辑** - 基于FFmpeg将视频转换为竖屏格式(9:16)并添加模糊背景
- **⚡ 硬件加速** - 支持NVIDIA NVENC,自动回退到CPU

## 📋 系统要求

### 软件
- **Python** 3.10或更高版本
- **OBS Studio** 启用WebSocket插件
- **FFmpeg** (硬件编码支持可选)
- **反恐精英2**
- **Google API密钥** 用于Gemini(提供免费套餐 - 无需信用卡!)

### Python依赖
```bash
pip install -r requirements.txt
```

**依赖项:** `google-genai`, `obs-websocket-py`, `flask`

## 🚀 快速开始

### 1. 克隆和安装

```bash
git clone https://github.com/MACULINX/TickZero.git
cd TickZero
pip install -r requirements.txt
```

### 2. 配置OBS WebSocket

1. 打开 **OBS Studio**
2. 转到 **工具 → WebSocket服务器设置**
3. 启用WebSocket服务器
4. 记录端口(默认: `4455`)和密码(如果设置)
5. 更新`main.py`中的`config`:

```python
config = {
    'obs_host': 'localhost',
    'obs_port': 4455,              # OBS WebSocket端口
    'obs_password': '',            # OBS WebSocket密码
    'gsi_port': 3000,              # GSI服务器端口
    'log_file': 'match_log.json',
    'output_dir': 'highlights',
    'use_gpu': True,               # 启用GPU加速
    'continuous_mode': True,       # 比赛后自动处理
    'auto_process': True,          # 启用自动处理
    'auto_min_priority': 6         # 最低优先级(1-10)
}
```

### GPU加速

TickZero会自动检测并使用最佳可用的GPU编码器:

1. **NVIDIA NVENC** (h264_nvenc) - 需要安装驱动的NVIDIA GPU
2. **AMD AMF** (h264_amf) - 需要AMD Radeon GPU
3. **Intel QuickSync** (h264_qsv) - 需要带核显的Intel CPU
4. **CPU Fallback** (libx264) - 适用于任何系统

### 连续录制模式

启用 `continuous_mode: True` 后, TickZero会:
- 自动检测比赛结束("gameover"事件)
- 后台处理高光时刻
- 继续录制下一场比赛
- 比赛之间无需重启!

### 3. 启用CS2游戏状态集成

将`gamestate_integration_highlights.cfg`复制到您的CS2配置文件夹:

```
Windows: C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\game\csgo\cfg\
Linux:   ~/.steam/steam/steamapps/common/Counter-Strike Global Offensive/game/csgo/cfg/
```

### 4. 获取Google Gemini API密钥(免费!)

1. 访问 [Google AI Studio](https://aistudio.google.com/app/apikey)
2. 使用您的Google账户登录
3. 点击 **"Create API Key"**
4. 复制您的密钥(以`AIzaSy...`开头)
5. 设置为环境变量:

**Windows (PowerShell):**
```powershell
$env:GOOGLE_API_KEY = "您的API密钥"

# 设为永久:
[System.Environment]::SetEnvironmentVariable('GOOGLE_API_KEY', '您的API密钥', 'User')
```

**Linux/Mac:**
```bash
export GOOGLE_API_KEY="您的API密钥"

# 设为永久(添加到~/.bashrc或~/.zshrc):
echo 'export GOOGLE_API_KEY="您的API密钥"' >> ~/.bashrc
source ~/.bashrc
```

> 💡 **注意:** Gemini 2.5 Flash免费提供1500次请求/天。足够约50场比赛/天!

## 📖 使用方法

流水线分为**两个阶段**:

### 阶段1: 实时记录(比赛期间)

在开始CS2比赛**之前**运行:

```bash
python main.py live
```

**执行内容:**
1. ✅ 连接到OBS WebSocket
2. ✅ 自动开始录制
3. ✅ 在端口3000启动GSI服务器
4. ✅ 记录所有游戏事件及精确的视频时间戳

正常进行您的比赛。完成后,按`Ctrl+C`停止记录。

事件保存在`match_log.json`中。

### 阶段2: 后处理(比赛之后)

比赛**之后**运行以创建高光片段:

```bash
python main.py process <录制文件路径.mp4> [api密钥] [最低优先级]
```

**示例:**
```bash
python main.py process "C:\Videos\cs2_match.mp4" 6
```

**参数:**
- `<录制文件路径.mp4>` - OBS录制文件路径(必需)
- `[api密钥]` - Google API密钥(如果设置了`GOOGLE_API_KEY`环境变量则可选)
- `[最低优先级]` - 片段最低优先级1-10(默认: 6)

**执行内容:**
1. 🤖 AI分析`match_log.json`
2. 🎯 识别高光时刻(多杀、残局、爆头)
3. ✂️ 在`highlights/`目录创建竖屏视频片段

## 🎬 输出格式

**竖屏视频规格:**
- **分辨率:** 1080×1920(9:16宽高比)
- **格式:** MP4 (H.264)
- **音频:** AAC立体声
- **视觉风格:** 模糊背景 + 居中游戏画面

**文件命名规则:**
```
clip_01_3k_headshot_p9.mp4
clip_02_clutch_1v3_p8.mp4
clip_03_ace_p10.mp4
```

## 🐛 故障排除

### OBS连接问题
- ✅ 确保OBS Studio正在运行
- ✅ 检查WebSocket是否启用: **工具 → WebSocket服务器设置**
- ✅ 验证端口和密码是否与配置匹配

###未记录任何事件
- ✅ 验证`gamestate_integration_highlights.cfg`是否在正确的CS2文件夹中
- ✅ 检查GSI服务器是否运行(应显示"Listening on port 3000")
- ✅ 启动CS2并检查控制台是否有GSI连接消息

### FFmpeg错误
- ✅ 确保已安装FFmpeg: `ffmpeg -version`
- ✅ 验证源视频路径是否正确
- ✅ 如果遇到NVENC错误,尝试设置`use_gpu: False`

### AI未返回高光时刻
- ✅ 检查`match_log.json`是否包含击杀事件
- ✅ 降低`min_priority`阈值(尝试4或5)
- ✅ 验证Google API密钥是否有效: 运行`python examples/test_gemini_api.py`
- ✅ 检查是否超过每日配额(1500次请求)

## 🤝 贡献

欢迎贡献! 请随时提交Pull Request。对于重大更改,请先开issue讨论您想要更改的内容。

详见[CONTRIBUTING.md](../../CONTRIBUTING.md)。

## 📝 许可证

本项目采用**MIT许可证** - 详见[LICENSE](../../LICENSE)文件。

**摘要:** 您可以自由使用、修改和分发此代码,但必须包含原始版权声明,且不能追究作者责任。

## 🙏 致谢

### 构建工具
- [obs-websocket-py](https://github.com/Elektordi/obs-websocket-py) - OBS WebSocket的Python客户端
- [Google Gemini API](https://ai.google.dev/) - AI驱动的高光分析
- [FFmpeg](https://ffmpeg.org/) - 视频处理引擎

### AI协助
本项目的部分代码是在AI语言模型(Google Gemini, Claude)的协助下创建的,以加速开发并提高代码质量。所有AI生成的代码都经过审查、测试并为此特定用例进行了调整。

---

**由玩家为玩家用❤️制作。**

**如果觉得有用,请给此仓库点个星⭐!**
