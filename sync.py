"""
龙虾 Skill 合集平台 - 数据同步工具
支持多种同步方式：本地备份、GitHub、云存储
"""
import os
import json
import shutil
import zipfile
import requests
from datetime import datetime
from config import DATA_DIR, BACKUP_DIR, GITHUB_CONFIG, CLOUD_STORAGE_CONFIG


class DataSync:
    """数据同步服务"""
    
    def __init__(self):
        self.data_dir = DATA_DIR
        self.backup_dir = BACKUP_DIR
    
    def create_backup(self):
        """创建本地备份"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(self.backup_dir, f'backup_{timestamp}.zip')
        
        with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 添加数据库文件
            db_path = os.path.join(self.data_dir, 'lobster_platform.db')
            if os.path.exists(db_path):
                zipf.write(db_path, 'lobster_platform.db')
            
            # 添加 skills 目录
            skills_dir = os.path.join(self.data_dir, 'skills')
            if os.path.exists(skills_dir):
                for root, dirs, files in os.walk(skills_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, self.data_dir)
                        zipf.write(file_path, arcname)
        
        print(f"✓ 备份已创建：{backup_file}")
        return backup_file
    
    def export_platform_data(self, output_path=None):
        """导出平台数据（用于分享）"""
        if not output_path:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = os.path.join(self.backup_dir, f'platform_export_{timestamp}.zip')
        
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 添加数据库
            db_path = os.path.join(self.data_dir, 'lobster_platform.db')
            if os.path.exists(db_path):
                zipf.write(db_path, 'data/lobster_platform.db')
            
            # 添加 skills
            skills_dir = os.path.join(self.data_dir, 'skills')
            if os.path.exists(skills_dir):
                for root, dirs, files in os.walk(skills_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, self.data_dir)
                        zipf.write(file_path, f'data/{arcname}')
            
            # 添加配置信息
            config_info = {
                'export_time': datetime.now().isoformat(),
                'version': '1.0.0'
            }
            zipf.writestr('export_info.json', json.dumps(config_info, indent=2))
        
        print(f"✓ 平台数据已导出：{output_path}")
        return output_path
    
    def import_platform_data(self, import_path):
        """导入平台数据"""
        if not os.path.exists(import_path):
            raise FileNotFoundError(f"导入文件不存在：{import_path}")
        
        with zipfile.ZipFile(import_path, 'r') as zipf:
            zipf.extractall(self.data_dir)
        
        print(f"✓ 平台数据已导入：{import_path}")
        return True
    
    def sync_to_github(self):
        """同步到 GitHub（如果配置）"""
        if not GITHUB_CONFIG['enabled']:
            print("⚠️  GitHub 同步未启用")
            return False
        
        # 创建备份
        backup_file = self.create_backup()
        
        # TODO: 实现 GitHub API 上传
        # 需要使用 github REST API 或 PyGithub 库
        print("📤 正在同步到 GitHub...")
        
        return True
    
    def sync_from_github(self):
        """从 GitHub 下载最新数据"""
        if not GITHUB_CONFIG['enabled']:
            print("⚠️  GitHub 同步未启用")
            return False
        
        # TODO: 实现 GitHub API 下载
        print("📥 正在从 GitHub 下载...")
        
        return True
    
    def sync_to_cloud(self):
        """同步到云存储（如果配置）"""
        if not CLOUD_STORAGE_CONFIG['enabled']:
            print("⚠️  云存储同步未启用")
            return False
        
        # TODO: 实现 WebDAV/S3 等云存储同步
        print("📤 正在同步到云存储...")
        
        return True
    
    def cleanup_old_backups(self, keep_days=7):
        """清理旧备份"""
        cutoff_date = datetime.now().timestamp() - (keep_days * 24 * 60 * 60)
        
        for filename in os.listdir(self.backup_dir):
            if filename.startswith('backup_') or filename.startswith('platform_export_'):
                file_path = os.path.join(self.backup_dir, filename)
                file_time = os.path.getmtime(file_path)
                
                if file_time < cutoff_date:
                    os.remove(file_path)
                    print(f"✓ 已删除旧备份：{filename}")


def auto_sync():
    """自动同步任务（每日执行）"""
    sync = DataSync()
    
    print(f"\n🔄 开始自动同步 - {datetime.now()}")
    
    # 创建备份
    sync.create_backup()
    
    # 同步到 GitHub
    if GITHUB_CONFIG['enabled']:
        sync.sync_to_github()
    
    # 同步到云存储
    if CLOUD_STORAGE_CONFIG['enabled']:
        sync.sync_to_cloud()
    
    # 清理旧备份
    sync.cleanup_old_backups(keep_days=7)
    
    print("✓ 自动同步完成\n")


if __name__ == '__main__':
    # 手动执行同步
    auto_sync()
