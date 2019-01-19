from django.urls import path, re_path
from django.shortcuts import HttpResponse,render,redirect
from django import forms


class BaseModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'input'
            if isinstance(field, forms.DateField):
                field.widget.input_type = 'date'
                field.widget.format = '%Y-%m-%d'



class ModelStark:
    '''
    模型的配置类
    '''

    list_display = ['__str__']

    model_form_class = None

    def __init__(self, model):
        self.model = model
        self.app_label = model._meta.app_label
        self.model_name = model._meta.model_name
        self.list_view_url_alais = f'{self.app_label}_{self.model_name}_show_view'

    def get_new_list_display(self):
        return self.list_display

    def get_model_form_class(self):
        class DetailModelForm(BaseModelForm):
            class Meta:
                model = self.model
                fields = '__all__'

        return self.model_form_class or DetailModelForm

    def list_view(self, request):
        # 查看的视图函数
        data = []  # 用户保存数据的，最终结格式为:  [[td, td, td...], [td, td, '''], [...]]
        queryset = self.model.objects.all()

        for field in self.get_new_list_display():
            temp = []
            for model_obj in queryset:
                val = getattr(model_obj, field)
                temp.append(val)
            data.append(temp)
        # data = [['python', 123], ['go', 1234]]
        return render(request, 'stark/list_view.html', {'data': data})

    def add_view(self, request):
        # 添加的视图函数

        CurrentModelForm = self.get_model_form_class()

        if request.method == 'GET':
            form = CurrentModelForm()
            return render(request, 'stark/add_view.html', {'form': form})
        else:
            form = CurrentModelForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect(self.list_view_url_alais)
            else:
                return render(request, 'stark/add_view.html', {'form': form})

    def change_view(self, request, id):
        # 修改的视图函数
        return HttpResponse('change_view')

    def delete_view(self, request, id):
        # 删除的视图函数
        return HttpResponse('delete_view')

    @property
    def urls(self):
        '''
       二级url分发
       :return:
       '''
        return [
                   path('', self.list_view, name=self.list_view_url_alais),
                   path('add/', self.add_view),
                   re_path('(\d+)/change/', self.change_view),
                   re_path('(\d+)/delete', self.delete_view),
               ], None, None

class StarkSite:

    def __init__(self):
        '''
        初始化函数，self._registry字典用于保存模型类和模型配置类的对应关系
        '''
        self._register = {}

    def register(self, model, StarkClass=None):
        '''
        模型配置类的 注册函数 ==》  {model：Stark_class(model)}
        :param model:
        :param Stark_class:
        :return:
        '''
        StarkClass = StarkClass or ModelStark
        self._register[model] = StarkClass(model)

    @property
    def urls(self):
        '''
        为每个注册的model动态生成url
        :return:
        '''
        tmp_urls = []

        for model, model_config in self._register.items():
            model_name, app_label = model._meta.model_name, model._meta.app_label
            tmp_urls.append(
                path(f'{app_label}/{model_name}/', model_config.urls),
            )

        return tmp_urls, None, None

site = StarkSite()