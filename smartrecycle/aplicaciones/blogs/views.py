from django.shortcuts import render
from django.views import generic, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.utils import timezone
from .models import Post, Category
from django.db.models import Q
from django.urls import reverse
from .forms import PostCommentForm
# Create your views here.







def home_page(request):
    posts = Post.objects.filter(
        pub_date__lte=timezone.now()
    )
    categories = Category.objects.all()
    featured = Post.objects.filter(featured=True).filter(
        pub_date__lte=timezone.now()
        )[:3]
    
    context = {
        'post_list': posts,
        'featured': featured
    }
    
    return render(request, 'blogs/home_page.html', context=context)

class PostDetailView(generic.DetailView):
    model = Post
    queryset= Post.objects.filter(
        pub_date__lte=timezone.now()
    )
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostCommentForm()
        return context
    
    
class PostCommentFormView(LoginRequiredMixin,SingleObjectMixin,FormView):
    template_name = 'blogs/post_detail.html'
    form_class = PostCommentForm
    model = Post
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)    
    
    def form_valid(self, form):
        f = form.save(commit=False)
        f.author = self.request.user
        f.post = self.object
        f.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        
        return reverse('blogs:post', kwargs={'slug': self.object.slug}) + '#comments-section'
    
    
class PostView(View):

    def get(self, request, *args, **kwargs):
        view = PostDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostCommentFormView.as_view()
        return view(request, *args, **kwargs)   
    
    
    
class FeaturedListView(generic.ListView):
    model = Post
    template_name = 'blogs/results.html'
    paginate_by = 2
    def get_queryset(self):
        query = Post.objects.filter(featured=True).filter(
            pub_date__lte=timezone.now()
        )
        return query
    
    

class CategoryListView(generic.ListView):
    model = Post
    template_name = 'blogs/categorias.html'
    paginate_by = 2
    def get_queryset(self):
        query = self.request.path.replace('/category/', '')
        print(query)
        post_list = Post.objects.filter(categories__slug=query).filter(
            pub_date__lte=timezone.now()
        )
        return post_list
    
    
    #Titulos en categorias seleccionadas
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('category_slug')
        try:
            query = self.request.path.replace('/category/', '')
            category_title = query.replace('_', ' ').capitalize()  # Capitalizar la primera letra y reemplazar guiones bajos con espacios
            context['category_title'] = category_title
        except Category.DoesNotExist:
            context['category_title'] = None  # or handle the case where category is not found
        return context

    
    
    

    

class SearchResultsView(generic.ListView):
    model = Post
    template_name = 'blogs/search.html'
    paginate_by = 2
    def get_queryset(self):
        query = self.request.GET.get('search')
        post_list = Post.objects.filter(
            Q(title__icontains=query) | Q(categories__title__icontains=query)
        ).filter(
            pub_date__lte=timezone.now()
        ).distinct()
        return post_list

    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         context['query'] = self.request.GET.get('search')
         return context
    
