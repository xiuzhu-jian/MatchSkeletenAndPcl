import json
import os

from Config import Config
from MatchProcess import match
from Tool import make_output_dir

skeleton_data_dir = r'C:\Users\XiuzhuJian_05qqcw2\PycharmProjects\D455Test\output'

if __name__ == '__main__':
    output_dir = make_output_dir()

    with open('config.json', 'r') as f:
        config = json.load(f)

        for item in config:
            info = Config(*item['coordinate'].split(','), *item['arena'].split(','))
            for sub_dir in os.listdir(item['data_path']):
                id_str = sub_dir.rsplit('_', 1)[-1]
                sub_skeleton_data_dir = os.path.join(skeleton_data_dir, id_str)
                if not os.path.exists(sub_skeleton_data_dir):
                    print(f'error: {sub_dir} does not exists')
                    continue
                sub_dir = os.path.join(item['data_path'], sub_dir)
                match(sub_skeleton_data_dir, sub_dir, output_dir, info)
