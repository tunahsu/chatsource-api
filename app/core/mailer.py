from fastapi_mail import FastMail, ConnectionConfig
from pydantic import EmailStr, BaseModel
from typing import List

from app.core.config import settings


class EmailSchema(BaseModel):
    email_list: List[EmailStr]


conf = ConnectionConfig(MAIL_USERNAME=settings.MAIL_USERNAME,
                        MAIL_PASSWORD=settings.MAIL_PASSWORD,
                        MAIL_FROM=settings.MAIL_FROM,
                        MAIL_PORT=settings.MAIL_PORT,
                        MAIL_SERVER=settings.MAIL_SERVER,
                        MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
                        MAIL_STARTTLS=True,
                        MAIL_SSL_TLS=False,
                        USE_CREDENTIALS=True,
                        VALIDATE_CERTS=True)

fm = FastMail(conf)

forgot_passwor_template = """
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 10px;">
        <h2 style="text-align: center; color: #333;">Reset Your Password</h2>
        <p style="color: #555;">Hello,</p>
        <p style="color: #555;">We received a request to reset your password. Please click the button below to reset it:</p>
        <div style="text-align: center; margin: 20px 0;">
            <a href="{}/reset_password?token={}" style="background-color: #007BFF; color: white; padding: 15px 25px; text-decoration: none; border-radius: 5px; font-size: 16px;">
                Reset Password
            </a>
        </div>
        <p style="color: #555;">If you did not request this, please ignore this email.</p>
        <p style="color: #555;">Thank you!</p>
        <hr style="border: none; border-top: 1px solid #e0e0e0;">
        <p style="text-align: center; color: #999; font-size: 12px;">
            &copy; 2024 Chatsource. All rights reserved.
        </p>
    </div>
"""
