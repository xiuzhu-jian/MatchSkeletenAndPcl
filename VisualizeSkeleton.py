import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import datetime
import json
import numpy as np
import tqdm
import os

def visualize_pointcloud_and_skeleton(directory_path, x_lim, y_lim, z_lim):
    fig = plt.figure(figsize=(10, 5))
    gs = gridspec.GridSpec(1, 2, width_ratios=[2, 1])  
    ax1 = fig.add_subplot(gs[0], projection='3d')
    ax2 = fig.add_subplot(gs[1]) 

    skeleton_connect = [
        (4, 2), (2, 0), (0, 1), (1, 3),
        (10, 8), (8, 6), (6, 5), (5, 7), (7, 9),
        (6, 12), (12, 11), (11, 5),
        (12, 14), (14, 16), (11, 13), (13, 15)
    ]

    json_files = [f for f in os.listdir(directory_path) if f.endswith('.json')]

    def update_plot(doc):
        ax1.clear()
        ax2.clear()

        timestamp_str = doc["timestamp"]
        timestamp = int((timestamp_str)[:10])
        formatted_timestamp = datetime.datetime.fromtimestamp(timestamp)

        pointcloud = json.loads(doc['points'])
        gt_info = json.loads(doc['gt_info'])
        skeleton = gt_info[0]['skeleton']
        pointcloud = np.array([[p['x'], p['y'], p['z']] for p in pointcloud])
        skeleton = np.array([[s['x'], s['y'], s['z']] for s in skeleton])

        ax1.set_title(f'Vstraw Points and 3D Skeleton Points {formatted_timestamp}')
        ax1.set_xlabel('X axis')
        ax1.set_ylabel('Y axis')
        ax1.set_zlabel('Z axis')
        ax1.set_xlim(x_lim)
        ax1.set_ylim(y_lim)
        ax1.set_zlim(z_lim)
        ax1.scatter(pointcloud[:, 0], pointcloud[:, 1], pointcloud[:, 2], c='blue', marker='o', alpha=0.3)

        ax2.set_title('Top View of Skeleton Points')
        ax2.set_xlabel('X axis')
        ax2.set_ylabel('Y axis')
        ax2.set_xlim(x_lim)
        ax2.set_ylim(y_lim)
        ax2.scatter(pointcloud[:, 0], pointcloud[:, 1], c='blue', marker='o', alpha=0.3)

        for skeleton_info in gt_info:
            skeleton = skeleton_info['skeleton']
            skeleton = np.array([[s['x'], s['y'], s['z']] for s in skeleton])
            skeleton_target = skeleton
            ax1.scatter(skeleton_target[:, 0], skeleton_target[:, 1], skeleton_target[:, 2], c='green', marker='o')

            for joint1, joint2 in skeleton_connect:
                x_values = [skeleton_target[joint1, 0], skeleton_target[joint2, 0]]
                y_values = [skeleton_target[joint1, 1], skeleton_target[joint2, 1]]
                z_values = [skeleton_target[joint1, 2], skeleton_target[joint2, 2]]
                ax1.plot(x_values, y_values, z_values, 'ro-', alpha=0.8)

            ax2.scatter(skeleton_target[:, 0], skeleton_target[:, 1], c='green', marker='o')

        info_text = f'Timestamp: {formatted_timestamp}\nPointcloud shape: {pointcloud.shape}\nSkeleton joints: {len(skeleton)}'
        ax1.text2D(0.05, 0.95, info_text, transform=ax1.transAxes, fontsize=12, va='top')

        print(f"Timestamp: {formatted_timestamp}")

        plt.tight_layout()

    for json_file in tqdm.tqdm(json_files, desc="Loading data"):
        with open(os.path.join(directory_path, json_file), 'r') as f:
            data = json.load(f)
            update_plot(data)
            plt.draw()
            plt.pause(0.05)

    plt.show()

if __name__ == "__main__":
    # area
    x_min, x_max, y_min, y_max, z_min, z_max = -1.5, 1.5, 0, 4, 0, 2
    x_lim, y_lim, z_lim = [x_min, x_max], [y_min, y_max], [z_min, z_max]

    # .json directory path
    directory_path = r'C:\Users\XiuzhuJian_05qqcw2\PycharmProjects\MatchSkeletenAndPcl\output\point_cloud_info_generated_at_2024_07_22_22_11_50'

    visualize_pointcloud_and_skeleton(directory_path, x_lim, y_lim, z_lim)
