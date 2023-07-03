from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from PIL import Image
from collectibles_db_app.models import CollectibleItem
from django.dispatch import receiver
from django.db.models.signals import post_save


User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(), 
        verbose_name=_("user"), 
        on_delete=models.CASCADE,
        related_name='profile',
        null=True, blank=True,
    )
    picture = models.ImageField(_("picture"), upload_to='user_profile/pictures')
    friends = models.ManyToManyField("self", blank=True)

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse("profile_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        if self.picture:
            pic = Image.open(self.picture.path)
            if pic.width > 300 or pic.height > 300:
                new_size = (300, 300)
                pic.thumbnail(new_size)
                pic.save(self.picture.path)


class FriendRequest(models.Model):
    sender = models.ForeignKey(
        User, 
        verbose_name=_("sender"), 
        on_delete=models.CASCADE,
        related_name="sent_request"
        )
    receiver = models.ForeignKey(
        User, 
        verbose_name=_("receiver"), 
        on_delete=models.CASCADE,
        related_name="received_request"
        )
    collectible_item = models.ForeignKey(
        CollectibleItem,
        verbose_name=_("collectible_items"),
        on_delete=models.CASCADE, 
        related_name='friend_requests'
        )

    STATUS_CHOICES = (
        (1, _('Pending')),
        (2, _('Accepted')),
        (3, _('Rejected')),
    )
    status = models.PositiveSmallIntegerField(
        _("status"),
        choices=STATUS_CHOICES,
        db_index=True,
        )

    created_at = models.DateTimeField(_(''), auto_now_add=True)

    class Meta:
        verbose_name = _("friendrequest")
        verbose_name_plural = _("friendrequests")

    def __str__(self):
        return f"{self.sender} {self.receiver} {self.status}"

    def get_absolute_url(self):
        return reverse("friendrequest_detail", kwargs={"pk": self.pk})
