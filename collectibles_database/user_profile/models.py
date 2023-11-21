from collectibles_db_app.models import CollectibleItem
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from PIL import ExifTags, Image

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(), 
        verbose_name=_("user"), 
        on_delete=models.CASCADE,
        related_name='profile',
        null=True, blank=True,
    )
    picture = models.ImageField(_("picture"), upload_to='user_profile/pictures', null=True, blank=True)
    friends = models.ManyToManyField("self", blank=True)

    # User preferences

    PAGINATION_CHOICES = [
        (12, _('12 items per page')),
        (24, _('24 items per page')),
        (36, _('36 items per page')),
        (48, _('48 items per page')),
    ]

    paginate_by = models.PositiveSmallIntegerField(
        _("paginate_by"),
        choices=PAGINATION_CHOICES,
        default=12,
    )

    COLOR_THEME_CHOICES = (
        (1, _('light')),
        (2, _('dark')),
    )

    color_theme = models.PositiveSmallIntegerField(
        _("color_theme"),
        max_length = 20, 
        choices = COLOR_THEME_CHOICES,
        default = 1,
    )

    DISPLAY_THEME_CHOICES = (
        (1, _('grid')),
        (2, _('list')),
    )

    display_theme = models.PositiveSmallIntegerField(
        _("color_theme"),
        max_length = 20, 
        choices = DISPLAY_THEME_CHOICES,
        default = 1,
    )

    is_verification = models.BooleanField(
        _("is_verification"),
        default= True,
    )

    is_notification = models.BooleanField(
        _("is_notification"),
        default= True,
    )

    # user preferences end

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse("profile_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.picture:
            img = Image.open(self.picture.path)
            try:
                # Check if the image has an EXIF orientation tag
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break
                exif = dict(img._getexif().items())

                if orientation in exif:
                    if exif[orientation] == 3:
                        img = img.rotate(180, expand=True)
                    elif exif[orientation] == 6:
                        img = img.rotate(270, expand=True)
                    elif exif[orientation] == 8:
                        img = img.rotate(90, expand=True)
            except (AttributeError, KeyError, IndexError):
                # Ignore if the image doesn't have EXIF data or orientation tag
                pass

            # Resize the image if needed
            if img.width > 300 or img.height > 300:
                new_size = (300, 300)
                img.thumbnail(new_size)
            img.save(self.picture.path)
                

    def remove_friend(self, friend):
        self.friends.remove(friend)


    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

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
