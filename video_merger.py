import os
import subprocess
import logging
from pathlib import Path
import re
import shutil
import argparse

def setup_logging(directory):
    log_file = os.path.join(directory, 'merge.log')
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def check_ffmpeg():
    """检查ffmpeg是否正确安装"""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True)
        return True
    except:
        print("警告: ffmpeg未正确安装或未添加到系统路径")
        return False

def natural_sort_key(filename):
    """实现更智能的自然排序"""
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    return [convert(c) for c in re.split('([0-9]+)', os.path.basename(filename))]

def process_directory(directory, args):
    setup_logging(directory)
    logging.info(f"开始处理目录: {directory}")
    
    if not check_ffmpeg():
        logging.error("错误: 请确保ffmpeg已正确安装")
        return
    
    if os.path.exists(os.path.join(directory, 'done.md')):
        logging.info(f"目录 {directory} 已处理过，跳过")
        return
    
    # 获取当前目录名
    current_dir = Path(directory).name
    
    # 创建输出目录（与source同级）
    output_dir = Path(args.source).parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    # 构建输出文件名：（合集）目录名.mp4
    output_filename = f"（合集）{current_dir}.mp4"
    output_path = output_dir / output_filename
    
    # 获取视频文件
    video_files = []
    for file in os.listdir(directory):
        if file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            video_files.append(os.path.join(directory, file))
    
    if not video_files:
        logging.info(f"目录 {directory} 中未找到视频文件")
        return
    
    # 按数字排序
    video_files.sort(key=natural_sort_key)
    
    # 输出合并顺序
    logging.info(f"\n{'='*50}\n合并顺序如下：")
    for i, video in enumerate(video_files, 1):
        filename = os.path.basename(video)
        logging.info(f"{i:02d}. {filename}")
    logging.info(f"{'='*50}\n")
    
    # 检查磁盘空间
    total_video_size = sum(os.path.getsize(f) for f in video_files)
    free_space = shutil.disk_usage(output_dir).free
    if free_space < total_video_size * 1.2:
        logging.error(f"磁盘空间不足。需要: {total_video_size*1.2/(1024**3):.2f}GB, 可用: {free_space/(1024**3):.2f}GB")
        return
    
    try:
        # 创建合并列表文件
        concat_file = os.path.join(directory, 'concat.txt')
        with open(concat_file, 'w', encoding='utf-8') as f:
            for video in video_files:
                abs_path = os.path.abspath(video)
                escaped_path = abs_path.replace("'", "'\\''")
                f.write(f"file '{escaped_path}'\n")
        
        # 使用ffmpeg直接拼接
        cmd = [
            'ffmpeg', '-f', 'concat', '-safe', '0',
            '-i', concat_file,
            '-c', 'copy',
            '-map', '0',
            '-y',
            str(output_path)
        ]
        
        logging.info(f"开始合并视频到: {output_path}")
        process = subprocess.run(cmd, capture_output=True, text=True)
        
        if process.returncode != 0:
            raise Exception(f"FFmpeg错误: {process.stderr}")
        
        # 清理concat文件
        os.remove(concat_file)
        
        # 创建done.md，同时记录合并顺序
        with open(os.path.join(directory, 'done.md'), 'w', encoding='utf-8') as f:
            f.write(f"视频合并完成\n输出文件：{output_path}\n\n合并顺序：\n")
            for i, video in enumerate(video_files, 1):
                f.write(f"{i:02d}. {os.path.basename(video)}\n")
        
        logging.info(f"目录 {directory} 处理完成，输出文件：{output_path}")
        
    except Exception as e:
        logging.error(f"处理目录 {directory} 时出现错误: {str(e)}")
        if os.path.exists(concat_file):
            os.remove(concat_file)

def process_source_directories(source_root, args):
    if not os.path.exists(source_root):
        print(f"源目录 {source_root} 不存在")
        return
    
    for item in os.listdir(source_root):
        item_path = os.path.join(source_root, item)
        if os.path.isdir(item_path):
            print(f"开始处理目录: {item_path}")
            process_directory(item_path, args)

def parse_args():
    parser = argparse.ArgumentParser(description='视频合并工具')
    parser.add_argument('--source', default='source', help='源目录路径')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    process_source_directories(args.source, args) 