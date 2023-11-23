from django.contrib import admin
from .models import CustomUser
from .models import Contributor


# Registering CustomUser for Django admin interface.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    # Columns to be displayed in the user listing.
    list_display = ('id', 'username', 'age', 'can_be_contacted', 'can_data_be_shared', 'created_time')

    # Filters added to the side of the admin page.
    list_filter = ('can_be_contacted', 'can_data_be_shared')

    # Adding a search bar to search users by their 'username'.
    search_fields = ('username',)


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    # Columns to be displayed in the contributor listing
    list_display = ('user', 'project')
