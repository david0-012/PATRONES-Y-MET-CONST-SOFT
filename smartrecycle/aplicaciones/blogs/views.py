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
    
#Registro de usuarios ----------------------------------------------------------------------

from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import RegisterForm
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from .views import View    
from django.utils.encoding import force_str
from django.shortcuts import redirect
from .token import account_activation_token
from django.contrib.auth.views import LoginView as AuthLoginView
UserModel = get_user_model()


class UserRegistration(FormView):
    template_name = 'users/registration.html'
    form_class = RegisterForm
    success_url = reverse_lazy('blogs:success')#blogs:success
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # Deactivate account till it is confirmed
        user.save()

        current_site = get_current_site(self.request)
        mail_subject = 'Activate your blog account.'
        message = render_to_string('users/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(mail_subject, message, to=[to_email])
        if email.send():
            messages.success(self.request, f'Estimado/a {user}, vaya a la bandeja de entrada de su correo electrónico {to_email} y haga clic en \
                el enlace de activación recibido para confirmar y completar el registro. Nota: revisa tu carpeta de spam.')
        else:
            messages.error(self.request, f'Problem sending email to {to_email}, check if you typed it correctly.')

        return super(UserRegistration, self).form_valid(form)
class AccountVerification(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = UserModel.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                messages.success(request, 'Tu cuenta ha sido activada exitosamente, ahora puedes iniciar sesión')
                return redirect('login')
            else:
                messages.error(request, 'El enlace de activación es inválido')
                return redirect('login')
        except(TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            messages.error(request, 'El enlace de activación es inválido')
            return redirect('login')    
class LoginView(AuthLoginView):
    def get(self, request, *args, **kwargs):
        message = request.session.pop('account_activation_message', None)
        if message:
            messages.success(request, message)
        return super().get(request, *args, **kwargs)      