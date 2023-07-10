from typing import Any, Dict
from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.db.models.query import QuerySet
from . import models
from . import forms
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.http import Http404, JsonResponse


def index(request):
    return render(request, 'collectibles_database/index.html')


class CollectiblesListView(LoginRequiredMixin, ListView):
    model = models.CollectibleItem
    paginate_by = 7
    template_name = 'collectibles_database/collectibles_list.html'
    context_object_name = 'collectibles_list'

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        query = self.request.GET.get('query')
        
        if query:
            qs = qs.filter(
                Q(country__icontains=query),
                user=self.request.user
            )
        else:
            qs = qs.filter(user=self.request.user)
        
        return qs
    

class FriendCollectiblesListView(LoginRequiredMixin, ListView):
    model = models.CollectibleItem
    paginate_by = 7
    template_name = 'collectibles_database/friend_collectibles_list.html'
    context_object_name = 'friend_collectibles_list'

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        query = self.request.GET.get('query')
        user_id = self.kwargs.get('user_id')
        
        # Check if the logged-in user is friends with the requested user
        if self.request.user.profile.friends.filter(user_id=user_id).exists():
            if query:
                qs = qs.filter(
                    Q(country__icontains=query),
                    user_id=user_id
                )
            else:
                qs = qs.filter(user_id=user_id)
            
            return qs
        
        # If the logged-in user is not friends with the requested user, raise 404 error
        raise Http404("You are not authorized to view this page.")


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
        messages.success(self.request, _('New item successfully added to the list!'))
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        return super().get_form(form_class)


    # UserPassesTestMixin conditions
    def test_func(self):
        return self.request.user.is_authenticated
    

class UpdateItemView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = models.CollectibleItem
    form_class = forms.CreateItemForm
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
        messages.success(self.request, _('Item details updated successfully!'))
        return super().form_valid(form)
    
    # UserPassesTestMixin conditions
    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_authenticated and obj.user == self.request.user
    

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        instance = context.get('object')
        if instance:
            condition_id = instance.condition.gradation_system_id
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
        messages.success(self.request, _('Item deleted successfully!'))
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