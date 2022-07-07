from django.db import models


class Subscriber(models.Model):
    email = models.CharField(blank=False, null=False,
                             max_length=120,
                             help_text="E-mail address")
    full_name = models.CharField(max_length=255, blank=False,
                                 null=False, help_text="Full name")
    nickname = models.CharField(max_length=20, blank=True, null=True,
                                help_text="Nickname")
    show_nickname = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Subscriber"
        verbose_name_plural = "Subscribers"

    def __str__(self):
        if self.show_nickname:
            return self.nickname
        return self.full_name
