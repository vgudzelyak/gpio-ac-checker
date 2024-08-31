from telethon import TelegramClient
from asyncio import sleep
import subprocess

api_id = 'your_api_id'
api_hash = 'your_api_hash'
notifications_channel = 'some_channel'
jkbms_bt_mac = '00:00:00:00:00:00'
jkbms_port = 'jkv11'
ps_file = 'power_state.txt'

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
            dis_current = subprocess.check_output(f"jkbms -p {jkbms_bt_mac} -c getCellData -P {jkbms_port} | grep 'current_discharge' | awk '{{print $2}}'", shell=True).decode('utf-8')
            if float(dis_current) >= 1.0 and current_state == 'On':
                metadata = await client.get_entity(notifications_channel)
                await client.send_message(entity=metadata, message='❌ AC power outage')
                with open(ps_file, 'w') as file:
                    file.write(str('Off'))
            elif float(dis_current) < 1.0 and current_state == 'Off':
                metadata = await client.get_entity(notifications_channel)
                await client.send_message(entity=metadata, message='✅ AC power has been restored')
                with open(ps_file, 'w') as file:
                    file.write(str('On'))
            await sleep(60)
        except Exception as error:
            print(error)

client.start()
client.loop.run_until_complete(main())