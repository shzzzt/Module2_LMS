"""
Classroom Service
Handles all classroom-related data operations and business logic
"""
import json
import os
from typing import List, Dict, Optional
from datetime import datetime


class ClassroomService:
    def __init__(self):
        self.data_file = 'data/classrooms.json'
        self._ensure_data_file()
    
    def _ensure_data_file(self):
        """Ensure the data file exists with initial structure"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        if not os.path.exists(self.data_file):
            initial_data = {
                "classes": [
                    {
                        "class_id": 1,
                        "code": "ITSD81",
                        "title": "Desktop Application Development",
                        "section": "BSIT 3C",
                        "instructor": "Neil John Jomaya",
                        "instructor_id": "faculty_001",
                        "schedule": "MONDAY - 1:00 - 4:00 PM",
                        "room": "Room 301",
                        "semester": "2nd Semester",
                        "academic_year": "2024-2025",
                        "status": "active",
                        "created_at": "2024-08-01",
                        "students": ["student_001", "student_002", "student_003"],
                        "recent_posts": "Desktop Project Guidelines posted"
                    },
                    {
                        "class_id": 2,
                        "code": "IT59",
                        "title": "Data Structures and Algorithms",
                        "section": "BSIT 3A",
                        "instructor": "John Doe",
                        "instructor_id": "faculty_002",
                        "schedule": "TUESDAY - 9:00 - 12:00 PM",
                        "room": "Room 205",
                        "semester": "2nd Semester",
                        "academic_year": "2024-2025",
                        "status": "active",
                        "created_at": "2024-08-01",
                        "students": ["student_004", "student_005"],
                        "recent_posts": "No recent posts"
                    },
                    {
                        "class_id": 3,
                        "code": "IT95",
                        "title": "Capstone Project",
                        "section": "BSIT 3A",
                        "instructor": "Jinky",
                        "instructor_id": "faculty_003",
                        "schedule": "WEDNESDAY - 2:00 - 5:00 PM",
                        "room": "Room 404",
                        "semester": "2nd Semester",
                        "academic_year": "2024-2025",
                        "status": "active",
                        "created_at": "2024-08-01",
                        "students": ["student_006", "student_007", "student_008"],
                        "recent_posts": "Project proposal due next week"
                    }
                ],
                "topics": [
                    {
                        "topic_id": 1,
                        "class_id": 1,
                        "title": "Lecture: Topic 1",
                        "description": "Introduction to Desktop Application Development",
                        "created_at": "2024-08-15",
                        "order": 1
                    },
                    {
                        "topic_id": 2,
                        "class_id": 1,
                        "title": "Lecture: Topic 2",
                        "description": "Advanced Concepts in Desktop Development",
                        "created_at": "2024-08-25",
                        "order": 2
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
            return {"classes": [], "topics": []}
    
    def _save_data(self, data: Dict):
        """Save data to JSON file"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    
    def get_classes_by_role(self, user_role: str, user_id: str = None) -> List[Dict]:
        """Get all classes accessible by user role"""
        data = self._load_data()
        classes = data.get('classes', [])
        
        # Filter based on role
        if user_role == "student":
            # For students, filter by enrollment
            if user_id:
                classes = [cls for cls in classes if user_id in cls.get('students', [])]
        elif user_role == "faculty":
            # For faculty, filter by instructor
            if user_id:
                classes = [cls for cls in classes if cls.get('instructor_id') == user_id]
        # Admin can see all classes
        
        # Return only active classes
        return [cls for cls in classes if cls.get('status') == 'active']
    
    def get_class_by_id(self, class_id: int) -> Optional[Dict]:
        """Get a specific class by ID"""
        data = self._load_data()
        classes = data.get('classes', [])
        
        for cls in classes:
            if cls.get('class_id') == class_id:
                return cls
        return None
    
    def create_class(self, class_data: Dict) -> int:
        """Create a new class"""
        data = self._load_data()
        classes = data.get('classes', [])
        
        # Generate new class ID
        max_id = max([cls.get('class_id', 0) for cls in classes] + [0])
        new_class_id = max_id + 1
        
        new_class = {
            'class_id': new_class_id,
            'created_at': datetime.now().strftime('%Y-%m-%d'),
            'status': 'active',
            'students': [],
            'recent_posts': 'No recent posts',
            **class_data
        }
        
        classes.append(new_class)
        data['classes'] = classes
        self._save_data(data)
        
        return new_class_id
    
    def update_class(self, class_id: int, updates: Dict) -> bool:
        """Update an existing class"""
        data = self._load_data()
        classes = data.get('classes', [])
        
        for i, cls in enumerate(classes):
            if cls.get('class_id') == class_id:
                classes[i].update(updates)
                data['classes'] = classes
                self._save_data(data)
                return True
        return False
    
    def delete_class(self, class_id: int) -> bool:
        """Delete a class (mark as deleted)"""
        return self.update_class(class_id, {'status': 'deleted'})
    
    def restore_class(self, class_id: int) -> bool:
        """Restore a deleted class"""
        return self.update_class(class_id, {'status': 'active'})
    
    def get_class_topics(self, class_id: int) -> List[Dict]:
        """Get all topics for a specific class"""
        data = self._load_data()
        topics = data.get('topics', [])
        
        class_topics = [topic for topic in topics if topic.get('class_id') == class_id]
        # Sort by order
        class_topics.sort(key=lambda x: x.get('order', 0))
        
        return class_topics
    
    def create_topic(self, class_id: int, topic_data: Dict) -> int:
        """Create a new topic for a class"""
        data = self._load_data()
        topics = data.get('topics', [])
        
        # Generate new topic ID
        max_id = max([topic.get('topic_id', 0) for topic in topics] + [0])
        new_topic_id = max_id + 1
        
        # Get next order number for this class
        class_topics = [t for t in topics if t.get('class_id') == class_id]
        max_order = max([t.get('order', 0) for t in class_topics] + [0])
        
        new_topic = {
            'topic_id': new_topic_id,
            'class_id': class_id,
            'created_at': datetime.now().strftime('%Y-%m-%d'),
            'order': max_order + 1,
            **topic_data
        }
        
        topics.append(new_topic)
        data['topics'] = topics
        self._save_data(data)
        
        return new_topic_id
    
    def update_topic(self, topic_id: int, updates: Dict) -> bool:
        """Update an existing topic"""
        data = self._load_data()
        topics = data.get('topics', [])
        
        for i, topic in enumerate(topics):
            if topic.get('topic_id') == topic_id:
                topics[i].update(updates)
                data['topics'] = topics
                self._save_data(data)
                return True
        return False
    
    def delete_topic(self, topic_id: int) -> bool:
        """Delete a topic"""
        data = self._load_data()
        topics = data.get('topics', [])
        
        data['topics'] = [t for t in topics if t.get('topic_id') != topic_id]
        self._save_data(data)
        return True
    
    def add_student_to_class(self, class_id: int, student_id: str) -> bool:
        """Add a student to a class"""
        data = self._load_data()
        classes = data.get('classes', [])
        
        for cls in classes:
            if cls.get('class_id') == class_id:
                students = cls.get('students', [])
                if student_id not in students:
                    students.append(student_id)
                    self.update_class(class_id, {'students': students})
                return True
        return False
    
    def remove_student_from_class(self, class_id: int, student_id: str) -> bool:
        """Remove a student from a class"""
        data = self._load_data()
        classes = data.get('classes', [])
        
        for cls in classes:
            if cls.get('class_id') == class_id:
                students = cls.get('students', [])
                if student_id in students:
                    students.remove(student_id)
                    self.update_class(class_id, {'students': students})
                return True
        return False