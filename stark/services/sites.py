from django.urls import path, re_path
from django.shortcuts import HttpResponse


class ModelStark:
    '''
    模型的配置类
    '''

    list_display = ['__str__']

    def __init__(self, model):
        self.model = model
        self.app_label = model._meta.app_label
        self.model_name = model._meta.model_name
        self.list_view_url_alais = f'{self.app_label}_{self.model_name}_show_view'

    def get_new_list_display(self):
        return self.list_display

    def list_view(self, request):
        # 查看的视图函数
       return HttpResponse('list_view')

    def add_view(self, request):
        # 添加的视图函数
        return HttpResponse('add_view')

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