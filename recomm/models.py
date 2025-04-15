from django.db import models

# Create your models here.

class ChampionInteraction(models.Model):
    ROLE_CHOICES = [
        ('top', 'Top'),
        ('jungle', 'Jungle'),
        ('middle', 'Middle'),
        ('bottom', 'Bottom'),
        ('support', 'Support'),
    ]

    TYPE_CHOICES = [
        ('synergy', 'Synergy'),
        ('matchup', 'Matchup'),
    ]

    champion1 = models.CharField(max_length=50)  # Primary champion
    champion1_role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    champion2 = models.CharField(max_length=50)  # Secondary champion
    champion2_role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    interaction_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    win_rate = models.FloatField()
    delta_wr = models.FloatField()
    sample_size = models.IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['champion1', 'champion1_role', 'interaction_type']),
            models.Index(fields=['champion2', 'champion2_role']),
        ]

    def __str__(self):
        return f"{self.champion1} ({self.champion1_role}) {self.interaction_type} with {self.champion2} ({self.champion2_role})"

class Champion(models.Model):
    champion_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]
