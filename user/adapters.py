from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from .utils import download_file_from_url


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super(SocialAccountAdapter, self).save_user(
            request, sociallogin, form)

        user.is_active = True

        url = sociallogin.account.get_avatar_url()
        # here you should download file from provided url, the code is below
        avatar = download_file_from_url(url)
        if avatar:

            user.profile_img = avatar

        user.save()
        return user
