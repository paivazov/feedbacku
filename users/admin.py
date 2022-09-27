from django.contrib import admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.forms import ModelForm, PasswordInput, CharField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User


class UserCreationForm(ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = CharField(label='Password', widget=PasswordInput)
    password2 = CharField(label='Password confirmation', widget=PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'is_organisation_lead')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_organisation_lead')


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_organisation_lead', "first_name", "last_name")
    list_filter = ('is_organisation_lead', "groups")
    fieldsets = (
        (None, {'fields': ('email', 'password', 'date_joined')}),
        ('Personal info', {'fields': ("first_name", "last_name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_organisation_lead",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2'),
            },
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # form.base_fields["is_organisation_lead"].disabled = True
        return form


admin.site.unregister(Group)
