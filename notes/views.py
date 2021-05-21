from django.contrib import messages
from django.http import Http404
from django.shortcuts import reverse, get_object_or_404
from django.utils.timezone import now
from django.views import generic

from .forms import NoteCreateForm
from .models import Note


class HomeView(generic.CreateView):
    template_name = 'home.html'
    form_class = NoteCreateForm

    def get_success_url(self):
        return f'{reverse("created")}?s={self.object.slug}'


class CreatedView(generic.TemplateView):
    template_name = 'created.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.request.GET.get('s')
        context['link'] = get_object_or_404(Note, slug=slug).get_absolute_url()
        return context


class NoteView(generic.DetailView):
    template_name = 'note.html'
    model = Note

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if obj.allowed_reads <= obj.times_read:
            raise Http404('Note not found.')

        if obj.expires_at and obj.expires_at < now():
            raise Http404('Note not found.')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        obj = self.get_object()

        if obj.password:
            self.template_name = 'note_locked.html'
        elif obj.display_confirmation:
            self.template_name = 'confirm.html'
        else:
            obj.times_read += 1
            obj.save()

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        password = request.POST.get('password')
        self.object = self.get_object()

        if self.object.password == password or not self.object.password:
            self.object.times_read += 1
            self.object.save()
        else:
            self.template_name = 'note_locked.html'
            messages.add_message(request, messages.ERROR, 'Invalid Password')

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class AboutView(generic.TemplateView):
    template_name = 'about.html'


home = HomeView.as_view()
created = CreatedView.as_view()
note = NoteView.as_view()
about = AboutView.as_view()
