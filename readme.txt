A Django-based online drug ordering system designed for an imaginary scenario where hospital personnel order drugs from a central storage and receive delivery by drones. This is a project finished in a limited time (~2 weeks) for the software engineering course of HKU.

Limitations:
-uploading images for  supply items in Django admin will upload the images to the root directory of the project, need to manually
 move this image from root directory to aspsite/static/media

-password reset token is not guaranteed to destroy if unused (only destroyed when the user submits the last form), resulting in glitchy behaviour upon next forget password request

