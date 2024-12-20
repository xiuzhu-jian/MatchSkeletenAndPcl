from Reporters.Reporter import Reporter
from Tools.TimeTool import ms_timestamp_to_str


class MatchResultReporter:
    def __init__(self):
        self.reporter = Reporter('MatchResultReporter')

    def on_start(self, output_folder: str, report_name: str):
        headers = [
            'pcl_filename',
            'sk_filename',
            'pcl_timestamp_ms',
            'sk_timestamp_ms',
            'pcl_time',
            'sk_time',
            'diff_ms',
        ]
        self.reporter.on_start(output_folder, report_name, headers)

    def report(self, pcl_filename: str, sk_filename: str, pcl_timestamp: float, sk_timestamp: float):
        self.reporter.report([
            pcl_filename,
            sk_filename,
            f'[{pcl_timestamp}]',
            f'[{sk_timestamp}]',
            f'[{ms_timestamp_to_str(pcl_timestamp)}]',
            f'[{ms_timestamp_to_str(sk_timestamp)}]',
            f'{pcl_timestamp - sk_timestamp}',
        ])

    def on_finish(self):
        self.reporter.on_finish()
