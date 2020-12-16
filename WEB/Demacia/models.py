# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class DemaciaappAdmin(models.Model):
    admin_id = models.CharField(primary_key=True, max_length=50)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'DemaciaApp_admin'


class DemaciaappTrafficcount(models.Model):
    file_name = models.CharField(max_length=100)
    date = models.DateTimeField()
    time = models.TimeField()
    total = models.IntegerField()
    straight = models.IntegerField()
    turn_left = models.IntegerField()
    turn_right = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'DemaciaApp_trafficcount'


class DemaciaappUser(models.Model):
    user_id = models.CharField(primary_key=True, max_length=50)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'DemaciaApp_user'


class DemaciaappVideofile(models.Model):
    upload_file = models.CharField(unique=True, max_length=100)
    uploaded_time = models.DateTimeField()
    state = models.IntegerField()
    csv_file = models.CharField(max_length=100)
    convert_file = models.CharField(max_length=100, blank=True, null=True)
    line_data = models.TextField(blank=True, null=True)
    user = models.ForeignKey(DemaciaappUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'DemaciaApp_videofile'


class SeoulPlaza(models.Model):
    index = models.BigIntegerField(blank=True, null=True)
    intersection_name = models.TextField(blank=True, null=True)
    time = models.TextField(blank=True, null=True)
    frame = models.TextField(blank=True, null=True)
    direction_1 = models.IntegerField(blank=True, null=True)
    direction_2 = models.IntegerField(blank=True, null=True)
    car = models.IntegerField(blank=True, null=True)
    bus = models.IntegerField(blank=True, null=True)
    truck = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Seoul_Plaza'


class SeoulPlaza20201204Result(models.Model):
    intersection_name = models.TextField(blank=True, null=True)
    time = models.TextField(blank=True, null=True)
    frame = models.TextField(blank=True, null=True)
    direction_1 = models.IntegerField(blank=True, null=True)
    direction_2 = models.IntegerField(blank=True, null=True)
    car = models.IntegerField(blank=True, null=True)
    bus = models.IntegerField(blank=True, null=True)
    truck = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Seoul_Plaza_20201204_result'


class SeoulPlaza20201205Result(models.Model):
    intersection_name = models.TextField(blank=True, null=True)
    time = models.TextField(blank=True, null=True)
    frame = models.TextField(blank=True, null=True)
    direction_1 = models.IntegerField(blank=True, null=True)
    direction_2 = models.IntegerField(blank=True, null=True)
    car = models.IntegerField(blank=True, null=True)
    bus = models.IntegerField(blank=True, null=True)
    truck = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Seoul_Plaza_20201205_result'


class SeoulPlaza20201206Result(models.Model):
    intersection_name = models.TextField(blank=True, null=True)
    time = models.TextField(blank=True, null=True)
    frame = models.TextField(blank=True, null=True)
    direction_1 = models.IntegerField(blank=True, null=True)
    direction_2 = models.IntegerField(blank=True, null=True)
    car = models.IntegerField(blank=True, null=True)
    bus = models.IntegerField(blank=True, null=True)
    truck = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Seoul_Plaza_20201206_result'


class SeoulPlaza20201207Result(models.Model):
    intersection_name = models.TextField(blank=True, null=True)
    time = models.TextField(blank=True, null=True)
    frame = models.TextField(blank=True, null=True)
    direction_1 = models.IntegerField(blank=True, null=True)
    direction_2 = models.IntegerField(blank=True, null=True)
    car = models.IntegerField(blank=True, null=True)
    bus = models.IntegerField(blank=True, null=True)
    truck = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Seoul_Plaza_20201207_result'


class SeoulPlaza20201208Result(models.Model):
    intersection_name = models.TextField(blank=True, null=True)
    time = models.TextField(blank=True, null=True)
    frame = models.TextField(blank=True, null=True)
    direction_1 = models.IntegerField(blank=True, null=True)
    direction_2 = models.IntegerField(blank=True, null=True)
    car = models.IntegerField(blank=True, null=True)
    bus = models.IntegerField(blank=True, null=True)
    truck = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Seoul_Plaza_20201208_result'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
