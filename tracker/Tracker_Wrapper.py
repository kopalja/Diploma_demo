### Description: Tracker Wrapper units API for using different IoU implementations and shared libralies 
### (e.g., Python , C++ [x86, ARMv7, AArach64])

import sys
import os
import platform
sys.path.insert(0, os.environ['RTT'])


class Tracker_Wrapper:
    def __init__(self, sigma_l, sigma_h, sigma_iou, t_min, multiple_object = False, python = False):
        if python:
            #from tracker.IOUTracker import IOUTracker
	        raise Exception('Python version of the IoU tracker is not supported') 
        elif platform.machine() == 'x86_64':
            from tracker.x86.IOUTracker import IOUTracker
        elif platform.machine() == 'armv7l':
            from tracker.arm7.IOUTracker import IOUTracker  
        elif platform.machine() == 'aarch64':
            from tracker.aarch64.IOUTracker import IOUTracker  
        else:
            raise Exception('Unsupported tracker architecture')
        self._python = python   
        self._tracker = IOUTracker(sigma_l, sigma_h, sigma_iou, t_min, multiple_object)


    def update_tracks(self, ans):
        if not self._python:
            record = []
            for d in ans:
                tmp = [d.label_id, d.score.item()]
                tmp.extend(d.bounding_box.flatten().tolist())
                record.extend(tmp)
            ans = record
        self._tracker.update_tracks(ans)

    def get_tracked_number(self):
        return self._tracker.get_finished_tracks(), self._tracker.get_active_tracks()

    def get_tracked_multiple(self):
        if self._python:
            raise Exception('Python multiple not implemented')

        return self._tracker.get_finished_cars(), self._tracker.get_finished_trucks(), self._tracker.get_active_cars(), self._tracker.get_active_trucks()
