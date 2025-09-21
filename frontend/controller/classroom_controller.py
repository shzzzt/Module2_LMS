"""
Classroom Controller
Handles all classroom-related business logic and coordinates between views and services
"""
from PyQt6.QtCore import QObject, pyqtSignal
from frontend.services.classroom_service import ClassroomService
from frontend.services.post_service import PostService


class ClassroomController(QObject):
    # Signals for view updates
    classes_updated = pyqtSignal(list)
    posts_updated = pyqtSignal(list)
    post_details_updated = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.classroom_service = ClassroomService()
        self.post_service = PostService()
        
    # Class management methods
    def get_user_classes(self, user_role="student"):
        """Get all classes for the current user"""
        try:
            classes = self.classroom_service.get_classes_by_role(user_role)
            self.classes_updated.emit(classes)
            return classes
        except Exception as e:
            self.error_occurred.emit(f"Failed to load classes: {str(e)}")
            return []
    
    def get_class_details(self, class_id):
        """Get details for a specific class"""
        try:
            return self.classroom_service.get_class_by_id(class_id)
        except Exception as e:
            self.error_occurred.emit(f"Failed to load class details: {str(e)}")
            return None
    
    def restore_class(self, class_data):
        """Restore an archived class"""
        try:
            success = self.classroom_service.restore_class(class_data['class_id'])
            if success:
                # Refresh classes list
                self.get_user_classes()
            return success
        except Exception as e:
            self.error_occurred.emit(f"Failed to restore class: {str(e)}")
            return False
    
    def delete_class(self, class_data):
        """Delete a class"""
        try:
            success = self.classroom_service.delete_class(class_data['class_id'])
            if success:
                # Refresh classes list
                self.get_user_classes()
            return success
        except Exception as e:
            self.error_occurred.emit(f"Failed to delete class: {str(e)}")
            return False
    
    # Post management methods
    def get_class_posts(self, class_id, post_type=None):
        """Get all posts for a class, optionally filtered by type"""
        try:
            posts = self.post_service.get_posts_by_class(class_id, post_type)
            self.posts_updated.emit(posts)
            return posts
        except Exception as e:
            self.error_occurred.emit(f"Failed to load posts: {str(e)}")
            return []
    
    def get_stream_posts(self, class_id):
        """Get stream posts for a class"""
        return self.get_class_posts(class_id)
    
    def get_classwork_posts(self, class_id, filter_type=None):
        """Get classwork posts, optionally filtered"""
        if filter_type and filter_type != "All":
            if filter_type == "Materials":
                return self.get_class_posts(class_id, "material")
            elif filter_type == "Assessments":
                return self.get_class_posts(class_id, "assessment")
        return self.get_class_posts(class_id)
    
    def get_post_details(self, post_id):
        """Get detailed information about a specific post"""
        try:
            post_details = self.post_service.get_post_by_id(post_id)
            if post_details:
                self.post_details_updated.emit(post_details)
            return post_details
        except Exception as e:
            self.error_occurred.emit(f"Failed to load post details: {str(e)}")
            return None
    
    def create_material(self, class_id, material_data):
        """Create a new material post"""
        try:
            post_id = self.post_service.create_post({
                **material_data,
                'class_id': class_id,
                'type': 'material'
            })
            if post_id:
                # Refresh posts
                self.get_class_posts(class_id)
            return post_id
        except Exception as e:
            self.error_occurred.emit(f"Failed to create material: {str(e)}")
            return None
    
    def create_assessment(self, class_id, assessment_data):
        """Create a new assessment post"""
        try:
            post_id = self.post_service.create_post({
                **assessment_data,
                'class_id': class_id,
                'type': 'assessment'
            })
            if post_id:
                # Refresh posts
                self.get_class_posts(class_id)
            return post_id
        except Exception as e:
            self.error_occurred.emit(f"Failed to create assessment: {str(e)}")
            return None
    
    def create_topic(self, class_id, topic_data):
        """Create a new topic"""
        try:
            topic_id = self.classroom_service.create_topic(class_id, topic_data)
            if topic_id:
                # Refresh posts to show new topic
                self.get_class_posts(class_id)
            return topic_id
        except Exception as e:
            self.error_occurred.emit(f"Failed to create topic: {str(e)}")
            return None
    
    def edit_post(self, post_id, updated_data):
        """Edit an existing post"""
        try:
            success = self.post_service.update_post(post_id, updated_data)
            if success:
                # Refresh post details
                self.get_post_details(post_id)
            return success
        except Exception as e:
            self.error_occurred.emit(f"Failed to edit post: {str(e)}")
            return False
    
    def delete_post(self, post_id):
        """Delete a post"""
        try:
            success = self.post_service.delete_post(post_id)
            return success
        except Exception as e:
            self.error_occurred.emit(f"Failed to delete post: {str(e)}")
            return False
    
    def add_comment(self, post_id, comment_text, user_id):
        """Add a comment to a post"""
        try:
            comment_id = self.post_service.add_comment(post_id, comment_text, user_id)
            if comment_id:
                # Refresh post details to show new comment
                self.get_post_details(post_id)
            return comment_id
        except Exception as e:
            self.error_occurred.emit(f"Failed to add comment: {str(e)}")
            return None