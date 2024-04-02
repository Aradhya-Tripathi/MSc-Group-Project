from django.db import models


TABLE_NAME = "Tasks"


class Tasks(models.Model):
    """Handle Task Information"""

    class Meta:
        verbose_name_plural = "Tasks"
        db_table = TABLE_NAME

    task_id: models.CharField = models.CharField(max_length=150, primary_key=True)
    registration_time: models.DateTimeField = models.DateTimeField()
    task_status: models.CharField = models.CharField(max_length=50)
    result_destination: models.FilePathField = models.FilePathField()
    queries_path: models.FilePathField = models.FilePathField()
    model_settings: models.JSONField = (
        models.JSONField()
    )  # Store model type and model parameters for now!
