from typing import Any
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from . import models


class CollectiblesListView(LoginRequiredMixin, ListView):
    model = models.CollectibleItem
    template_name = 'collectibles_database/collectibles_list.html'
    context_object_name = 'collectibles_list'
