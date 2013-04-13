from django.contrib import admin

import reversion

from .models import Forum
from .models import ForumComment
from .models import defaultCategories
from .models import ModeratorForumCategories


class ForumAdmin(reversion.VersionAdmin):

    pass
    
class ForumCommentAdmin(reversion.VersionAdmin):
    list_display = ('post', 'created_by', 'comment', 'added', 'date_last_changed',)
    list_filter = ('tags__name',)

admin.site.register(Forum, ForumAdmin)
admin.site.register(ForumComment, ForumCommentAdmin)
admin.site.register(defaultCategories)
admin.site.register(ModeratorForumCategories)


# OLD
#admin.site.register(Thread)
#admin.site.register(ThreadHistory)
#admin.site.register(ForumPost)
#admin.site.register(ForumPostHistory)