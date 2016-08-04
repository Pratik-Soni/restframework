from __future__ import unicode_literals
from django.db import models
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles
from pygments import highlight
from pygments.formatters.html import HtmlFormatter


LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])



class UserDetails(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=True, default='')
    last = models.CharField(max_length=100, blank=True, default='')
    address = models.CharField(max_length=500, blank=True, default='')
    number = models.IntegerField()
    language = models.CharField(choices=LANGUAGE_CHOICES, default='Hindi', max_length=100)
    owner = models.ForeignKey('auth.User', related_name='userdetail')
    #highlighted = models.TextField()
    
    class Meta:
        ordering = ('created',)

    
    def save(self, *args, **kwargs):
        
        lexer = get_lexer_by_name(self.language)
        option = self.name and {'name':self.name} or {}
        
        super(UserDetails, self).save(*args, **kwargs)        

    