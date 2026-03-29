from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
	list_display = ('title', 'user', 'category', 'completed', 'created_at')
	list_filter = ('category', 'completed', 'created_at')
	search_fields = ('title', 'description', 'user__email')

	def save_model(self, request, obj, form, change):
		# Ensure tasks created in admin are always owned by someone.
		if obj.user_id is None:
			obj.user = request.user
		super().save_model(request, obj, form, change)