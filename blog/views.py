from django.shortcuts import render

from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse
from .models import Blog, BlogAuthor, BlogComment
from django.contrib.auth.models import User


def index(request):
    """
    View function for home page of site.
    """
    # Render the HTML template index.html
    return render(
        request,
        'index.html',
    )



class BlogListView(generic.ListView):
    """
    Generic class-based view for a list of all blogs.
    """
    model = Blog
    paginate_by = 5
    ordering = ['-post_date']



class BlogListbyAuthorView(generic.ListView):
    """
    Generic class-based view for a list of blogs posted by a particular BlogAuthor.
    """
    model = Blog
    paginate_by = 5
    template_name ='blog/blog_list_by_author.html'

    def get_queryset(self):
        """
        Return list of Blog objects created by BlogAuthor (author id specified in URL)
        """
        id = self.kwargs['pk']
        target_author=get_object_or_404(User, pk = id)
        return Blog.objects.filter(author=target_author)

    def get_context_data(self, **kwargs):
        """
        Add BlogAuthor to context so they can be displayed in the template
        """
        # Call the base implementation first to get a context
        context = super(BlogListbyAuthorView, self).get_context_data(**kwargs)
        # Get the blogger object from the "pk" URL parameter and add it to the context
        context['blogger'] = get_object_or_404(User, pk = self.kwargs['pk'])
        return context



class BlogDetailView(generic.DetailView):
    """
    Generic class-based detail view for a blog.
    """
    model = Blog


# class BloggerListView(generic.ListView):
#     """
#     Generic class-based view for a list of bloggers.
#     """
#     model = User
#     paginate_by = 5

def BloggerListView(request):
    users = User.objects.all
    context = {'users': users}
    paginate_by = 10
    return render(request, 'auth/user_list.html', context)


class BlogCommentCreate(LoginRequiredMixin, CreateView):
    """
    Form for adding a blog comment. Requires login.
    """
    model = BlogComment
    fields = ['comment',]

    def get_context_data(self, **kwargs):
        """
        Add associated blog to form template so can display its title in HTML.
        """
        # Call the base implementation first to get a context
        context = super(BlogCommentCreate, self).get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        context['blog'] = get_object_or_404(Blog, pk = self.kwargs['pk'])
        return context

    def form_valid(self, form):
        """
        Add author and associated blog to form data before setting it as valid (so it is saved to model)
        """
        #Add logged-in user as author of comment
        form.instance.author = self.request.user
        #Associate comment with blog based on passed id
        form.instance.blog=get_object_or_404(Blog, pk = self.kwargs['pk'])
        # Call super-class form validation behaviour
        return super(BlogCommentCreate, self).form_valid(form)

    def get_success_url(self):
        """
        After posting comment return to associated blog.
        """
        return reverse('blog-detail', kwargs={'pk': self.kwargs['pk']})


class BlogCreate(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['title', 'content']
    success_url = reverse_lazy('blogs')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)