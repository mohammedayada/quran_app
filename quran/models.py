from django.db import models

MAKAH_MADINA_CHOICES = (("مكية", "مكية"),
                        ("مدنية", "مدنية")
                        )


# Create your models here.
class Surah(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    title = models.CharField(max_length=50)
    numbers_of_verses = models.PositiveIntegerField(null=False, blank=False)
    numbers_of_words = models.PositiveIntegerField(null=False, blank=False)
    numbers_of_chars = models.PositiveIntegerField(null=False, blank=False)
    order = models.PositiveIntegerField(null=False, blank=False)
    madanya_or_makya = models.CharField(max_length=8, choices=MAKAH_MADINA_CHOICES)

    def __str__(self):
        return self.title


# aya
class Verse(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    number = models.PositiveIntegerField(null=False, blank=False)
    text = models.TextField()
    surah = models.ForeignKey(Surah, null=False, blank=False, on_delete=models.CASCADE)
    info = models.TextField()

    def __str__(self):
        return '{} {}'.format(self.surah, self.number)


# juza
class Part(models.Model):
    number = models.PositiveIntegerField(primary_key=True)
    from_verse = models.ForeignKey(Verse, null=False, blank=False, on_delete=models.CASCADE, related_name='from_verses')
    to_verse = models.ForeignKey(Verse, null=False, blank=False, on_delete=models.CASCADE, related_name='to_verses')

    def __str__(self):
        return 'from: {} to: {}'.format(self.from_verse.id, self.to_verse.id)


# al mofaser
class Author(models.Model):
    name = models.CharField(max_length=250, null=False, blank=False)
    die_date_in_higri = models.CharField(max_length=250)
    info = models.TextField()
    religious_view = models.TextField()
    mazhab_fekhy = models.TextField()
    etgah_almofaser_fe_tafseroh = models.TextField()
    manhag_almofaser = models.TextField()
    relations_tree = models.TextField()
    knowledge = models.CharField(max_length=50)  # 3alem , taleb 3elm mo3aser

    def __str__(self):
        return self.name


# tafsier
class Explanation(models.Model):
    verse = models.ForeignKey(Verse, null=False, blank=False, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, null=False, blank=False, on_delete=models.CASCADE)
    comment = models.TextField(null=False, blank=False)

    def __str__(self):
        return 'Verse: {}, Author: {}, comment: {} '.format(self.verse, self.author, self.comment)
