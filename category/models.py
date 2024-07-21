from django.db import models

from category import imggenerate


class State(models.Model):
    class Meta:
        verbose_name = 'State'
        verbose_name_plural = 'States'

    name = models.CharField('Название', max_length=200)

    def __str__(self):
        return str(self.name)


class District(models.Model):
    class Meta:
        verbose_name = 'District'
        verbose_name_plural = 'Districts'

    name = models.CharField('Название', max_length=200)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='State')

    def __str__(self):
        return str(self.name)


class IndicatorCategory(models.Model):
    class Meta:
        verbose_name = 'Категория показателя'
        verbose_name_plural = 'Категории показателей'

    name = models.CharField('Название', max_length=200)
    icon = models.TextField('Иконка', blank=True)
    iconSecond = models.TextField('Вторая иконка', blank=True)
    description = models.TextField('Описание', blank=True)

    def __str__(self):
        return str(self.name)


class IndicatorSubCategory(models.Model):
    class Meta:
        verbose_name = 'Под категория показателя'
        verbose_name_plural = 'Под категории показателей'

    name = models.CharField('Название', max_length=200)
    category = models.ForeignKey(IndicatorCategory, models.SET_NULL, null=True, blank=True, verbose_name='Категория')
    icon = models.TextField('Иконка', blank=True)
    iconSecond = models.TextField('Вторая иконка', blank=True)
    description = models.TextField('Описание', blank=True)
    additionalDataTitle = models.CharField('Заголовок допалнительных данных', max_length=200, blank=True)
    addDataDesc = models.TextField('Описание допалнительных данных', blank=True)

    def __str__(self):
        return str(self.name)


class NewsCategory(models.Model):
    class Meta:
        verbose_name = 'Категория новостей'
        verbose_name_plural = 'Категории новостей'

    name = models.CharField('Название', max_length=200)
    icon = models.TextField('Иконка', blank=True)

    def __str__(self):
        return str(self.name)


class Image(models.Model):
    class Meta:
        verbose_name = 'Рисунок'
        verbose_name_plural = 'Рисунки'

    title = models.CharField('Заголовок', max_length=200)
    image = models.ImageField('Рисунок', upload_to=imggenerate.all_image_path, blank=True)
    forSvg = models.FileField('Svg рисунок', upload_to=imggenerate.all_image_path, blank=True)

    def __str__(self):
        return str(self.title)


class GraphCategory(models.Model):
    class Meta:
        verbose_name = 'Категория графов'
        verbose_name_plural = 'Категории графов'

    name = models.CharField('Название', max_length=250)
    value = models.FloatField('Значение', default=0)
    subCategory = models.ForeignKey(IndicatorSubCategory, models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.name)
