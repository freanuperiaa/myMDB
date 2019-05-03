from django.shortcuts import redirect
from django.urls import reverse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView


from .forms import VoteForm
from .models import Movie, Person, Vote


class MovieListView(ListView):
    model = Movie
    paginate_by = 10


class MovieDetailView(DetailView):
    queryset = Movie.objects.all_with_related_persons_and_score()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            vote = Vote.objects.get_vote_or_unsaved_blank_vote(
                movie=self.object, user=self.request.user,
            )
            if vote.id:
                vote_form_url = reverse('core:vote_update', kwargs={
                    'movie_id': vote.movie.id, 'pk': vote.id})
            else:
                vote_form_url = (
                    reverse(
                        'core:vote_create', kwargs={'movie_id': self.object.id})
                )
            vote_form = VoteForm(instance=vote)
            context['vote_form'] = vote_form
            context['vote_form_url'] = vote_form_url
        return context


class PersonDetail(DetailView):
    queryset = Person.objects.all_with_prefetch_movies()


class CreateVote(LoginRequiredMixin, CreateView):
    form_class = VoteForm

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.id
        initial['movie'] = self.kwargs['movie_id']
        return initial

    def get_success_url(self):
        movie_id = self.object.movie.id
        return reverse('core:movie_detail', kwargs={'pk': movie_id})

    def render_to_response(self, context, **response_kwargs):
        movie_id = context['object'].id
        movie_detail_url = reverse('core:movie_detail', kwargs={'pk': movie_id})
        return redirect(to=movie_detail_url)


class UpdateVote(LoginRequiredMixin, UpdateView):
    form_class = VoteForm
    queryset = Vote.objects.all()

    def get_object(self, queryset=None):
        vote = super().get_object()
        user = self.request.user
        if vote.user != user:
            raise PermissionDenied('cannot change another users vote.')
        return vote

    def get_success_url(self):
        movie_id =  self.object.movie.id
        return reverse('core:movie_detail', kwargs={'pk': movie_id})

    def render_to_response(self, context, **response_kwargs):
        movie_id = context['object'].id
        movie_detail_url = reverse('core;movie_detail', kwargs={'pk': movie_id})
        return redirect(to=movie_detail_url)