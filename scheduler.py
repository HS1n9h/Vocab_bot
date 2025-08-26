#!/usr/bin/env python3
"""
Scheduler module for Daily Vocabulary Bot.
Handles automated execution and scheduling of vocabulary delivery.
"""

import schedule
import time
import logging
import threading
from datetime import datetime, time as dt_time
from typing import Optional, Callable
from config import Config

logger = logging.getLogger(__name__)

class Scheduler:
    """Manages scheduling and automated execution of the vocabulary bot."""
    
    def __init__(self):
        """Initialize the scheduler."""
        self.schedule_time = self._parse_schedule_time(Config.SCHEDULE_TIME)
        self.is_running = False
        self.scheduler_thread = None
        self.job = None
        
    def _parse_schedule_time(self, time_str: str) -> dt_time:
        """Parse schedule time string (HH:MM) into time object."""
        try:
            hour, minute = map(int, time_str.split(':'))
            return dt_time(hour, minute)
        except (ValueError, AttributeError):
            logger.warning(f"Invalid schedule time format: {time_str}. Using default 09:00")
            return dt_time(9, 0)
    
    def schedule_daily_job(self, job_function: Callable, time_str: Optional[str] = None):
        """Schedule a daily job at the specified time."""
        if time_str:
            self.schedule_time = self._parse_schedule_time(time_str)
        
        # Clear any existing job
        if self.job:
            schedule.clear()
        
        # Schedule the new job
        self.job = schedule.every().day.at(self.schedule_time.strftime('%H:%M')).do(job_function)
        
        logger.info(f"Daily job scheduled for {self.schedule_time.strftime('%H:%M')}")
        return self.job
    
    def start(self, job_function: Callable):
        """Start the scheduler in a background thread."""
        if self.is_running:
            logger.warning("Scheduler is already running")
            return
        
        # Schedule the job
        self.schedule_daily_job(job_function)
        
        # Start scheduler in background thread
        self.is_running = True
        self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        logger.info("Scheduler started successfully")
    
    def stop(self):
        """Stop the scheduler."""
        if not self.is_running:
            logger.warning("Scheduler is not running")
            return
        
        self.is_running = False
        schedule.clear()
        
        if self.scheduler_thread and self.scheduler_thread.is_alive():
            self.scheduler_thread.join(timeout=5)
        
        logger.info("Scheduler stopped")
    
    def _run_scheduler(self):
        """Run the scheduler loop in the background thread."""
        logger.info("Scheduler loop started")
        
        while self.is_running:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except Exception as e:
                logger.error(f"Error in scheduler loop: {e}")
                time.sleep(60)  # Wait before retrying
        
        logger.info("Scheduler loop stopped")
    
    def get_next_run(self) -> Optional[datetime]:
        """Get the next scheduled run time."""
        if not self.job:
            return None
        
        try:
            # Get the next run time from the job
            next_run = schedule.next_run()
            return next_run
        except Exception as e:
            logger.error(f"Error getting next run time: {e}")
            return None
    
    def get_schedule_info(self) -> dict:
        """Get current schedule information."""
        next_run = self.get_next_run()
        
        return {
            'is_running': self.is_running,
            'schedule_time': self.schedule_time.strftime('%H:%M'),
            'next_run': next_run.isoformat() if next_run else None,
            'has_job': self.job is not None
        }
    
    def run_now(self, job_function: Callable):
        """Run the job immediately."""
        try:
            logger.info("Running job immediately")
            job_function()
            logger.info("Job completed successfully")
        except Exception as e:
            logger.error(f"Error running job: {e}")
    
    def add_one_time_job(self, job_function: Callable, delay_minutes: int):
        """Add a one-time job to run after a delay."""
        try:
            schedule.every(delay_minutes).minutes.do(job_function)
            logger.info(f"One-time job scheduled for {delay_minutes} minutes from now")
        except Exception as e:
            logger.error(f"Error scheduling one-time job: {e}")
    
    def clear_all_jobs(self):
        """Clear all scheduled jobs."""
        try:
            schedule.clear()
            self.job = None
            logger.info("All scheduled jobs cleared")
        except Exception as e:
            logger.error(f"Error clearing jobs: {e}")
    
    def list_jobs(self) -> list:
        """List all scheduled jobs."""
        try:
            jobs = schedule.get_jobs()
            job_list = []
            
            for job in jobs:
                job_info = {
                    'function': job.job_func.__name__,
                    'next_run': job.next_run.isoformat() if job.next_run else None,
                    'interval': str(job.interval),
                    'unit': job.unit
                }
                job_list.append(job_info)
            
            return job_list
        except Exception as e:
            logger.error(f"Error listing jobs: {e}")
            return []

def run_scheduled_bot():
    """Function to run the vocabulary bot (used by scheduler)."""
    try:
        from main import main
        logger.info("Running scheduled vocabulary bot")
        success = main()
        
        if success:
            logger.info("Scheduled bot run completed successfully")
        else:
            logger.error("Scheduled bot run failed")
            
    except Exception as e:
        logger.error(f"Error in scheduled bot run: {e}")

def main():
    """Main function for the scheduler."""
    print("🕐 Daily Vocabulary Bot Scheduler")
    print("=" * 40)
    
    # Initialize scheduler
    scheduler = Scheduler()
    
    try:
        # Schedule the daily job
        scheduler.schedule_daily_job(run_scheduled_bot)
        
        print(f"✅ Daily job scheduled for {scheduler.schedule_time.strftime('%H:%M')}")
        print("🚀 Starting scheduler...")
        
        # Start the scheduler
        scheduler.start(run_scheduled_bot)
        
        # Keep the main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n⏹️ Stopping scheduler...")
            scheduler.stop()
            print("👋 Scheduler stopped. Goodbye!")
            
    except Exception as e:
        print(f"❌ Scheduler error: {e}")
        logger.error(f"Scheduler error: {e}")

if __name__ == "__main__":
    main()
