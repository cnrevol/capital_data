"""
Logging Module

Provides centralized logging functionality for the portfolio backtesting system.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime


class PortfolioLogger:
    """
    Portfolio Logger Class
    
    Manages logging configuration and provides logging utilities.
    """
    
    _loggers = {}
    
    @classmethod
    def get_logger(cls, name='portfolio', log_dir='./logs', log_level=logging.INFO):
        """
        Get or create a logger instance
        
        Args:
            name: Logger name
            log_dir: Directory to store log files
            log_level: Logging level
            
        Returns:
            logging.Logger: Logger instance
        """
        if name in cls._loggers:
            return cls._loggers[name]
        
        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(log_level)
        
        # Avoid duplicate handlers
        if logger.handlers:
            cls._loggers[name] = logger
            return logger
        
        # Create log directory
        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)
        
        # Create formatters
        # Console formatter without emoji and special characters
        console_formatter = logging.Formatter(
            fmt='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # File formatter with more details
        file_formatter = logging.Formatter(
            fmt='%(asctime)s [%(levelname)s] %(name)s - %(filename)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        # File handler - daily rotating log file
        log_filename = f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(
            log_path / log_filename,
            encoding='utf-8'
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        # Store logger
        cls._loggers[name] = logger
        
        return logger
    
    @classmethod
    def cleanup_old_logs(cls, log_dir='./logs', days_to_keep=30):
        """
        Clean up old log files
        
        Args:
            log_dir: Log directory
            days_to_keep: Number of days to keep logs
        """
        log_path = Path(log_dir)
        if not log_path.exists():
            return
        
        cutoff_date = datetime.now().timestamp() - (days_to_keep * 86400)
        
        for log_file in log_path.glob('*.log'):
            if log_file.stat().st_mtime < cutoff_date:
                try:
                    log_file.unlink()
                except Exception:
                    pass


def get_logger(name='portfolio', log_dir='./logs', log_level=logging.INFO):
    """
    Convenience function to get a logger
    
    Args:
        name: Logger name
        log_dir: Directory to store log files
        log_level: Logging level
        
    Returns:
        logging.Logger: Logger instance
    """
    return PortfolioLogger.get_logger(name, log_dir, log_level)


if __name__ == '__main__':
    # Test logging
    logger = get_logger('test')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.debug('This is a debug message')