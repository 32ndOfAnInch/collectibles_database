from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


User = get_user_model()


class Value(models.Model):
    value = models.CharField(_("value"), max_length=50)
    

    class Meta:
        verbose_name = _("value")
        verbose_name_plural = _("values")

    def __str__(self):
        return f"{self.value}"

    def get_absolute_url(self):
        return reverse("value_detail", kwargs={"pk": self.pk})


class GradationSystem(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name=_("user"),
        on_delete=models.CASCADE,
        related_name="gradation_systems"
    )
    value = models.ForeignKey(
        Value, 
        verbose_name=_("value"), 
        on_delete=models.CASCADE,
        related_name="gradation_systems"
        )
    name = models.CharField(_("name"), max_length=100)
    description = models.TextField(_("description"), null=True, blank=True)

    class Meta:
        verbose_name = _("gradation_system")
        verbose_name_plural = _("gradation_systems")

    def __str__(self):
        return f"{self.name}"


class CollectibleItem(models.Model):
    user = models.ForeignKey(
        User, 
        verbose_name=_("user"), 
        on_delete=models.CASCADE,
        related_name="collectible_items"
        )
    country = models.CharField(_("country"), max_length=100)
    currency = models.CharField(_("currency"), max_length=100)
    release_year = models.IntegerField(_("release_year"))
    circulation = models.IntegerField(_("circulation"), null=True, blank=True)

    ITEM_TYPE_CHOICES = (
        (1, _('Circulation Coins')),
        (2, _('Banknotes')),
        (3, _('Commemorative Coins')),
        (4, _('Circulating Commemoratives')),
        (5, _('Collector Coins')),
        (6, _('Bullion Coins')),
        (7, _('Medals')),
        (8, _('Other')),
    )

    item_type = models.PositiveSmallIntegerField(
        _("item_type"),
        choices=ITEM_TYPE_CHOICES,
        db_index=True,
        )
    denomination = models.FloatField(_("denomination"), null=True, blank=True)
    quantity = models.IntegerField(_("quantity"))
    condition = models.ForeignKey(
        GradationSystem,
        verbose_name=_("condition"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="collectible_items"
    )
    
    description = models.CharField(_("description"), max_length=3000, null=True, blank=True)
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
