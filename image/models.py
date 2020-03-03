from django.db import models
import os
import uuid

STATUS_CHOICE = (
    (0, 'Complete'), (1, 'In Progress'), (2, 'Failed'),
)


def get_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('media/image_service', filename)


class ImageService(models.Model):
    model_name = models.CharField(max_length=255)
    image_analysis = models.TextField()
    image = models.ImageField(upload_to=get_upload_path, null=True, blank=True)
    transaction_status = models.SmallIntegerField(
        choices=STATUS_CHOICE, default=1
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Service External - Create Image base64"

    def __str__(self):
        return str(self.models)
