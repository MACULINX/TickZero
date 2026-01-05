"""
MatchDatabase: SQLite database manager for CS2 match history.
Stores match metadata, video paths, statistics, and generated highlights.
"""
import sqlite3
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MatchDatabase:
    """Manages SQLite database for match history and highlights."""
    
    def __init__(self, db_path="matches.db"):
        """
        Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.init_database()
        logger.info(f"✓ Match database initialized: {db_path}")
    
    def init_database(self):
        """Create database tables if they don't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create matches table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS matches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                match_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                video_path TEXT NOT NULL,
                log_path TEXT NOT NULL,
                duration_seconds REAL,
                total_kills INTEGER DEFAULT 0,
                total_deaths INTEGER DEFAULT 0,
                total_rounds INTEGER DEFAULT 0,
                map_name TEXT,
                player_steamid TEXT,
                player_name TEXT,
                processed BOOLEAN DEFAULT 0,
                highlights_generated INTEGER DEFAULT 0,
                notes TEXT
            )
        ''')
        
        # Create highlights table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS highlights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                match_id INTEGER NOT NULL,
                clip_path TEXT NOT NULL,
                start_time REAL NOT NULL,
                end_time REAL NOT NULL,
                label TEXT,
                priority INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (match_id) REFERENCES matches(id)
            )
        ''')
        
        # Create index for faster queries
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_match_date ON matches(match_date DESC)
        ''')
        
        conn.commit()
        conn.close()
    
    def save_match(self, video_path: str, log_path: str, match_stats: Optional[Dict] = None) -> int:
        """
        Save a new match to the database.
        
        Args:
            video_path: Path to recorded video file
            log_path: Path to match_log.json file
            match_stats: Dictionary with match statistics
            
        Returns:
            int: ID of the saved match
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Extract statistics from match_stats or parse log file
        if match_stats is None:
            match_stats = self._parse_match_log(log_path)
        
        cursor.execute('''
            INSERT INTO matches (
                video_path, log_path, duration_seconds, total_kills,
                total_deaths, total_rounds, map_name, player_steamid, player_name
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            video_path,
            log_path,
            match_stats.get('duration_seconds', 0),
            match_stats.get('total_kills', 0),
            match_stats.get('total_deaths', 0),
            match_stats.get('total_rounds', 0),
            match_stats.get('map_name'),
            match_stats.get('player_steamid'),
            match_stats.get('player_name')
        ))
        
        match_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        logger.info(f"✓ Saved match #{match_id} to database")
        return match_id
    
    def _parse_match_log(self, log_path: str) -> Dict[str, Any]:
        """
        Parse match_log.json to extract statistics.
        
        Args:
            log_path: Path to match log JSON file
            
        Returns:
            dict: Extracted statistics
        """
        try:
            with open(log_path, 'r') as f:
                data = json.load(f)
            
            events = data.get('events', [])
            
            # Count kills and find player info
            kills = [e for e in events if e.get('type') == 'kill']
            rounds = set(e.get('round', 0) for e in events if 'round' in e)
            
            # Calculate duration from last event
            duration = 0
            if events:
                last_event = events[-1]
                duration = last_event.get('video_time', 0)
            
            # Extract player info (from first event if available)
            player_steamid = None
            player_name = None
            # This would need to be added to GSI server in future
            
            return {
                'total_kills': len(kills),
                'total_deaths': 0,  # Not tracked yet
                'total_rounds': len(rounds),
                'duration_seconds': duration,
                'map_name': None,  # Not tracked yet
                'player_steamid': player_steamid,
                'player_name': player_name
            }
            
        except Exception as e:
            logger.error(f"Error parsing match log: {e}")
            return {}
    
    def get_all_matches(self, limit: int = 50, processed_only: bool = False) -> List[Dict]:
        """
        Retrieve all matches from database.
        
        Args:
            limit: Maximum number of matches to return
            processed_only: Only return processed matches
            
        Returns:
            list: List of match dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        cursor = conn.cursor()
        
        query = "SELECT * FROM matches"
        if processed_only:
            query += " WHERE processed = 1"
        query += " ORDER BY match_date DESC LIMIT ?"
        
        cursor.execute(query, (limit,))
        matches = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return matches
    
    def get_match(self, match_id: int) -> Optional[Dict]:
        """
        Get specific match by ID.
        
        Args:
            match_id: Match ID
            
        Returns:
            dict: Match data or None if not found
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM matches WHERE id = ?", (match_id,))
        row = cursor.fetchone()
        
        conn.close()
        return dict(row) if row else None
    
    def get_match_events(self, match_id: int) -> List[Dict]:
        """
        Get all events for a specific match from its log file.
        
        Args:
            match_id: Match ID
            
        Returns:
            list: List of event dictionaries
        """
        match = self.get_match(match_id)
        if not match:
            return []
        
        try:
            with open(match['log_path'], 'r') as f:
                data = json.load(f)
            return data.get('events', [])
        except Exception as e:
            logger.error(f"Error loading match events: {e}")
            return []
    
    def update_match(self, match_id: int, **kwargs):
        """
        Update match fields.
        
        Args:
            match_id: Match ID
            **kwargs: Fields to update (processed, highlights_generated, notes, etc.)
        """
        if not kwargs:
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Build UPDATE query dynamically
        fields = ', '.join(f"{k} = ?" for k in kwargs.keys())
        values = list(kwargs.values()) + [match_id]
        
        cursor.execute(f"UPDATE matches SET {fields} WHERE id = ?", values)
        conn.commit()
        conn.close()
        
        logger.info(f"✓ Updated match #{match_id}")
    
    def save_highlight(self, match_id: int, clip_path: str, start_time: float, 
                      end_time: float, label: str = "", priority: int = 5):
        """
        Save generated highlight clip to database.
        
        Args:
            match_id: Associated match ID
            clip_path: Path to generated clip
            start_time: Start timestamp
            end_time: End timestamp
            label: Clip label/description
            priority: Clip priority (1-10)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO highlights (match_id, clip_path, start_time, end_time, label, priority)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (match_id, clip_path, start_time, end_time, label, priority))
        
        conn.commit()
        conn.close()
        
        # Update match highlights count
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE matches 
            SET highlights_generated = (SELECT COUNT(*) FROM highlights WHERE match_id = ?)
            WHERE id = ?
        ''', (match_id, match_id))
        conn.commit()
        conn.close()
    
    def delete_match(self, match_id: int):
        """
        Delete match and associated highlights.
        
        Args:
            match_id: Match ID to delete
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Delete highlights first (foreign key)
        cursor.execute("DELETE FROM highlights WHERE match_id = ?", (match_id,))
        # Delete match
        cursor.execute("DELETE FROM matches WHERE id = ?", (match_id,))
        
        conn.commit()
        conn.close()
        
        logger.info(f"✓ Deleted match #{match_id}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get overall statistics across all matches.
        
        Returns:
            dict: Statistics summary
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total matches
        cursor.execute("SELECT COUNT(*) FROM matches")
        total_matches = cursor.fetchone()[0]
        
        # Total kills
        cursor.execute("SELECT SUM(total_kills) FROM matches")
        total_kills = cursor.fetchone()[0] or 0
        
        # Total highlights
        cursor.execute("SELECT COUNT(*) FROM highlights")
        total_highlights = cursor.fetchone()[0]
        
        # Total duration
        cursor.execute("SELECT SUM(duration_seconds) FROM matches")
        total_duration = cursor.fetchone()[0] or 0
        
        # Pending (not processed)
        cursor.execute("SELECT COUNT(*) FROM matches WHERE processed = 0")
        pending_matches = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_matches': total_matches,
            'total_kills': total_kills,
            'total_highlights': total_highlights,
            'total_duration_hours': total_duration / 3600,
            'pending_matches': pending_matches
        }
