from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import ugettext as _


class TimestampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseModel(TimestampedModel):
    name = models.CharField(max_length=70)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Department(BaseModel):

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'department'


class Territory(BaseModel):
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'territory'
        verbose_name_plural = 'territories'


class EmployeeManager(UserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """ Creates and saves a User with the given username, email and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_admin=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def _supervisor(self):
        return self.supervisor.first_name


class Employee(AbstractUser):
    USERNAME_FIELD = 'email'
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('username'), unique=False,
                                blank=True, max_length=150, null=True)
    nik = models.CharField(max_length=10, blank=True, default='999999', unique=True)
    is_guest = models.BooleanField(default=False)
    REQUIRED_FIELDS = []
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)

    supervisor = models.ForeignKey(
        'Employee',
        null=True,
        blank=True,
        related_name='employees',
        on_delete=models.CASCADE
    )

    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)

    territory = models.ForeignKey(Territory, on_delete=models.CASCADE, blank=True, null=True)

    objects = EmployeeManager()

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        db_table = 'employee'


class Parameter(BaseModel):
    question = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='departments')
    weight = models.DecimalField(default=0, decimal_places=2, max_digits=12)
    standard = models.IntegerField(default=0)

    def __str__(self):
        return self.question

    class Meta:
        db_table = 'parameter'


class Answer(TimestampedModel):
    question = models.ForeignKey(Parameter, on_delete=models.CASCADE, related_name='parameters')
    value = models.IntegerField()

    def __str__(self):
        return self.question.question

    class Meta:
        db_table = 'answer'


class Result(BaseModel):
    DEFAULT = 'not-assestment'
    PRODUCTIVE = 'productive'
    NOT_PRODUCTIVE = 'not-productive'

    STATUS = (
        (DEFAULT, 'Belum Dinilai'),
        (PRODUCTIVE, 'Produktif'),
        (NOT_PRODUCTIVE, 'Tidak Produktif'),
    )

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    answers = models.ManyToManyField(Answer)
    period = models.CharField(max_length=100, default='')
    result = models.CharField(max_length=100, choices=STATUS, default=DEFAULT)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'result'
        ordering = ['-period', '-result']
