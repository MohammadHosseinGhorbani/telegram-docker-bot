import humanfriendly
import i18n
import html
from telegram import InlineKeyboardButton
from datetime import datetime
from docker.models.containers import Container
from docker.models.images import Image
from docker.models.volumes import Volume

from config import CONFIG, dclient, jinja


status_emojis = {
    'restarting': '🔄',
    'running': '🟢',
    'paused': '⏸️',
    'exited': '🔴'
}
commands_past = {
    'start': 'started',
    'stop': 'stopped',
    'restart': 'restarted',
    'pause': 'paused',
    'unpause': 'unpaused'
}


def make_containers_list_text():
    containers = dclient.containers.list(all=True)

    containers_list = [
        jinja.from_string(i18n.t('containers_list_item')).render(
            status=status_emojis[container.status],
            name=container.name,
            command='/c'+str(container.short_id)
        )
        for container in containers
    ]

    return jinja.from_string(i18n.t('containers_list')).render(container_list='\n'.join(containers_list))


def make_container_text(container: Container):
    ports_text = '\n'.join(
        ['\n'.join([f'{host.get("HostIp", '')}:{host.get("HostPort", '')}->{port}' for host in hosts]) for port, hosts in
         container.ports.items()])

    if container.status == 'exited':
        return jinja.from_string(i18n.t('stopped_container')).render(
            name=container.name,
            _id=container.short_id,
            status=container.short_id,
            ports=ports_text
        )
    else:
        status = dict(container.stats(stream=False))
        cpu_percent = ((status['cpu_stats']['cpu_usage']['total_usage'] - status['precpu_stats']['cpu_usage'][
            'total_usage']) / (status['cpu_stats']['system_cpu_usage'] - status['precpu_stats']['system_cpu_usage'])) * \
                      status['cpu_stats']['online_cpus'] * 100
        memory_usage = status['memory_stats']['usage']
        memory_limit = status['memory_stats']['limit']
        memory_percent = memory_usage / memory_limit * 100

        return jinja.from_string(i18n.t('running_container')).render(
            name=container.name,
            _id=container.short_id,
            status=container.status,
            ports=ports_text,
            cpu_percent=cpu_percent,
            mem_usage=humanfriendly.format_size(float(memory_usage)),
            mem_limit=humanfriendly.format_size(float(memory_limit)),
            mem_percent=memory_percent,
            pids=status['pids_stats']['current']
        )


def make_container_keyboard(container: Container):
    return ([
                [
                    InlineKeyboardButton(jinja.from_string(i18n.t('container_keyboard_start')).render(), callback_data=f'c_{container.short_id}_start', api_kwargs={'style': 'success'}),
                ]
            ] if container.status == 'exited' else [
        [
            InlineKeyboardButton(i18n.t('container_keyboard_restart'), callback_data=f'c_{container.short_id}_restart', api_kwargs={'style': 'primary'}),
            InlineKeyboardButton(i18n.t('container_keyboard_pause'), callback_data=f'c_{container.short_id}_pause', api_kwargs={'style': 'danger'}),
            InlineKeyboardButton(i18n.t('container_keyboard_stop'), callback_data=f'c_{container.short_id}_stop', api_kwargs={'style': 'danger'})
        ]
    ] if container.status != 'paused' else [
        [
            InlineKeyboardButton(i18n.t('container_keyboard_restart'), callback_data=f'c_{container.short_id}_restart', api_kwargs={'style': 'primary'}),
            InlineKeyboardButton(i18n.t('container_keyboard_unpause'), callback_data=f'c_{container.short_id}_unpause', api_kwargs={'style': 'success'}),
            InlineKeyboardButton(i18n.t('container_keyboard_stop'), callback_data=f'c_{container.short_id}_stop', api_kwargs={'style': 'danger'})
        ]
    ]) + [
        [
            InlineKeyboardButton(i18n.t('container_keyboard_logs'), callback_data=f'c_{container.short_id}_logs'),
        ],
        [
            InlineKeyboardButton(i18n.t('container_keyboard_back'), callback_data=f'c_list')
        ]
    ]


def make_images_list_text():
    images = dclient.images.list(all=True)

    images_list = [
        jinja.from_string(i18n.t('images_list_item')).render(
            index=str(index + 1) + '.',
            name=image.tags[0] if image.tags else image.short_id.split(':')[-1],
            command='/i' + image.short_id.split(':')[-1]
        )
        for index, image in enumerate(images)
    ]

    return jinja.from_string(i18n.t('images_list')).render(image_list='\n'.join(images_list))


def make_image_text(image: Image):
    return jinja.from_string(i18n.t('image')).render(
        names=', '.join(image.tags),
        _id=image.short_id,
        history=html.escape(('\n'.join([i['CreatedBy'] for i in image.history()]))[-CONFIG['history_character_limit']:])
    )


def make_volumes_list_text():
    volumes = dclient.volumes.list()

    volumes_list = []
    for volume in volumes:
        volume_id = 'v'
        underscores = []
        periods = []
        dashes = []
        for index, char in enumerate(volume.short_id):
            match char:
                case '_': underscores.append(str(index))
                case '.': periods.append(str(index))
                case '-': dashes.append(str(index))
                case _:
                    volume_id += char
        volume_id += (''.join(underscores) + ''.join(periods) + ''.join(dashes) +
                      str(len(underscores)) + str(len(periods))) + str(len(dashes))

        volumes_list.append([volume_id, volume.short_id])

    volumes_list_items = [
        jinja.from_string(i18n.t('volumes_list_item')).render(
            index=str(index + 1) + '.',
            name=vol[1],
            command='/'+vol[0]
        )
        for index, vol in enumerate(volumes_list)
    ]

    return jinja.from_string(i18n.t('volumes_list')).render(volumes_list='\n'.join(volumes_list_items))


def make_volume_text(volume: Volume):
    volume_date = datetime.fromisoformat(volume.attrs['CreatedAt'])

    return jinja.from_string(i18n.t('volume')).render(
        name=volume.name,
        _id=volume.short_id,
        driver=volume.attrs['Driver'],
        year=volume_date.year,
        month=volume_date.month,
        day=volume_date.day,
        hour=volume_date.hour,
        minute=volume_date.minute,
        second=volume_date.second,
        mount_point=volume.attrs['Mountpoint']
    )
