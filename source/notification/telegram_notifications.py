#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from datetime import datetime

from telethon import TelegramClient

from source.model.config.notification import NotificationConfig
from source.utils.variables import NOTIFICATION_CONFIG_PATH, REPOSITORY_IMG_DATA_PATH
from source.model.repository import ImageRepository

image_repository = ImageRepository()
notification_conf = NotificationConfig.create_from_file(NOTIFICATION_CONFIG_PATH)

api_id = notification_conf.telegram_api_id
api_hash = notification_conf.telegram_api_hash
receivers_list = ['@ainokila'] #notification_conf.telegram_receivers.split(',')
time_notification = notification_conf.check_hour
service_enabled = notification_conf.enabled_notifications

client = TelegramClient('telegram_nofitication', api_id, api_hash)


async def send_notification(image_paths):

    for receiver in receivers_list:
        message = await client.send_message(
            receiver,
            'Hello,\n\n'
            'We have dectected a new candidates in the station,\n\n'
            'You can validate or discard them in [Sky Meteor Detector](https://example.com)\n\n'
            'Captured images:',
            link_preview=False
        )

        for image_path in image_paths:
            await client.send_file(receiver, image_path)


if __name__ == '__main__':

    while True:

            notification_conf_new = NotificationConfig.create_from_file(NOTIFICATION_CONFIG_PATH)

            if hash(notification_conf_new) != hash(notification_conf):
                print("Detected configuration change")

                notification_conf = notification_conf_new

                receivers_list = notification_conf.telegram_receivers.split(',')
                time_notification = notification_conf.check_hour
                service_enabled = notification_conf.enabled_notifications

            if service_enabled and datetime.now().strftime("%H:%M") == time_notification:

                image_names = image_repository.list_files('candidates', extension='jpg')
                image_paths = []

                for image_name in image_names:
                    image_paths.append(REPOSITORY_IMG_DATA_PATH + '/candidates/' + image_name + '.jpg')

                if image_paths:
                    with client:
                        client.loop.run_until_complete(send_notification(image_paths))

            time.sleep(60)
            break
