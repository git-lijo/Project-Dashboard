from django.contrib import admin

from projects.models import Company, Project, ProjectLogging, Tag


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'start_date', 'end_date')
    list_filter = ('company__name','tags')
    ordering = ('-start_date',)

    fieldsets = (
        (None, {'fields': ['company', 'title', 'start_date', 'end_date','tags']}),
        ('Estimated hours', {'fields': ['estimated_design', 'estimated_development', 'estimated_testing']}),
        ('Actual hours', {'fields': ['actual_design', 'actual_development', 'actual_testing']}),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ()

        return 'company',


admin.site.register(Company)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectLogging)
admin.site.register(Tag)