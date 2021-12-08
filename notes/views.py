import nanoid
from django.contrib import messages
from django.http import Http404
from django.utils.timezone import now
from django.views import generic

from .forms import NoteCreateForm
from .models import Note


class HomeView(generic.CreateView):
    template_name = 'home.html'
    form_class = NoteCreateForm

    def form_valid(self, form):
        append_password = False
        password = form.cleaned_data.get('password')
        if not password:
            password = nanoid.generate(size=8)
            append_password = True

        self.object = form.save(commit=False)
        self.object.encrypt_content(password)
        self.object.save()

        link = self.object.get_absolute_url()
        if append_password:
            link += f'?p={password}'

        self.template_name = 'created.html'
        context = self.get_context_data()
        context['link'] = link
        return self.render_to_response(context)


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
        self.object = self.get_object()
        password = request.GET.get('p')

        if not password:
            self.template_name = 'note_locked.html'
            return super().get(request, *args, **kwargs)

        elif self.object.display_confirmation:
            self.template_name = 'confirm.html'
            return super().get(request, *args, **kwargs)

        return self.process(request, password, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        password = request.POST.get('password')
        self.object = self.get_object()

        return self.process(request, password, *args, **kwargs)

    def process(self, request, password, *args, **kwargs):
        content = self.object.decrypt_content(password)
        if not content:
            self.template_name = 'note_locked.html'
            messages.add_message(request, messages.ERROR, 'Invalid Password')
            return super().get(request, *args, **kwargs)

        context = self.get_context_data(object=self.object)
        context['content'] = content
        return self.render_to_response(context)


class AboutView(generic.TemplateView):
    template_name = 'about.html'


home = HomeView.as_view()
note = NoteView.as_view()
about = AboutView.as_view()
