from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from PIL import ExifTags, Image

User = get_user_model()


class GradationSystem(models.Model):
    name = models.CharField(_("name"), max_length=100)
    description = models.TextField(_("description"), null=True, blank=True)

    class Meta:
        verbose_name = _("gradation_system")
        verbose_name_plural = _("gradation_systems")

    def __str__(self):
        return f"{self.name}"


class Value(models.Model):
    value = models.CharField(_("value"), max_length=50, null=True, blank=True)
    description = models.TextField(_("description"), null=True, blank=True)
    picture = models.ImageField(
        _("picture"),
        upload_to='collectibles/gradation_value',
        null=True,
        blank=True,
        )
    gradation_system = models.ForeignKey(
        GradationSystem,
        verbose_name=_("gradation_system"),
        on_delete=models.CASCADE,
        related_name="values",
        )

    class Meta:
        verbose_name = _("value")
        verbose_name_plural = _("values")

    def __str__(self):
        return f"{self.value}"

    def get_absolute_url(self):
        return reverse("value_detail", kwargs={"pk": self.pk})


class ItemType(models.Model):
    name = models.CharField(_("name"), max_length=50)
    description = models.TextField(_("description"), null=True, blank=True)
    picture = models.ImageField(
        _("picture"),
        upload_to='collectibles/item_type',
        null=True,
        blank=True,
        )

    class Meta:
        verbose_name = _("item_type")
        verbose_name_plural = _("item_types")

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("itemtype_detail", kwargs={"pk": self.pk})


class CollectibleItem(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name=_("user"),
        on_delete=models.CASCADE,
        related_name="collectible_items"
        )
    country = models.CharField(_("country"), max_length=100)
    currency = models.CharField(_("currency"), max_length=100, null=True, blank=True)
    release_year = models.PositiveIntegerField(_("release_year"))
    circulation = models.PositiveIntegerField(_("circulation"), null=True, blank=True)
    item_type = models.ForeignKey(
        ItemType,
        verbose_name=_("item_type"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="collectible_items"
    )
    denomination = models.FloatField(_("denomination"), null=True, blank=True)
    quantity = models.PositiveIntegerField(_("quantity"))
    condition = models.ForeignKey(
        GradationSystem,
        verbose_name=_("condition"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="collectible_items"
    )
    value = models.ForeignKey(
        Value,
        verbose_name=_("value"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="collectible_items"
    )
    
    description = models.TextField(_("description"), max_length=3000, null=True, blank=True)
    obverse_side = models.ImageField(
        _("obverse_side"),
        upload_to='collectibles/obverse_side',
        null=True,
        blank=True,
        )
    reverse_side = models.ImageField(
        _("reverse_side"),
        upload_to='collectibles/reverse_side',
        null=True,
        blank=True,
        )
    register_date = models.DateTimeField(_("register_date"), auto_now_add=True)
    update_date = models.DateTimeField(_("update date"), null=True, blank=True)
    

    class Meta:
        verbose_name = _("collectible_item")
        verbose_name_plural = _("collectible_items")

    def __str__(self):
        return self.country

    def get_absolute_url(self):
        return reverse("collectibleitem_detail", kwargs={"pk": self.pk})
    
    # item verification
    # def find_similar_items(self, user):
    #     return CollectibleItem.objects.filter(
    #         user=user,
    #         country=self.country,
    #         release_year=self.release_year,
    #         item_type=self.item_type,
    #         denomination=self.denomination,
    #     ).exclude(pk=self.pk)


    # This part is for keeping images in their original orientation and resizing
    def _rotate_image(self, image):
        try:
            # Check if the image has an EXIF orientation tag
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break
            exif = dict(image._getexif().items())

            if orientation in exif:
                if exif[orientation] == 3:
                    image = image.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    image = image.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    image = image.rotate(90, expand=True)
        except (AttributeError, KeyError, IndexError):
            # Ignore if the image doesn't have EXIF data or orientation tag
            pass

        return image

    def _resize_and_save_image(self, field_name):
        image_field = getattr(self, field_name)
        if image_field:
            image = Image.open(image_field.path)
            image = self._rotate_image(image)
            if image.width > 600 or image.height > 600:
                new_size = (600, 600)
                image.thumbnail(new_size)
            image.save(image_field.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._resize_and_save_image('obverse_side')
        self._resize_and_save_image('reverse_side')