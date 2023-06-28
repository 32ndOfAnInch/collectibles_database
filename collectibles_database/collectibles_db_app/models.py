from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


User = get_user_model()


class Condition(models.Model):
    value = models.CharField(_("value"), max_length=70)
    

    class Meta:
        verbose_name = _("condition")
        verbose_name_plural = _("conditions")

    def __str__(self):
        return f"{self.value}"

    def get_absolute_url(self):
        return reverse("condition_detail", kwargs={"pk": self.pk})


class GradingSystem(models.Model):
    name = models.CharField(_("name"), max_length=50)
    description = models.CharField(_("description"), max_length=2000)
    condition = models.ForeignKey(
        Condition, 
        verbose_name=_("condition"), 
        on_delete=models.CASCADE,
        related_name="grading_systems"
        )
    

    class Meta:
        verbose_name = _("grading_system")
        verbose_name_plural = _("grading_systems")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("gradingsystem_detail", kwargs={"pk": self.pk})
    

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
    circulation = models.IntegerField(_("circulation"))

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
    denomination = models.FloatField(_("denomination"))
    quantity = models.IntegerField(_("quantity"))
    condition = models.ForeignKey(
        GradingSystem, 
        verbose_name=_("condition"), 
        on_delete=models.CASCADE,
        related_name="collectible_items"
        )
    description = models.CharField(_("description"), max_length=3000)
    # obverse side  // image
    # reverse side  // imgae
    register_date = models.DateTimeField(_("register_date"), auto_now_add=True)
    update_date = models.DateTimeField(_("update date"))
    

    class Meta:
        verbose_name = _("collectible_item")
        verbose_name_plural = _("collectible_items")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("collectibleitem_detail", kwargs={"pk": self.pk})
