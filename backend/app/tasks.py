from app.extensions import celery # <- NEW
import time

@celery.task(bind=True, name='create_task')
def create_task(self, video_id):
    """
    A mock task that simulates video processing.
    """
    total_steps = 10
    for i in range(total_steps):
        # Simulate work
        time.sleep(2)
        
        # Update state with progress
        progress = (i + 1) / total_steps * 100
        self.update_state(
            state='PROGRESS',
            meta={'current': i + 1, 'total': total_steps, 'percent': progress, 'video_id': video_id}
        )
    
    # Task completion
    return {'status': 'Completed', 'video_id': video_id, 'result_url': f'/static/processed/{video_id}.mp4'}