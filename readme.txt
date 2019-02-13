Limitations:
-uploading images for  supply items in Django admin will upload the images to the root directory of the project, need to manually
 move this image from root directory to aspsite/static/media

-password reset token is not guaranteed to destroy if unused (only destroyed when the user submits the last form), resulting in glitchy behaviour upon next forget password request

