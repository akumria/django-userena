from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from userena import views as userena_views
from userena import settings as userena_settings

USERENA_USERNAME_REGEX="(?P<username>[\\.\\w]+)/"
if userena_settings.USERENA_WITHOUT_USERNAMES:
    USERENA_USERNAME_REGEX=""

urlpatterns = patterns('',
    # Signup, signin and signout
    url(r'^signup/$',
       userena_views.signup,
       name='userena_signup'),
    url(r'^signin/$',
       userena_views.signin,
       name='userena_signin'),
    url(r'^signout/$',
       auth_views.logout,
       {'next_page': userena_settings.USERENA_REDIRECT_ON_SIGNOUT,
        'template_name': 'userena/signout.html'},
       name='userena_signout'),

    # Reset password
    url(r'^password/reset/$',
       auth_views.password_reset,
       {'template_name': 'userena/password_reset_form.html',
        'email_template_name': 'userena/emails/password_reset_message.txt'},
       name='userena_password_reset'),
    url(r'^password/reset/done/$',
       auth_views.password_reset_done,
       {'template_name': 'userena/password_reset_done.html'},
       name='userena_password_reset_done'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
       auth_views.password_reset_confirm,
       {'template_name': 'userena/password_reset_confirm_form.html'},
       name='userena_password_reset_confirm'),
    url(r'^password/reset/confirm/complete/$',
       auth_views.password_reset_complete,
       {'template_name': 'userena/password_reset_complete.html'}),

    # Signup
    url(r'^%ssignup/complete/$' % USERENA_USERNAME_REGEX,
       userena_views.direct_to_user_template,
       {'template_name': 'userena/signup_complete.html',
        'extra_context': {'userena_activation_days': userena_settings.USERENA_ACTIVATION_DAYS}},
       name='userena_signup_complete'),

    # Activate
    url(r'^%sactivate/(?P<activation_key>\w+)/$' % USERENA_USERNAME_REGEX,
       userena_views.activate,
       name='userena_activate'),

    # Change email and confirm it
    url(r'^%semail/$' % USERENA_USERNAME_REGEX,
       userena_views.email_change,
       name='userena_email_change'),
    url(r'^%semail/complete/$' % USERENA_USERNAME_REGEX,
       userena_views.direct_to_user_template,
       {'template_name': 'userena/email_change_complete.html'},
       name='userena_email_change_complete'),
    url(r'^%sconfirm-email/complete/$' % USERENA_USERNAME_REGEX,
       userena_views.direct_to_user_template,
       {'template_name': 'userena/email_confirm_complete.html'},
       name='userena_email_confirm_complete'),
    url(r'^%sconfirm-email/(?P<confirmation_key>\w+)/$' % USERENA_USERNAME_REGEX,
       userena_views.email_confirm,
       name='userena_email_confirm'),

    # Disabled account
    url(r'^%sdisabled/$' % USERENA_USERNAME_REGEX,
       userena_views.direct_to_user_template,
       {'template_name': 'userena/disabled.html'},
       name='userena_disabled'),

    # Change password
    url(r'^%spassword/$' % USERENA_USERNAME_REGEX,
       userena_views.password_change,
       name='userena_password_change'),
    url(r'^%spassword/complete/$' % USERENA_USERNAME_REGEX,
       userena_views.direct_to_user_template,
       {'template_name': 'userena/password_complete.html'},
       name='userena_password_change_complete'),

    # Edit profile
    url(r'^%sedit/$' % USERENA_USERNAME_REGEX,
       userena_views.profile_edit,
       name='userena_profile_edit'),

)


# View profiles
if userena_settings.USERENA_WITHOUT_USERNAMES:
    urlpatterns += patterns('',
        url(r'^detail/$',
           userena_views.profile_detail,
           name='userena_profile_detail'),
    )
else:
    urlpatterns += patterns('',
        url(r'^(?P<username>[\.\w]+)/$',
           userena_views.profile_detail,
           name='userena_profile_detail'),
    )

urlpatterns += patterns('',
    url(r'^page/(?P<page>[0-9]+)/$',
       userena_views.profile_list,
       name='userena_profile_list_paginated'),
    url(r'^$',
       userena_views.profile_list,
       name='userena_profile_list'),
)
