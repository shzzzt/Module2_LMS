"""
Post Service
Handles all post-related data operations (materials, assessments, announcements)
"""
import json
import os
from typing import List, Dict, Optional
from datetime import datetime


class PostService:
    def __init__(self):
        self.data_file = 'data/posts.json'
        self._ensure_data_file()
    
    def _ensure_data_file(self):
        """Ensure the data file exists with initial structure"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        if not os.path.exists(self.data_file):
            initial_data = {
                "posts": [
                    {
                        "post_id": 1,
                        "class_id": 1,
                        "topic_id": None,
                        "type": "material",
                        "title": "Desktop Project Guidelines",
                        "description": "Please ensure that the task is completed according to the requirements provided, keeping everything consistent and aligned throughout the process. Make sure to follow the necessary steps as outlined, review your work before finalizing, and confirm that it meets the expected standards.",
                        "instructor": "Carlos Fidel Castro",
                        "instructor_id": "faculty_001",
                        "date_posted": "2024-08-18",
                        "attachment": {
                            "filename": "desktop_project_guidelines.pdf",
                            "file_type": "pdf",
                            "file_path": "attachments/desktop_project_guidelines.pdf"
                        },
                        "status": "published",
                        "created_at": "2024-08-18T10:00:00",
                        "updated_at": "2024-08-18T10:00:00"
                    },
                    {
                        "post_id": 2,
                        "class_id": 1,
                        "topic_id": 1,
                        "type": "material",
                        "title": "Chapter 2: Basics",
                        "description": "This chapter covers the fundamental concepts of desktop application development.",
                        "instructor": "Carlos Fidel Castro",
                        "instructor_id": "faculty_001",
                        "date_posted": "2024-08-25",
                        "attachment": {
                            "filename": "chapter_2_basics.pdf",
                            "file_type": "pdf",
                            "file_path": "attachments/chapter_2_basics.pdf"
                        },
                        "status": "published",
                        "created_at": "2024-08-25T09:00:00",
                        "updated_at": "2024-08-25T09:00:00"
                    },
                    {
                        "post_id": 3,
                        "class_id": 1,
                        "topic_id": 2,
                        "type": "material",
                        "title": "Chapter 3: Advanced Concepts",
                        "description": "Advanced topics in desktop application development including UI/UX design patterns.",
                        "instructor": "Carlos Fidel Castro",
                        "instructor_id": "faculty_001",
                        "date_posted": "2024-09-01",
                        "attachment": {
                            "filename": "chapter_3_advanced.pdf",
                            "file_type": "pdf",
                            "file_path": "attachments/chapter_3_advanced.pdf"
                        },
                        "status": "published",
                        "created_at": "2024-09-01T11:00:00",
                        "updated_at": "2024-09-01T11:00:00"
                    },
                    {
                        "post_id": 4,
                        "class_id": 1,
                        "topic_id": 2,
                        "type": "assessment",
                        "title": "Midterm Exam",
                        "description": "Comprehensive examination covering chapters 1-5. Duration: 2 hours. Please bring your student ID and writing materials.",
                        "instructor": "Carlos Fidel Castro",
                        "instructor_id": "faculty_001",
                        "date_posted": "2024-09-08",
                        "due_date": "2024-09-20",
                        "points": 100,
                        "attachment": {
                            "filename": "midterm_exam_guide.pdf",
                            "file_type": "pdf",
                            "file_path": "attachments/midterm_exam_guide.pdf"
                        },
                        "status": "published",
                        "created_at": "2024-09-08T14:00:00",
                        "updated_at": "2024-09-08T14:00:00"
                    },
                    {
                        "post_id": 5,
                        "class_id": 1,
                        "topic_id": None,
                        "type": "assessment",
                        "title": "Practice Test",
                        "description": "Practice test to prepare for the midterm examination. This is not graded but highly recommended.",
                        "instructor": "Carlos Fidel Castro",
                        "instructor_id": "faculty_001",
                        "date_posted": "2024-09-10",
                        "due_date": "2024-09-15",
                        "points": 50,
                        "attachment": {
                            "filename": "practice_test.pdf",
                            "file_type": "pdf",
                            "file_path": "attachments/practice_test.pdf"
                        },
                        "status": "published",
                        "created_at": "2024-09-10T10:30:00",
                        "updated_at": "2024-09-10T10:30:00"
                    }
                ],
                "comments": [
                    {
                        "comment_id": 1,
                        "post_id": 1,
                        "user_id": "student_001",
                        "user_name": "John Student",
                        "comment_text": "Thank you for the guidelines! Very helpful.",
                        "created_at": "2024-08-19T08:30:00"
                    },
                    {
                        "comment_id": 2,
                        "post_id": 1,
                        "user_id": "faculty_001",
                        "user_name": "Carlos Fidel Castro",
                        "comment_text": "You're welcome! Feel free to ask if you have any questions.",
                        "created_at": "2024-08-19T09:00:00"
                    }
                ]
            }
            self._save_data(initial_data)
    
    def _load_data(self) -> Dict:
        """Load data from JSON file"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"posts": [], "comments": []}
    
    def _save_data(self, data: Dict):
        """Save data to JSON file"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    
    def get_posts_by_class(self, class_id: int, post_type: str = None) -> List[Dict]:
        """Get all posts for a specific class, optionally filtered by type"""
        data = self._load_data()
        posts = data.get('posts', [])
        
        # Filter by class and status
        filtered_posts = [
            post for post in posts 
            if post.get('class_id') == class_id and post.get('status') == 'published'
        ]
        
        # Filter by type if specified
        if post_type:
            filtered_posts = [post for post in filtered_posts if post.get('type') == post_type]
        
        # Sort by date posted (newest first)
        filtered_posts.sort(key=lambda x: x.get('date_posted', ''), reverse=True)
        
        return filtered_posts
    
    def get_posts_by_topic(self, topic_id: int) -> List[Dict]:
        """Get all posts for a specific topic"""
        data = self._load_data()
        posts = data.get('posts', [])
        
        filtered_posts = [
            post for post in posts 
            if post.get('topic_id') == topic_id and post.get('status') == 'published'
        ]
        
        # Sort by date posted
        filtered_posts.sort(key=lambda x: x.get('date_posted', ''))
        
        return filtered_posts
    
    def get_untitled_posts(self, class_id: int) -> List[Dict]:
        """Get posts that don't belong to any topic"""
        data = self._load_data()
        posts = data.get('posts', [])
        
        filtered_posts = [
            post for post in posts 
            if (post.get('class_id') == class_id and 
                post.get('topic_id') is None and 
                post.get('status') == 'published')
        ]
        
        # Sort by date posted (newest first)
        filtered_posts.sort(key=lambda x: x.get('date_posted', ''), reverse=True)
        
        return filtered_posts
    
    def get_post_by_id(self, post_id: int) -> Optional[Dict]:
        """Get a specific post by ID"""
        data = self._load_data()
        posts = data.get('posts', [])
        
        for post in posts:
            if post.get('post_id') == post_id:
                # Include comments
                comments = self.get_post_comments(post_id)
                post_with_comments = post.copy()
                post_with_comments['comments'] = comments
                return post_with_comments
        return None
    
    def create_post(self, post_data: Dict) -> int:
        """Create a new post"""
        data = self._load_data()
        posts = data.get('posts', [])
        
        # Generate new post ID
        max_id = max([post.get('post_id', 0) for post in posts] + [0])
        new_post_id = max_id + 1
        
        new_post = {
            'post_id': new_post_id,
            'date_posted': datetime.now().strftime('%Y-%m-%d'),
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'status': 'published',
            **post_data
        }
        
        posts.append(new_post)
        data['posts'] = posts
        self._save_data(data)
        
        return new_post_id
    
    def update_post(self, post_id: int, updates: Dict) -> bool:
        """Update an existing post"""
        data = self._load_data()
        posts = data.get('posts', [])
        
        for i, post in enumerate(posts):
            if post.get('post_id') == post_id:
                posts[i].update(updates)
                posts[i]['updated_at'] = datetime.now().isoformat()
                data['posts'] = posts
                self._save_data(data)
                return True
        return False
    
    def delete_post(self, post_id: int) -> bool:
        """Delete a post (mark as deleted)"""
        return self.update_post(post_id, {'status': 'deleted'})
    
    def get_post_comments(self, post_id: int) -> List[Dict]:
        """Get all comments for a specific post"""
        data = self._load_data()
        comments = data.get('comments', [])
        
        post_comments = [comment for comment in comments if comment.get('post_id') == post_id]
        # Sort by creation date
        post_comments.sort(key=lambda x: x.get('created_at', ''))
        
        return post_comments
    
    def add_comment(self, post_id: int, comment_text: str, user_id: str, user_name: str = None) -> int:
        """Add a comment to a post"""
        data = self._load_data()
        comments = data.get('comments', [])
        
        # Generate new comment ID
        max_id = max([comment.get('comment_id', 0) for comment in comments] + [0])
        new_comment_id = max_id + 1
        
        new_comment = {
            'comment_id': new_comment_id,
            'post_id': post_id,
            'user_id': user_id,
            'user_name': user_name or f"User {user_id}",
            'comment_text': comment_text,
            'created_at': datetime.now().isoformat()
        }
        
        comments.append(new_comment)
        data['comments'] = comments
        self._save_data(data)
        
        return new_comment_id
    
    def delete_comment(self, comment_id: int) -> bool:
        """Delete a comment"""
        data = self._load_data()
        comments = data.get('comments', [])
        
        data['comments'] = [c for c in comments if c.get('comment_id') != comment_id]
        self._save_data(data)
        return True
    
    def format_post_for_display(self, post: Dict) -> Dict:
        """Format post data for display in UI components"""
        attachment = post.get('attachment', {})
        
        formatted_post = {
            'type': post.get('type', 'material'),
            'title': post.get('title', 'Untitled'),
            'instructor': post.get('instructor', 'Unknown Instructor'),
            'date': post.get('date_posted', ''),
            'description': post.get('description', ''),
            'attachment': attachment.get('filename', ''),
            'score': str(post.get('points', '')) if post.get('type') == 'assessment' else None
        }
        
        return formatted_post