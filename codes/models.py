from django.db import models


class Code(models.Model):
    id = models.AutoField(primary_key=True)
    phrase = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    max_uses = models.IntegerField(default=0)  # 0 means unlimited
    uses = models.IntegerField(default=0)

    def __str__(self):
        return self.phrase

    @property
    def is_valid(self):
        return self.is_active and (self.max_uses == 0 or self.uses < self.max_uses)


class UniqueCode(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=255, unique=True)
    phrase_code = models.ForeignKey(Code, on_delete=models.CASCADE)
    used = models.BooleanField(default=False)
