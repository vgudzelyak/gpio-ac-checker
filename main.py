import gpiod

from datetime import datetime
from asyncio import sleep
from telethon import TelegramClient

api_id = 'your_api_id'
api_hash = 'your_api_hash'
notifications_channel = 'some_channel'
ps_file = 'power_state.txt'
log_file = 'checker.log'
chip_path = '/dev/gpiochip0'
gpio_line = 22

client = TelegramClient('notificationbotua', api_id, api_hash)

async def main():
    while True:
        try:
            with open(ps_file, 'r') as file:
                raw_value = file.read()
                if raw_value:
                    current_state = raw_value.strip()
                else:
                    current_state = 'Unknown'
            with gpiod.request_lines(
                chip_path,
                consumer="get-line-value",
                config={gpio_line: gpiod.LineSettings(direction=gpiod.line.Direction.INPUT)},
            ) as request:
                value = str(request.get_value(gpio_line))[6:]
            if value == 'INACTIVE' and current_state == 'On':
                metadata = await client.get_entity(notifications_channel)
                message = '❌ AC power outage'
                await client.send_message(entity=metadata, message=message)
                with open(ps_file, 'w') as file:
                    file.write(str('Off'))
                with open(log_file, 'a') as file:
                    file.write(f'\n{datetime.now()} {message}')
            elif value == 'ACTIVE' and current_state == 'Off':
                metadata = await client.get_entity(notifications_channel)
                message = '✅ AC power has been restored'
                await client.send_message(entity=metadata, message=message)
                with open(ps_file, 'w') as file:
                    file.write(str('On'))
                with open(log_file, 'a') as file:
                    file.write(f'\n{datetime.now()} {message}')
            await sleep(1)
        except Exception as error:
            with open(log_file, 'a') as file:
                file.write(f'\n{datetime.now()} {error}')
                break

client.start()
client.loop.run_until_complete(main())