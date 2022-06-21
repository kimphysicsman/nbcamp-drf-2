from django.contrib import admin
from .models import User, UserProfile, Hobby


class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'fullname')
    list_display_links = ('username', )
    # list_filter = ('username', )
    search_fields = ('username', )


    # 생성 / 수정 모두 readonly로 설정
    readonly_fields = ('join_date', )

    # 생성 시 write 가능, 수정 시 readonly field로 설정
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('username', 'join_date', )
        else:
            return ('join_date', )

    fieldsets = (
        ("info", {'fields': ('username', 'fullname', 'join_date')}),
        ('permissions', {'fields': ('is_admin', 'is_active', )}),
    )

    inlines = (
            UserProfileInline,
        )

    # def has_add_permission(self, request, obj=None): # 추가 권한
    #     return False

    # def has_delete_permission(self, request, obj=None): # 삭제 권한
    #     return False

    # def has_change_permission(self, request, obj=None): # 수정 권한
    #     return False


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)
admin.site.register(Hobby)

