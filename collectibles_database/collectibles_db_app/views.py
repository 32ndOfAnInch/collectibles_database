from datetime import datetime
from typing import Any, Dict

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Avg, Count, F, Max, Min, Q, Sum
from django.db.models.functions import Coalesce
from django.db.models.query import QuerySet
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from . import forms, models
from .utils.spacy_utils import extract_entities

User = get_user_model()


def index(request):
    return render(request, 'collectibles_database/index.html')


class CollectiblesListView(LoginRequiredMixin, ListView):
    model = models.CollectibleItem
    paginate_by = 12
    template_name = 'collectibles_database/collectibles_list.html'
    context_object_name = 'collectibles_list'

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        user = self.request.user

        # sorting functionality (by country and by release year)
        sort_by = self.request.GET.get('sort_by', 'default')
        order_by_fields = []

        if sort_by == 'country':
            order_by_fields.append('country')
        if sort_by == 'release_year':
            order_by_fields.append('release_year')


        # queryset fetch and apply sorting
        if order_by_fields:
            qs = qs.filter(user=user).order_by(*order_by_fields)
        else:
            qs = qs.filter(user=user)


        # search functionality
        query = self.request.GET.get('query')

        if query:
            entities = extract_entities(query, user)
            country_names = [entity[0] for entity in entities if entity[1] == 'GPE']
            # country_names = []
            # for entity in entities:
            #     if entity[1] == 'GPE':
            #         country_names.append(entity[0])
            qs = qs.filter(
                Q(country__icontains=query) | 
                Q(country__in=country_names) |  # fuzzy matching
                Q(release_year__icontains=query) |
                Q(currency__icontains=query),
                user=user
            )
        else:
            qs = qs.filter(user=user)
        
        return qs
    

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['sort_by'] = self.request.GET.get('sort_by', 'default')
        return context
    

class FriendCollectiblesListView(LoginRequiredMixin, ListView):
    model = models.CollectibleItem
    paginate_by = 12
    template_name = 'collectibles_database/friend_collectibles_list.html'
    context_object_name = 'friend_collectibles_list'

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        query = self.request.GET.get('query')
        user_id = self.kwargs.get('user_id')
        
        # Check if the logged-in user is friends with the requested user
        if self.request.user.profile.friends.filter(user_id=user_id).exists():
            user = User.objects.get(id=user_id)
            entities = extract_entities(query, user)

            if query:
                country_names = [entity[0] for entity in entities if entity[1] == 'GPE']
                qs = qs.filter(
                    Q(country__icontains=query) | 
                    Q(country__in=country_names) |  # fuzzy matching
                    Q(release_year__icontains=query) |
                    Q(currency__icontains=query),
                    user_id=user_id
                )
            else:
                qs = qs.filter(user_id=user_id)
            
            return qs
        
        # If the logged-in user is not friends with the requested user, raise 404 error
        raise Http404("You are not authorized to view this page.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('user_id')
        user = User.objects.get(id=user_id)
        context['friend'] = user
        return context


@login_required
def item_detail(request, pk: int):
    return render(request, 'collectibles_database/collectible_item_detail.html', 
                  {'item': get_object_or_404(models.CollectibleItem, pk=pk)})


@login_required
def statistics_view(request):
    total_records = models.CollectibleItem.objects.filter(user=request.user).count()
    total_items = models.CollectibleItem.objects.filter(user=request.user).aggregate(
        total_items=Sum('quantity'))['total_items']
    oldest_item = models.CollectibleItem.objects.filter(user=request.user).aggregate(
        Min('release_year'))['release_year__min']
    newest_item = models.CollectibleItem.objects.filter(user=request.user).aggregate(
        Max('release_year'))['release_year__max']
    total_years = models.CollectibleItem.objects.filter(user=request.user).annotate(
        total_year=F('release_year') * F('quantity')).aggregate(
        total_years=Sum('total_year'))['total_years']
    if total_items:
        average_year = total_years / total_items
        average_year = round(average_year, 1)
    else:
        average_year = None

    # stats by item type
    item_type_stats = models.CollectibleItem.objects.filter(user=request.user).values('item_type__name').annotate(
        total_records=Count('id'),
        total_items=Coalesce(Sum('quantity'), 0),
        oldest_item=Min('release_year'),
        newest_item=Max('release_year'),
    ).order_by('item_type__name')

    item_type_stats = [
        {
            'item_type': stat['item_type__name'],
            'total_records': stat['total_records'],
            'total_items': stat['total_items'],
            'oldest_item': stat['oldest_item'],
            'newest_item': stat['newest_item'],
        }
        for stat in item_type_stats
    ]

    
    context = {
        'total_records': total_records,
        'total_items': total_items,
        'oldest_item': oldest_item,
        'newest_item': newest_item,
        'average_year': average_year,
        'item_type_stats': item_type_stats,
    }

    return render(request, 'collectibles_database/collectibles_statistics.html', context)


def about_view(request):
    gradation_systems = models.GradationSystem.objects.all()
    return render(request, 'collectibles_database/about.html', {'gradation_systems': gradation_systems})

class CreateItemView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = models.CollectibleItem
    form_class = forms.CreateItemForm
    template_name = 'collectibles_database/collectible_item_form.html'
    success_url = reverse_lazy('collectibles_list')
    context_object_name = 'create_new_item'


    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        instance = context.get('object')
        if instance:
            condition_id = instance.condition_id
            if condition_id:
                context['form'].fields['value'].queryset = models.Value.objects.filter(
                    gradation_system_id=condition_id
                )
        return context
    
    def get_initial(self) -> Dict[str, Any]:
        initial = super().get_initial()
        initial['user'] = self.request.user
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        # messages.success(self.request, _('New item successfully added to the list!'))
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        return super().get_form(form_class)


    # UserPassesTestMixin conditions
    def test_func(self):
        return self.request.user.is_authenticated
    

class UpdateItemView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = models.CollectibleItem
    form_class = forms.UpdateItemForm
    template_name = 'collectibles_database/collectible_item_form.html'
    success_url = reverse_lazy('collectibles_list')
    context_object_name = 'update_item'

    def get_form(self, form_class=None):
        return super().get_form(form_class)
    

    def get_initial(self) -> Dict[str, Any]:
        initial = super().get_initial()
        initial['update_date'] = datetime.now().replace(microsecond=0)
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        # messages.success(self.request, _('Item details updated successfully!'))
        return super().form_valid(form)
    
    # UserPassesTestMixin conditions
    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_authenticated and obj.user == self.request.user
    

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        instance = context.get('object')
        if instance:
            condition_id = instance.condition_id
            if condition_id:
                context['form'].fields['value'].queryset = models.Value.objects.filter(
                    gradation_system_id=condition_id
                )
        return context
        

class DeleteItemView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = models.CollectibleItem
    template_name = 'collectibles_database/collectible_item_delete.html'
    success_url = reverse_lazy('collectibles_list')
    context_object_name = 'delete_item'

    def form_valid(self, form):
        # messages.success(self.request, _('Item deleted successfully!'))
        return super().form_valid(form)
    
    # UserPassesTestMixin conditions
    def test_func(self) -> bool | None:
        obj = self.get_object()
        return self.request.user.is_authenticated and obj.user == self.request.user
    

def get_values(request):
    gradation_system_id = request.GET.get('gradation_system_id')

    # Fetch the related Value objects based on the gradation_system_id
    values = models.Value.objects.filter(gradation_system_id=gradation_system_id)

    data = {
        'values': list(values.values('id', 'value'))
    }

    return JsonResponse(data)