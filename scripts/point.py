import numpy as np
import laspy as lp
import sys
sys.path.append('../scripts')
from logger import CreateLogger

logger = CreateLogger('CloudSubSampler')
logger = logger.get_default_logger()


class CloudPoint():
    """Redefines a numpy array as an object to hold x,y,z class attributes.

    Parameters
    ----------
    cloud_point_array : np.array
        Numpy Array Type consisting of 3 numeric values in a single element

    Returns
    -------
    None
    """
    def __init__(self, cloud_point_array: np.array) -> None:
        self.x = cloud_point_array[:, 0]
        self.y = cloud_point_array[:, 1]
        self.z = cloud_point_array[:, 2]
        
class CloudSubSampler():
    """Point Clouds Sampler Class that can implement Factor, BaryCenter or Relative Distance Samplings .

    Parameters
    ----------
    point_cloud : np.array
        Numpy Array Type consisting of 3 numeric values in a single element
    file_name : str
        String of the path plus name of the LAS or LAZ file to load point clouds from

    Returns
    -------
    None
    """

   def __init__(self, point_cloud: np.array = [], file_name: str = '') -> None:
        if((point_cloud == []) and (file_name == '')):
            logger.error(
                'Invalid Usage:\n\t-> Please Provide Either Cloud Points(np.array type) or File Path to a LAS or LAZ file only')
            sys.exit(1)

        elif((point_cloud != []) and (file_name == '')):
            self.point_cloud = self.create_cloud_point_class(point_cloud)
            logger.info(
                'Successfully Loaded Point Clouds')

        elif((point_cloud == []) and (file_name != '')):
            self.point_cloud = self.read_point_cloud_file(file_name)
            logger.info(
                'Successfully Loaded Point Clouds from LAS/LAZ File')
        else:
            logger.error(
                'Invalid Usage:\n\t-> Please Provide Either Cloud Points(np.array type) or File Path to a LAS or LAZ file only')
            sys.exit(1)

        self.available_samplings = ['factor', 'barycenter', 'closest']

        logger.info('Successfully Instantiated CloudSubSampler Class Object')

    def create_cloud_point_class(self, cloud_point_array: np.array) -> CloudPoint:
        """Create A CloudPoint Class instance from a given array.

        Parameters
        ----------
        cloud_point_array : np.array
            Numpy Array Type consisting of 3 numeric values in a single element

        Returns
        -------
        CloudPoint
            A CloudPoint Instance based on the numpy array provided
        """
        cloud_point = CloudPoint(cloud_point_array)

        return cloud_point

    def read_point_cloud_file(self, file_name: str):
        """Reads Point Clouds from a LAS/LAZ file.

        Parameters
        ----------
        file_name : str
            Path plus file name of the LAS/LAZ file

        Returns
        -------
        Laspy.data
            Point Clouds read from a LAS/LAZ file
        """
        try:
            clouds = lp.read(file_name)

            logger.info(f'Successfully Loaded point cloud form {file_name}')

            return clouds

        except Exception as e:
            logger.exception('Failed to load point clouds from File')
            sys.exit(1)

    def separate_points(self) -> None:
        """Separates points as numpy arrays from the loaded or given point clouds.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        try:
            if(not hasattr(self, 'points')):
                self.points = np.vstack(
                    (self.point_cloud.x, self.point_cloud.y, self.point_cloud.z)).transpose()

            else:
                logger.info('Points already Calculated, using previous values')

        except Exception as e:
            logger.exception(
                'Failed to separate points from point cloud')
            sys.exit(1)

    def get_factor_subsampling(self, factor: int) -> np.array:
        """Performs Simple Subsampling type, selects samples with a constant jump scale(factor).

        Parameters
        ----------
        factor : int
            How many items to count to select the next sample

        Returns
        -------
        np.array
            Sampled Numpy Array of the Point Clouds
        """

        try:
            self.separate_points()
            if(not hasattr(self, 'factored_points')):
                self.factored_points = self.points[::factor]

                return self.factored_points
            else:
                logger.info(
                    'Factoring Already Done Previously, using previous values')

        except:
            logger.exception(
                'Failed to sample cloud points using factoring')
            sys.exit(1)

    def get_grid_subsampling(self, voxel_size: float, sampling_type: str = 'closest') -> np.array:
        """Perfroms Grid Sampling on Point Clouds based on the specified voxel size and sampling type selected.

        Parameters
        ----------
        voxel_size : float
            Voxel size by which points are gathered together
        sampling_type : str, optional
            Which typeof grid subsampling to perform. If no input is provided distance relative
            sub-sampling implemented

        Returns
        -------
        np.array
            Sampled Numpy Array of the Point Clouds
        """

        self.separate_points()
        if(sampling_type != 'closest' and sampling_type != 'barycenter_sample'):
            print('Invalid type of sampling')
            sys.exit(1)
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

            logger.info('Successfully SubSampled Point Clouds')

            return self.candidate_center if sampling_type == 'closest' else self.barycenter_sample

        else:
            logger.info('Sampling Already Done before, Using Previous Value')
            return self.candidate_center if sampling_type == 'closest' else self.barycenter_sample

    def save_cloud(self, filename: str, sampling_type: str) -> None:
        """Save the variable to an ASCII file to open in a 3D Software.

        Parameters
        ----------
        filename : str
            Name of the file to save the data in.
        sampling_type : str
            Which Sampling type to save from.

        Returns
        -------
        None
        """
        try:
            if(sampling_type == 'barycenter'):
                sample_data = self.barycenter_sample
            elif(sampling_type == 'closest'):
                sample_data = self.candidate_center
            elif(sampling_type == 'factor'):
                sample_data = self.factored_points

            np.savetxt(filename+f'_{sampling_type}'+"_sampled.xyz",
                       sample_data, delimiter=";", fmt="%s")

            logger.info('Point Clouds Saved as ASCII File')

        except Exception as e:
            logger.exception('Failed to Save Point Clouds as ASCII File')
             