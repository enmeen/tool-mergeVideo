# 新北境战神视频处理工具

## 环境要求
- Python 3.8+
- FFmpeg (必需)

## 安装说明

1. 安装 FFmpeg (必需)
- Windows: 
  1. 下载 FFmpeg: https://ffmpeg.org/download.html
  2. 添加到系统环境变量
- Mac: `brew install ffmpeg`
- Linux: `sudo apt install ffmpeg`

2. 确认安装
```
ffmpeg -version
```

## 使用说明

### 目录结构准备
```
项目目录/
  ├── source/                # 源视频目录
  │   ├── 第1集/            # 分集目录
  │   │   ├── 1.mp4
  │   │   ├── 2.mp4
  │   │   └── ...
  │   ├── 第2集/
  │   └── ...
  ├── output/               # 输出目录(自动创建)
  └── video_merger.py       # 合并脚本
```

### 使用步骤

1. 准备源文件
   - 在 source 目录下创建分集目录
   - 将需要合并的视频文件放入对应的分集目录
   - 确保视频文件名能按正确顺序排序(如: 1.mp4, 2.mp4...)

2. 运行脚本
   ```
   python video_merger.py
   ```
   或指定自定义源目录:
   ```
   python video_merger.py --source 自定义源目录路径
   ```

3. 查看结果
   - 合并后的视频将保存在 output 目录
   - 输出文件名格式: "（合集）分集目录名.mp4"
   - 每个分集目录下会生成 done.md 记录处理记录
   - merge.log 记录详细处理日志

### 注意事项

1. 确保有足够的磁盘空间(至少需要源视频总大小的1.2倍)
2. 支持的视频格式: mp4, avi, mov, mkv
3. 如果目录下已存在 done.md，该目录将被跳过处理
4. 合并过程中请勿移动或修改源文件

### 处理记录

- done.md: 记录视频合并顺序
- merge.log: 记录详细处理过程和任何错误信息

如遇到问题，请查看 merge.log 了解详细信息。