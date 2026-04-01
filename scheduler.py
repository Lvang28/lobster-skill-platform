"""
龙虾 Skill 合集平台 - 定时任务调度器
每日 3 次推送待办清单和推荐技能（10:30、14:00、17:00）
"""
import schedule
import time
import threading
from datetime import datetime
from models import init_db, User
from config import DATABASE_URL
from services import RecommendationService, UserService


class TaskScheduler:
    """定时任务调度器"""
    
    def __init__(self):
        self.db_session = init_db(DATABASE_URL)
        self.user_service = UserService(self.db_session)
        self.recommendation_service = RecommendationService(self.db_session)
        self.running = False
    
    def send_daily_recommendations(self):
        """发送每日推荐（模拟推送）"""
        print(f"\n⏰ [{datetime.now()}] 执行每日推荐任务...")
        
        # 获取所有用户
        users = self.db_session.query(User).all()
        
        for user in users:
            # 为每个用户生成推荐
            recommendations = self.recommendation_service.generate_daily_recommendations(user.id)
            
            if recommendations:
                skill_names = [s.name for s in recommendations]
                print(f"  👤 {user.username}: 推荐了 {len(recommendations)} 个技能")
                print(f"     技能：{', '.join(skill_names)}")
                
                # TODO: 这里可以集成邮件、短信、IM 等推送方式
                # 例如：发送邮件通知、发送钉钉消息等
        
        print("✓ 每日推荐任务完成\n")
    
    def crawl_hot_skills(self):
        """抓取网络热门技能"""
        print(f"\n🕷️  [{datetime.now()}] 执行网络热门技能抓取...")
        
        from crawler import daily_crawl_task
        added_count = daily_crawl_task()
        
        print(f"✓ 网络热门技能抓取完成，新增 {added_count} 个技能\n")
    
    def cleanup_database(self):
        """清理数据库（定期维护）"""
        print(f"\n🧹 [{datetime.now()}] 执行数据库清理...")
        
        # TODO: 实现过期数据清理
        # - 清理过期的推荐记录
        # - 清理临时文件
        # - 优化数据库
        
        print("✓ 数据库清理完成\n")
    
    def sync_data(self):
        """同步数据"""
        print(f"\n🔄 [{datetime.now()}] 执行数据同步...")
        
        from sync import auto_sync
        auto_sync()
        
        print("✓ 数据同步完成\n")
    
    def setup_schedule(self):
        """设置定时任务"""
        # 每日推荐任务 - 10:30, 14:00, 17:00
        schedule.every().day.at("10:30").do(self.send_daily_recommendations)
        schedule.every().day.at("14:00").do(self.send_daily_recommendations)
        schedule.every().day.at("17:00").do(self.send_daily_recommendations)
        
        # 每日凌晨 3 点抓取网络热门技能
        schedule.every().day.at("03:00").do(self.crawl_hot_skills)
        
        # 每日清理任务 - 凌晨 2 点
        schedule.every().day.at("02:00").do(self.cleanup_database)
        
        # 每 6 小时同步一次数据
        schedule.every(6).hours.do(self.sync_data)
        
        print("\n✓ 定时任务已设置:")
        print("  - 10:30 - 发送每日推荐")
        print("  - 14:00 - 发送每日推荐")
        print("  - 17:00 - 发送每日推荐")
        print("  - 03:00 - 抓取网络热门技能")
        print("  - 02:00 - 数据库清理")
        print("  - 每 6 小时 - 数据同步")
    
    def run(self):
        """运行调度器"""
        self.running = True
        self.setup_schedule()
        
        print("\n🚀 定时任务调度器已启动，按 Ctrl+C 停止...\n")
        
        while self.running:
            schedule.run_pending()
            time.sleep(1)
    
    def stop(self):
        """停止调度器"""
        self.running = False
        print("\n⏸️  定时任务调度器已停止")
    
    def run_once(self, task_name):
        """立即执行一次指定任务"""
        if task_name == 'recommendations':
            self.send_daily_recommendations()
        elif task_name == 'cleanup':
            self.cleanup_database()
        elif task_name == 'sync':
            self.sync_data()
        else:
            print(f"⚠️  未知任务：{task_name}")


def start_scheduler():
    """启动调度器（独立线程）"""
    scheduler = TaskScheduler()
    thread = threading.Thread(target=scheduler.run, daemon=True)
    thread.start()
    return scheduler


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        # 命令行执行特定任务
        scheduler = TaskScheduler()
        task = sys.argv[1]
        scheduler.run_once(task)
    else:
        # 启动持续运行的调度器
        scheduler = TaskScheduler()
        try:
            scheduler.run()
        except KeyboardInterrupt:
            scheduler.stop()
