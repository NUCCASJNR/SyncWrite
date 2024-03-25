#!/usr/bin/env python3

"""Celery task handler"""


from rental.utils.email_utils import EmailUtils
from rental.models.apartment import ( ApartmentImage,
                                     Apartment
)
from celery import shared_task
import logging
from cloudinary.uploader import upload

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@shared_task
def async_upload_images(images, apartment_id):
    try:
        upload_results = []
        for image_content in images:
            logger.debug(f"Uploading image: {image_content}")
            try:
                result = upload(image_content, folder=f'RentEase/Apartments/{apartment_id}')
                logger.debug(f"Image uploaded: {result}")
                upload_results.append(result)
            except Exception as e:
                logger.error(f"Error uploading image {image_content}: {str(e)}")
        apartment = Apartment.objects.get(id=apartment_id)
        apartment_images = []
        for result in upload_results:
            apartment_images.append(ApartmentImage(apartment=apartment, image=result))
            logger.info(f"Apartment image created: {result['secure_url']}")
        ApartmentImage.objects.bulk_create(apartment_images)
        return {
            "message": "Apartment images uploaded successfully",
            "uploaded_image_count": len(upload_results),
            "uploaded_image_urls": upload_results
        }
    except Exception as e:
        logger.error(f'Error uploading apartment images due to: {str(e)}')
        return {
            "error": f"Error uploading apartment images: {str(e)}"
        }


@shared_task
def send_verification_email_async(user, verification_code):
    EmailUtils.send_verification_email(user, verification_code)


@shared_task
def send_assigned_apartment_email_async(email, username, apartment_details):
    EmailUtils.send_assigned_apartment_email(email, username, apartment_details)


@shared_task
def send_review_email_async(agent_email, details):
    EmailUtils.send_owner_book_review_mail(agent_email, details)

