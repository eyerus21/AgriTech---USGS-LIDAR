import numpy as np
import laspy as lp
import sys
import logger_creator

logger = logger_creator.CreateLogger('CloudSubSampler')
logger = logger.get_default_logger()


class CloudSubSampler():
    def __init__(self, file_name: str):
        self.point_cloud = self.read_point_cloud_file(file_name)
        self.available_samplings = ['factor', 'barycenter', 'closest']
        logger.info('Successfully Instantiated CloudSubSampler Class Object')

    def read_point_cloud_file(self, file_name: str):
        try:
            clouds = lp.read(file_name)

            logger.info(f'Successfully Loaded point cloud form {file_name}')

            return clouds

        except Exception as e:
            logger.exception('Failed to load point clouds from File')
            sys.exit(1)

    def separate_points_colors(self):
        try:
            if(not hasattr(self, 'points') and not hasattr(self, 'colors')):
                self.points = np.vstack(
                    (self.point_cloud.x, self.point_cloud.y, self.point_cloud.z)).transpose()

                self.colors = np.vstack((self.point_cloud.red, self.point_cloud.green,
                                        self.point_cloud.blue)).transpose()

            else:
                logger.info('Points already Calculated, using previous values')

        except Exception as e:
            logger.exception(
                'Failed to separate points and colors from point cloud')
            sys.exit(1)

    def get_factor_subsampling(self, factor: int):
        try:
            self.separate_points_colors()
            if(not hasattr(self, 'factored_points') and not hasattr(self, 'factored_colors')):
                self.factored_points = self.points[::factor]
                self.factored_colors = self.colors[::factor]

                return self.factored_points, self.factored_colors
            else:
                logger.info(
                    'Factoring Already Done Previously, using previous values')

        except:
            logger.exception(
                'Failed to sample cloud points using factoring')
            sys.exit(1)

    def get_grid_subsampling(self, voxel_size: int, sampling_type: str = 'closest'):
        self.separate_points_colors()
        if(sampling_type != 'closest' or sampling_type != 'barycenter_sample'):
            raise
        elif(sampling_type == 'closest' and not hasattr(self, 'candidate_center') or sampling_type == 'barycenter_sample' and not hasattr(self, 'barycenter_sample')):
            nb_vox = np.ceil((np.max(self.points, axis=0) -
                             np.min(self.points, axis=0)) / voxel_size)

            non_empty_voxel_keys, inverse, nb_pts_per_voxel = np.unique(
                ((self.points - np.min(self.points, axis=0)) // voxel_size).astype(int), axis=0, return_inverse=True, return_counts=True)
            idx_pts_vox_sorted = np.argsort(inverse)
            voxel_grid = {}
            grid_barycenter, grid_candidate_center = [], []
            last_seen = 0

            for idx, vox in enumerate(non_empty_voxel_keys):
                voxel_grid[tuple(
                    vox)] = self.points[idx_pts_vox_sorted[last_seen:last_seen+nb_pts_per_voxel[idx]]]
                grid_barycenter.append(np.mean(voxel_grid[tuple(vox)], axis=0))
                grid_candidate_center.append(voxel_grid[tuple(vox)][np.linalg.norm(
                    voxel_grid[tuple(vox)]-np.mean(voxel_grid[tuple(vox)], axis=0), axis=1).argmin()])

                last_seen += nb_pts_per_voxel[idx]

            self.barycenter_sample = grid_barycenter
            self.candidate_center = grid_candidate_center

            return self.candidate_center if sampling_type == 'closest' else self.barycenter_sample

        else:
            print('already calcuated')
            return self.candidate_center if sampling_type == 'closest' else self.barycenter_sample

    def save_cloud(self, filename: str, sampling_type: str):
        """Save the variable to an ASCII file to open in a 3D Software"""
        if(sampling_type == 'barycenter'):
            sample_data = self.barycenter_sample
        elif(sampling_type == 'closest'):
            sample_data = self.candidate_center
        elif(sampling_type == 'factor'):
            sample_data = self.factored_points

        np.savetxt(filename+f'_{sampling_type}'+"_sampled.xyz",
                   sample_data, delimiter=";", fmt="%s")
