from .models import (
    Panel,
    Implantation,
    Roof,
    Roofing_type,
    Roof_type,
    Orientation,
    Pose,
)
from decimal import Decimal
import math
import json


class Implantation_calculation:
    def __init__(self, datas):
        """Init function of class Map"""

        # Replace empty values by 0
        datas = {k: (0 if v == "" else v) for (k, v) in datas.items()}

        # Project Data
        panel_id = datas["panel_id"]
        self.panel = Panel.objects.get(id=panel_id)

        # Roof Data
        roof_type = Roof_type.objects.get(id=datas["roof_type"])
        roofing_type = Roofing_type.objects.get(id=datas["roofing_type"])
        self.roof = Roof(
            roofing_type_id=roofing_type,
            roof_type_id=roof_type,
            bottom_length=float(datas["bottom_length"]),
            top_length=float(datas["top_length"]),
            width=float(datas["width"]),
            height=float(datas["height"]),
        )

        # Implantation Data
        orientation = Orientation.objects.get(id=datas["panel_orientation"])
        pose = Pose.objects.get(id=datas["panel_implantation"])
        self.data_implantation = Implantation(
            panel_orientation=orientation,
            panel_implantation=pose,
            vertical_overlapping=int(datas["vertical_overlapping"]) / 1000,
            horizontal_overlapping=int(datas["horizontal_overlapping"]) / 1000,
            vertical_spacing=int(datas["vertical_spacing"]) / 1000,
            horizontal_spacing=int(datas["horizontal_spacing"]) / 1000,
            distance_top=int(datas["distance_top"]) / 1000,
            distance_bottom=int(datas["distance_bottom"]) / 1000,
            distance_left=int(datas["distance_left"]) / 1000,
            distance_right=int(datas["distance_right"]) / 1000,
            abergement_top=int(datas["abergement_top"]) / 1000,
            abergement_bottom=int(datas["abergement_bottom"]) / 1000,
            abergement_left=int(datas["abergement_left"]) / 1000,
            abergement_right=int(datas["abergement_right"]) / 1000,
        )

        self.data = self.init_roof_data()

    def init_roof_data(self):
        if self.roof.roof_type_id_id == 3:
            self.roof.height = math.sqrt(
                (self.roof.width * self.roof.width)
                - ((self.roof.bottom_length / 2) * (self.roof.bottom_length / 2))
            )
        implantation = Roof_implantation_Calculation(
            self.panel, self.roof, self.data_implantation
        )

        if self.roof.roof_type_id_id == 1:
            implantation.modif_width(self.data_implantation)
            implantation.pan_in_width(self.roof)
            implantation.modif_length(self.data_implantation)
            implantation.pan_in_length(self.roof)
        elif self.roof.roof_type_id_id == 2:
            implantation.modif_top_length(self.data_implantation)
            implantation.modif_height(self.data_implantation)
            implantation.pan_in_width(self.roof)
            implantation.pan_in_length(self.roof)
            implantation.hor_centering = (
                implantation.top_length
                - implantation.nb_panel_length * implantation.panel_length
            ) / 2
            implantation.lateral_space(self.data_implantation)
            implantation.Centering(self.data_implantation)
        elif self.roof.roof_type_id_id == 3:
            implantation.bottom_rest = (
                self.data_implantation.distance_bottom
                + self.data_implantation.abergement_bottom
            )
            implantation.lateral_rest()

        implantation.set_pose(self.data_implantation)
        implantation.set_panel_in_triangle_col(self.roof, self.data_implantation)
        implantation.update_roof_available_size(self.roof, self.data_implantation)
        implantation.set_pan_in_width(self.roof, self.data_implantation)
        implantation.set_pan_in_length(self.roof, self.data_implantation)
        implantation.Set_nb_pan_in_triangle_length(self.roof, self.data_implantation)
        implantation.reset_pan_in_col(self.roof, self.data_implantation)

        # region Reste
        if self.roof.roof_type_id_id == 1:
            implantation.set_rest()
        elif self.roof.roof_type_id_id == 2:
            implantation.top_rest = (
                implantation.distance_top
                + implantation.abergement_top
                + (
                    implantation.height
                    - (implantation.nb_panel_width * implantation.panel_width)
                    - implantation.vertical_pose * (implantation.nb_panel_width - 1)
                )
                / 2
            )
            implantation.bottom_rest = (
                implantation.distance_bottom
                + implantation.abergement_bottom
                + (
                    implantation.height
                    - (implantation.nb_panel_width * implantation.panel_width)
                    - implantation.vertical_pose * (implantation.nb_panel_width - 1)
                )
                / 2
            )
        elif self.roof.roof_type_id_id == 3:
            implantation.top_rest = (
                self.roof.height
                - implantation.panel_left_triangle[
                    implantation.nb_pan_lentgh_left_triangle
                ]
                * implantation.panel_width
                - implantation.vertical_pose
                * (
                    implantation.panel_left_triangle[
                        implantation.nb_pan_lentgh_left_triangle
                    ]
                    - 1
                )
                - self.data_implantation.abergement_top
                - implantation.bottom_rest
            )
            implantation.left_rest = (
                implantation.side_rest
                - implantation.nb_pan_lentgh_left_triangle * implantation.panel_length
                - implantation.horizontal_pose
                * (implantation.nb_pan_lentgh_left_triangle - 1)
                - implantation.horizontal_pose / 2
                - self.data_implantation.abergement_left
            )
            implantation.right_rest = (
                implantation.side_rest
                - implantation.nb_pan_lentgh_left_triangle * implantation.panel_length
                - implantation.horizontal_pose
                * (implantation.nb_pan_lentgh_right_triangle - 1)
                - implantation.horizontal_pose / 2
                - self.data_implantation.abergement_right
            )
        # endregion

        for i in range(0, implantation.nb_pan_lentgh_left_triangle):
            implantation.nb_pan_left_triangle += implantation.panel_left_triangle[i + 1]
        for i in range(0, implantation.nb_pan_lentgh_right_triangle):
            implantation.nb_pan_right_triangle += implantation.panel_right_triangle[
                i + 1
            ]

        implantation.nbpantot = (
            implantation.nb_panel_length * implantation.nb_panel_width
            + implantation.nb_pan_left_triangle
            + implantation.nb_pan_right_triangle
        )

        implantation.plot_data(self.roof, self.data_implantation)

        return implantation.toJSON()


class Roof_implantation_Calculation:
    def __init__(self, panel, roof, implantation):
        if implantation.panel_orientation_id == 1:
            self.panel_width = panel.width / 1000
            self.panel_length = panel.length / 1000
        else:
            self.panel_width = panel.length / 1000
            self.panel_length = panel.width / 1000

        self.distance_top = implantation.distance_top
        self.distance_bottom = implantation.distance_bottom
        self.distance_left = implantation.distance_left
        self.distance_right = implantation.distance_right
        self.abergement_bottom = implantation.abergement_bottom
        self.abergement_top = implantation.abergement_top
        self.abergement_left = implantation.abergement_left
        self.abergement_right = implantation.abergement_right
        self.height = roof.height
        # self.top_length = (
        #     roof.top_length
        #     - implantation.abergement_left
        #     - implantation.abergement_right
        # )
        self.width = roof.width
        self.bottom_length = roof.bottom_length
        self.side_angle = 0
        self.nb_panel_width = 0
        self.nb_panel_length = 0
        if roof.roof_type_id_id == 1:
            self.nb_panel_width = int(self.width / self.panel_width)
            self.nb_panel_length = int(self.bottom_length / self.panel_length)
        elif roof.roof_type_id_id == 2:  # Paralepiped
            self.top_length = (
                roof.top_length
                - implantation.abergement_left
                - implantation.abergement_right
            )
            self.nb_panel_width = int(self.height / self.panel_width)
            self.nb_panel_length = int(self.top_length / self.panel_length)
            self.side_rest = (roof.bottom_length - roof.top_length) / 2
            self.side_angle = math.atan(self.height / self.side_rest)
        elif roof.roof_type_id_id == 3:  # Triangle
            self.side_rest = roof.bottom_length / 2
            self.height = roof.height
            self.side_angle = math.atan(self.height / self.side_rest)
            self.min_dist_left = (
                (
                    self.panel_width
                    + self.distance_bottom
                    + self.abergement_bottom
                    + self.abergement_top
                )
                / math.tan(self.side_angle)
            ) + self.abergement_left
            self.min_dist_right = (
                (
                    self.panel_width
                    + self.distance_bottom
                    + self.abergement_bottom
                    + self.abergement_top
                )
                / math.tan(self.side_angle)
            ) + self.abergement_right

        self.horizontal_pose = 0
        self.vertical_pose = 0
        self.panel_left_triangle = []
        self.panel_right_triangle = []
        self.nb_pan_lentgh_left_triangle = 0
        self.nb_pan_lentgh_right_triangle = 0
        self.nb_pan_left_triangle = 0
        self.nb_pan_right_triangle = 0
        self.abergement = []
        self.panel = []

    def modif_width(self, implantation):
        if ((self.width - (self.nb_panel_width * self.panel_width)) / 2) < (
            implantation.distance_top + implantation.abergement_top
        ):
            self.width = (
                self.width - implantation.distance_top - implantation.abergement_top
            )
        else:
            self.distance_top = 0
            self.abergement_top = 0

        if ((self.width - (self.nb_panel_width * self.panel_width)) / 2) < (
            implantation.distance_bottom + implantation.abergement_bottom
        ):
            self.width = (
                self.width
                - implantation.distance_bottom
                - implantation.abergement_bottom
            )
        else:
            self.distance_bottom = 0
            self.abergement_bottom = 0

    def modif_length(self, implantation):

        if ((self.bottom_length - (self.nb_panel_length * self.panel_length)) / 2) < (
            implantation.distance_left + implantation.abergement_left
        ):
            self.bottom_length = (
                self.bottom_length
                - implantation.distance_left
                - implantation.abergement_left
            )
        else:
            self.distance_left = 0
            self.abergement_left = 0

        if ((self.bottom_length - (self.nb_panel_length * self.panel_length)) / 2) < (
            implantation.distance_right + implantation.abergement_right
        ):
            self.bottom_length = (
                self.bottom_length
                - implantation.distance_right
                - implantation.abergement_right
            )
        else:
            self.distance_right = 0
            self.abergement_right = 0

    def modif_top_length(self, implantation):
        if self.distance_left >= self.side_rest:
            self.top_length = self.top_length - (self.distance_left - self.side_rest)
            self.left_rest = 0
            self.nb_pan_left_triangle = 0
        else:
            self.left_rest = self.side_rest - self.distance_left - self.abergement_left
        if self.distance_right >= self.side_rest:
            self.top_length = self.top_length - (self.distance_right - self.side_rest)
            self.right_rest = 0
            self.nb_pan_right_triangle = 0
        else:
            self.right_rest = (
                self.side_rest - self.distance_right - self.abergement_right
            )

    def modif_height(self, implantation):
        if ((self.height - (self.nb_panel_width * self.panel_width)) / 2) < (
            implantation.distance_top + implantation.abergement_top
        ):
            self.height = (
                self.height - implantation.distance_top - implantation.abergement_top
            )
        else:
            self.distance_top = 0
            self.abergement_top = 0
        if ((self.height - (self.nb_panel_width * self.panel_width)) / 2) < (
            implantation.distance_bottom + implantation.abergement_bottom
        ):
            self.height = (
                self.height
                - implantation.distance_bottom
                - implantation.abergement_bottom
            )
        else:
            self.distance_bottom = 0
            self.abergement_bottom = 0
        self.vert_centering = (
            self.height - (self.nb_panel_width * self.panel_width)
        ) / 2

    def lateral_space(self, implantation):
        self.min_dist_left = (
            (
                self.panel_width
                + implantation.distance_bottom
                + implantation.abergement_bottom
                + implantation.abergement_top
                + self.vert_centering
            )
            / math.tan(self.side_angle)
        ) + self.abergement_left
        if (
            implantation.distance_left + implantation.abergement_left
            >= self.min_dist_left
        ):
            self.left_space = self.left_rest + self.hor_centering - self.horizontal_pose
        else:
            self.left_space = (
                self.left_rest
                + self.hor_centering
                - (
                    self.min_dist_left
                    - implantation.abergement_left
                    - implantation.distance_left
                )
                - self.horizontal_pose
            )
        self.nb_pan_lentgh_left_triangle = int(self.left_space / self.panel_length)
        if self.right_rest > 0:
            self.min_dist_right = (
                (
                    self.panel_width
                    + implantation.distance_bottom
                    + implantation.abergement_bottom
                    + implantation.abergement_top
                    + self.vert_centering
                )
                / math.tan(self.side_angle)
            ) + implantation.abergement_right
            if (
                implantation.distance_right + implantation.abergement_right
                >= self.min_dist_right
            ):
                self.right_space = (
                    self.right_rest + self.hor_centering - self.horizontal_pose
                )
            else:
                self.right_space = (
                    self.right_rest
                    + self.hor_centering
                    - (
                        self.min_dist_right
                        - implantation.abergement_right
                        - implantation.distance_right
                    )
                    - self.horizontal_pose
                )

            self.nb_pan_lentgh_right_triangle = int(
                self.right_space / self.panel_length
            )

    def Centering(self, implantation):
        if self.left_rest > 0:
            self.centering = (
                self.left_rest
                + self.hor_centering
                + implantation.distance_left
                + (2 * implantation.abergement_left)
                - (self.panel_length * self.nb_pan_lentgh_left_triangle)
            )
        else:
            if implantation.distance_left > self.side_rest:
                self.centering = (
                    self.side_rest
                    + (implantation.distance_left - self.side_rest)
                    + implantation.abergement_left
                    + self.hor_centering
                )
            else:
                self.centering = (
                    self.side_rest + implantation.abergement_left + self.hor_centering
                )

    def lateral_rest(self):
        if (
            (self.distance_left >= self.side_rest)
            or (self.abergement_left >= self.side_rest)
            or ((self.abergement_left + self.distance_left) >= self.side_rest)
        ):
            self.left_rest = 0
            self.nb_pan_lentgh_left_triangle = 0
        else:
            self.left_rest = self.side_rest - self.distance_left - self.abergement_left
        if (
            (self.distance_right >= self.side_rest)
            or (self.abergement_right >= self.side_rest)
            or ((self.abergement_right + self.distance_right) >= self.side_rest)
        ):
            self.right_rest = 0
            self.nb_pan_lentgh_right_triangle = 0
        else:
            self.right_rest = (
                self.side_rest - self.distance_right - self.abergement_right
            )

        if self.left_rest > 0:
            if self.distance_left + self.abergement_left >= self.min_dist_left:
                self.left_space = self.left_rest
            else:
                self.left_space = self.left_rest - (
                    self.min_dist_left - self.abergement_left - self.distance_left
                )

            self.nb_pan_lentgh_left_triangle = int(self.left_space / self.panel_length)
            self.centering = self.side_rest - (
                self.panel_length * self.nb_pan_lentgh_left_triangle
            )
        else:
            if self.distance_left > self.side_rest:
                self.centering = (
                    self.side_rest
                    + (self.distance_left - self.side_rest)
                    + self.abergement_left
                )
            else:
                self.centering = self.side_rest + self.abergement_left

        if self.right_rest > 0:
            if self.distance_right + self.abergement_right >= self.min_dist_right:
                self.right_space = self.right_rest
            else:
                self.right_space = self.right_rest - (
                    self.min_dist_right - self.abergement_right - self.distance_right
                )

            self.nb_pan_lentgh_right_triangle = int(
                self.right_space / self.panel_length
            )

    def set_panel_in_triangle_col(self, roof, implantation):
        self.panel_right_triangle = [
            0 for x in range(self.nb_pan_lentgh_right_triangle + 2)
        ]
        self.panel_left_triangle = [
            0 for x in range(self.nb_pan_lentgh_left_triangle + 2)
        ]
        if roof.roof_type_id_id == 2:
            for i in range(1, self.nb_pan_lentgh_left_triangle + 1):
                self.panel_left_triangle[i] = int(
                    (
                        (
                            (
                                self.centering
                                - implantation.abergement_left
                                + (self.panel_length * (i - 1))
                            )
                            * math.tan(self.side_angle)
                        )
                        - implantation.abergement_bottom
                        - implantation.distance_bottom
                        - implantation.abergement_top
                        - self.vert_centering
                    )
                    / self.panel_width
                )
                if self.panel_left_triangle[i] > self.nb_panel_width:
                    self.panel_left_triangle[i] = self.nb_panel_width
            for i in range(1, self.nb_pan_lentgh_right_triangle + 1):
                self.panel_right_triangle[i] = int(
                    (
                        (
                            roof.bottom_length
                            - self.centering
                            - (
                                self.panel_length
                                * (
                                    self.nb_pan_lentgh_left_triangle
                                    + self.nb_panel_length
                                )
                            )
                            - implantation.abergement_right
                            - (self.panel_length * (i - 1))
                            - self.panel_length
                        )
                        * math.tan(self.side_angle)
                        - implantation.abergement_top
                        - implantation.abergement_bottom
                        - implantation.distance_bottom
                        - self.vert_centering
                    )
                    / self.panel_width
                )
                if self.panel_right_triangle[i] > self.nb_panel_width:
                    self.panel_right_triangle[i] = self.nb_panel_width

        if roof.roof_type_id_id == 3:
            for i in range(1, self.nb_pan_lentgh_left_triangle + 1):
                self.vert_centering = (
                    (
                        (
                            self.centering
                            - implantation.abergement_left
                            + (self.panel_length * (i - 1))
                        )
                        * math.tan(self.side_angle)
                    )
                    - implantation.abergement_bottom
                    - implantation.distance_bottom
                    - implantation.abergement_top
                )
                if (
                    roof.height
                    - implantation.distance_top
                    - implantation.distance_bottom
                    - implantation.abergement_top
                    - implantation.abergement_bottom
                ) < self.vert_centering:
                    self.panel_left_triangle[i] = int(
                        (
                            roof.height
                            - implantation.distance_top
                            - implantation.distance_bottom
                            - implantation.abergement_top
                            - implantation.abergement_bottom
                        )
                        / self.panel_width
                    )
                else:
                    self.panel_left_triangle[i] = int(
                        self.vert_centering / self.panel_width
                    )
            for i in range(1, self.nb_pan_lentgh_right_triangle + 1):
                self.vert_centering = (
                    (
                        roof.bottom_length
                        - self.centering
                        - (self.panel_length * self.nb_pan_lentgh_left_triangle)
                        - implantation.abergement_right
                        - (self.panel_length * (i - 1))
                        - self.panel_length
                    )
                    * math.tan(self.side_angle)
                    - implantation.abergement_top
                    - implantation.abergement_bottom
                    - implantation.distance_bottom
                )
                if (
                    roof.height
                    - implantation.distance_top
                    - implantation.distance_bottom
                    - implantation.abergement_top
                    - implantation.abergement_bottom
                ) < self.vert_centering:
                    self.panel_right_triangle[i] = int(
                        (
                            roof.height
                            - implantation.distance_top
                            - implantation.distance_bottom
                            - implantation.abergement_top
                            - implantation.abergement_bottom
                        )
                        / self.panel_width
                    )
                else:
                    self.panel_right_triangle[i] = int(
                        (
                            (
                                roof.bottom_length
                                - self.centering
                                - (
                                    self.panel_length
                                    * (
                                        self.nb_pan_lentgh_left_triangle
                                        + self.nb_panel_length
                                    )
                                )
                                - implantation.abergement_right
                                - (self.panel_length * (i - 1))
                                - self.panel_length
                            )
                            * math.tan(self.side_angle)
                            - implantation.abergement_top
                            - implantation.abergement_bottom
                            - implantation.distance_bottom
                        )
                        / self.panel_width
                    )

    def Set_nb_pan_in_triangle_length(self, roof, implantation):
        if roof.roof_type_id_id == 2:
            self.vert_centering = (
                self.height
                - (self.nb_panel_width * self.panel_width)
                - self.vertical_pose * (self.nb_panel_width - 1)
            ) / 2
            self.hor_centering = (
                self.top_length
                - self.nb_panel_length * self.panel_length
                - self.horizontal_pose * (self.nb_panel_length - 1)
            ) / 2

            if self.left_rest > 0:
                self.lateral_space(implantation)
                temp_nb_pan = self.nb_pan_lentgh_left_triangle
                temp_left_space = self.left_space
                self.nb_pan_lentgh_left_triangle = self.update_tempnbpan(
                    implantation, temp_nb_pan, temp_left_space,
                )
                if implantation.panel_implantation_id == 2:
                    while (
                        self.nb_pan_lentgh_left_triangle * self.panel_length
                        + self.horizontal_pose * (self.nb_pan_lentgh_left_triangle - 1)
                    ) < self.left_space:
                        self.nb_pan_lentgh_left_triangle = (
                            self.nb_pan_lentgh_left_triangle + 1
                        )
                    while (
                        self.nb_pan_lentgh_left_triangle * self.panel_length
                        + self.horizontal_pose * (self.nb_pan_lentgh_left_triangle - 1)
                    ) > self.left_space:
                        i = 1
                        self.nb_pan_lentgh_left_triangle = (
                            self.nb_pan_lentgh_left_triangle - 1
                        )
                        self.panel_left_triangle[i] = self.panel_left_triangle[i + 1]
                        i += 1

            if self.nb_pan_lentgh_right_triangle != 0:
                temp_nb_pan = self.nb_pan_lentgh_right_triangle
                temp_left_space = self.right_space - self.horizontal_pose
                self.nb_pan_lentgh_right_triangle = self.update_tempnbpan(
                    implantation, temp_nb_pan, temp_left_space
                )
                if implantation.panel_implantation_id == 2:
                    while (
                        self.nb_pan_lentgh_right_triangle * self.panel_length
                        + self.horizontal_pose * (self.nb_pan_lentgh_right_triangle - 1)
                    ) < self.right_space + self.horizontal_pose:
                        self.nb_pan_lentgh_right_triangle = (
                            self.nb_pan_lentgh_right_triangle + 1
                        )
                    while (
                        self.nb_pan_lentgh_right_triangle * self.panel_length
                        + self.horizontal_pose * (self.nb_pan_lentgh_right_triangle - 1)
                    ) > self.right_space + self.horizontal_pose:
                        self.nb_pan_lentgh_right_triangle = (
                            self.nb_pan_lentgh_right_triangle - 1
                        )

            if self.nb_pan_lentgh_left_triangle < 0:
                self.nb_pan_lentgh_left_triangle = 0
            if self.nb_pan_lentgh_left_triangle == 0:
                if implantation.distance_left > self.side_rest:
                    self.centering = (
                        self.side_rest
                        + (implantation.distance_left - self.side_rest)
                        + implantation.abergement_left
                        + self.hor_centering
                    )
                else:
                    self.centering = (
                        self.side_rest
                        + implantation.abergement_left
                        + self.hor_centering
                    )
            else:
                self.centering = (
                    self.side_rest
                    + self.hor_centering
                    + implantation.abergement_left
                    - self.nb_pan_lentgh_left_triangle
                    * (self.panel_length + self.horizontal_pose)
                )
            if self.nb_pan_lentgh_right_triangle < 0:
                self.nb_pan_lentgh_right_triangle = 0

        if roof.roof_type_id_id == 3:
            if implantation.panel_implantation_id == 2:
                if self.left_rest > 0:
                    self.min_dist_left = (
                        (
                            self.panel_width
                            + implantation.distance_bottom
                            + implantation.abergement_bottom
                            + implantation.abergement_top
                        )
                        / math.tan(self.side_angle)
                    ) + implantation.abergement_left
                    if (
                        implantation.distance_left + implantation.abergement_left
                        >= self.min_dist_left
                    ):
                        self.left_space = self.left_rest - (self.horizontal_pose / 2)
                    else:
                        self.left_space = (
                            self.left_rest
                            - (
                                self.min_dist_left
                                - implantation.abergement_left
                                - implantation.distance_left
                            )
                            - (self.horizontal_pose / 2)
                        )

                    while (
                        self.nb_pan_lentgh_left_triangle * self.panel_length
                        + self.horizontal_pose * (self.nb_pan_lentgh_left_triangle - 1)
                    ) > self.left_space:
                        i = 1
                        self.nb_pan_lentgh_left_triangle = (
                            self.nb_pan_lentgh_left_triangle - 1
                        )
                        self.panel_left_triangle[i] = self.panel_left_triangle[i + 1]
                        i += 1
                    self.centering = (
                        self.side_rest
                        - (self.panel_length * self.nb_pan_lentgh_left_triangle)
                        - (
                            self.horizontal_pose
                            * (self.nb_pan_lentgh_left_triangle - 1)
                        )
                        - (self.horizontal_pose / 2)
                    )
                else:
                    if implantation.distance_left > self.side_rest:
                        self.centering = (
                            self.side_rest
                            + (implantation.distance_left - self.side_rest)
                            + implantation.abergement_left
                        )
                    else:
                        self.centering = self.side_rest + implantation.abergement_left
                if self.nb_pan_lentgh_left_triangle < 0:
                    self.nb_pan_lentgh_left_triangle = 0

                if self.right_rest > 0:
                    self.min_dist_right = (
                        (
                            self.panel_width
                            + implantation.distance_bottom
                            + implantation.abergement_bottom
                            + implantation.abergement_top
                        )
                        / math.tan(self.side_angle)
                    ) + implantation.abergement_right
                    if (
                        implantation.distance_right + implantation.abergement_right
                        >= self.min_dist_right
                    ):
                        self.right_space = self.right_rest - (self.horizontal_pose / 2)
                    else:
                        self.right_space = (
                            self.right_rest
                            - (
                                self.min_dist_right
                                - implantation.abergement_right
                                - implantation.distance_right
                            )
                            - (self.horizontal_pose / 2)
                        )

                    while (
                        self.nb_pan_lentgh_right_triangle * self.panel_length
                        + self.horizontal_pose * (self.nb_pan_lentgh_right_triangle - 1)
                    ) < self.right_space:
                        self.nb_pan_lentgh_right_triangle = (
                            self.nb_pan_lentgh_right_triangle + 1
                        )
                    while (
                        self.nb_pan_lentgh_right_triangle * self.panel_length
                        + self.horizontal_pose * (self.nb_pan_lentgh_right_triangle - 1)
                    ) > self.right_space:
                        self.nb_pan_lentgh_right_triangle = (
                            self.nb_pan_lentgh_right_triangle - 1
                        )

                if self.nb_pan_lentgh_right_triangle < 0:
                    self.nb_pan_lentgh_right_triangle = 0
            if implantation.panel_implantation_id == 3:
                if self.left_rest > 0:
                    self.min_dist_left = (
                        (
                            self.panel_width
                            + implantation.distance_bottom
                            + implantation.abergement_bottom
                            + implantation.abergement_top
                        )
                        / math.tan(self.side_angle)
                    ) + implantation.abergement_left
                    if (
                        implantation.distance_left + implantation.abergement_left
                        >= self.min_dist_left
                    ):
                        self.left_space = self.left_rest
                    else:
                        self.left_space = self.left_rest - (
                            self.min_dist_left
                            - implantation.abergement_left
                            - implantation.distance_left
                        )

                    while (
                        self.nb_pan_lentgh_left_triangle * self.panel_length
                        - self.horizontal_pose * (self.nb_pan_lentgh_left_triangle - 1)
                    ) > self.left_space:
                        self.nb_pan_lentgh_left_triangle = (
                            self.nb_pan_lentgh_left_triangle - 1
                        )
                    while (
                        self.nb_pan_lentgh_left_triangle * self.panel_length
                        - self.horizontal_pose * (self.nb_pan_lentgh_left_triangle - 1)
                    ) < self.left_space:
                        self.nb_pan_lentgh_left_triangle = (
                            self.nb_pan_lentgh_left_triangle + 1
                        )
                    self.nb_pan_lentgh_left_triangle = (
                        self.nb_pan_lentgh_left_triangle - 1
                    )

                    self.centering = (
                        self.side_rest
                        - (self.panel_length * self.nb_pan_lentgh_left_triangle)
                        + (
                            self.horizontal_pose
                            * (self.nb_pan_lentgh_left_triangle - 1)
                        )
                    )
                else:
                    if implantation.distance_left > self.side_rest:
                        self.centering = (
                            self.side_rest
                            + (implantation.distance_left - self.side_rest)
                            + implantation.abergement_left
                        )
                    else:
                        self.centering = self.side_rest + implantation.abergement_left
                if self.nb_pan_lentgh_left_triangle < 0:
                    self.nb_pan_lentgh_left_triangle = 0

                if self.right_rest > 0:
                    self.min_dist_right = (
                        (
                            self.panel_width
                            + implantation.distance_bottom
                            + implantation.abergement_bottom
                            + implantation.abergement_top
                        )
                        / math.tan(self.side_angle)
                    ) + implantation.abergement_right
                    if (
                        implantation.distance_right + implantation.abergement_right
                        >= self.min_dist_right
                    ):
                        self.right_space = self.right_rest + self.horizontal_pose
                    else:
                        self.right_space = (
                            self.right_rest
                            - (
                                self.min_dist_right
                                - implantation.abergement_right
                                - implantation.distance_right
                            )
                            + self.horizontal_pose
                        )

                    while (
                        self.nb_pan_lentgh_right_triangle * self.panel_length
                        - self.horizontal_pose * (self.nb_pan_lentgh_right_triangle - 1)
                    ) > self.right_space + self.horizontal_pose:
                        self.nb_pan_lentgh_right_triangle = (
                            self.nb_pan_lentgh_right_triangle - 1
                        )
                    while (
                        self.nb_pan_lentgh_right_triangle * self.panel_length
                        - self.horizontal_pose * (self.nb_pan_lentgh_right_triangle - 1)
                    ) < self.right_space + self.horizontal_pose:
                        self.nb_pan_lentgh_right_triangle = (
                            self.nb_pan_lentgh_right_triangle + 1
                        )
                    self.nb_pan_lentgh_right_triangle = (
                        self.nb_pan_lentgh_right_triangle - 1
                    )

                if self.nb_pan_lentgh_right_triangle < 0:
                    self.nb_pan_lentgh_right_triangle = 0

    def update_tempnbpan(self, implantation, temp_nb_pan, temp_left_space):
        if implantation.panel_implantation_id == 3:
            while (
                temp_nb_pan * self.panel_length
                + self.horizontal_pose * (temp_nb_pan - 1)
            ) < temp_left_space:
                temp_nb_pan = temp_nb_pan + 1
            temp_nb_pan = temp_nb_pan - 1
        return temp_nb_pan

    def set_rest(self):
        self.left_rest = (
            self.distance_left
            + self.abergement_left
            + (
                self.bottom_length
                - (self.nb_panel_length * self.panel_length)
                - self.horizontal_pose * (self.nb_panel_length - 1)
            )
            / 2
        )
        self.right_rest = (
            self.distance_right
            + self.abergement_right
            + (
                self.bottom_length
                - (self.nb_panel_length * self.panel_length)
                - self.horizontal_pose * (self.nb_panel_length - 1)
            )
            / 2
        )
        self.top_rest = (
            self.distance_top
            + self.abergement_top
            + (
                self.width
                - (self.nb_panel_width * self.panel_width)
                - self.vertical_pose * (self.nb_panel_width - 1)
            )
            / 2
        )
        self.bottom_rest = (
            self.distance_bottom
            + self.abergement_bottom
            + (
                self.width
                - (self.nb_panel_width * self.panel_width)
                - self.vertical_pose * (self.nb_panel_width - 1)
            )
            / 2
        )

    def reset_pan_in_col(self, roof, implantation):
        A = 0
        i = 0
        if roof.roof_type_id_id == 2:
            if implantation.panel_implantation_id == 2:
                for i in range(1, self.nb_pan_lentgh_left_triangle + 1):
                    while (
                        self.panel_left_triangle[i] * self.panel_width
                        + self.vertical_pose * (self.panel_left_triangle[i] - 1)
                    ) < (
                        (
                            (
                                self.centering
                                - implantation.abergement_left
                                + ((self.panel_length + self.horizontal_pose) * (i - 1))
                            )
                            * math.tan(self.side_angle)
                        )
                        - implantation.abergement_bottom
                        - implantation.distance_bottom
                        - implantation.abergement_top
                        - self.vert_centering
                    ):
                        self.panel_left_triangle[i] = self.panel_left_triangle[i] + 1
                    while (
                        self.panel_left_triangle[i] * self.panel_width
                        + self.vertical_pose * (self.panel_left_triangle[i] - 1)
                    ) > (
                        (
                            (
                                self.centering
                                - implantation.abergement_left
                                + ((self.panel_length + self.horizontal_pose) * (i - 1))
                            )
                            * math.tan(self.side_angle)
                        )
                        - implantation.abergement_bottom
                        - implantation.distance_bottom
                        - implantation.abergement_top
                        - self.vert_centering
                    ):
                        self.panel_left_triangle[i] = self.panel_left_triangle[i] - 1
                    if self.panel_left_triangle[i] > self.nb_panel_width:
                        self.panel_left_triangle[i] = self.nb_panel_width
                    if self.panel_left_triangle[i] <= 0:
                        self.nb_pan_lentgh_left_triangle -= 1
                        A += 1

                for i in range(0, A):
                    for i in range(1, self.panel_left_triangle.Length - 1):
                        self.panel_left_triangle[i] = self.panel_left_triangle[i + 1]
                A = 0

                self.right_rest = (
                    roof.bottom_length
                    - self.centering
                    - (
                        (self.nb_pan_lentgh_left_triangle + self.nb_panel_length)
                        * (self.panel_length + self.horizontal_pose)
                    )
                )

                for i in range(1, self.nb_pan_lentgh_right_triangle + 1):
                    while (
                        self.panel_right_triangle[i] * self.panel_width
                        + self.vertical_pose * (self.panel_right_triangle[i] - 1)
                    ) < (
                        (
                            (
                                self.right_rest
                                - implantation.abergement_right
                                - ((self.panel_length + self.horizontal_pose) * (i - 1))
                                - self.panel_length
                            )
                            * math.tan(self.side_angle)
                        )
                        - implantation.abergement_bottom
                        - implantation.distance_bottom
                        - implantation.abergement_top
                        - self.vert_centering
                    ):
                        self.panel_right_triangle[i] = self.panel_right_triangle[i] + 1
                    while (
                        self.panel_right_triangle[i] * self.panel_width
                        + self.vertical_pose * (self.panel_right_triangle[i] - 1)
                    ) > (
                        (
                            (
                                self.right_rest
                                - implantation.abergement_right
                                - ((self.panel_length + self.horizontal_pose) * (i - 1))
                                - self.panel_length
                            )
                            * math.tan(self.side_angle)
                        )
                        - implantation.abergement_bottom
                        - implantation.distance_bottom
                        - implantation.abergement_top
                        - self.vert_centering
                    ):
                        self.panel_right_triangle[i] = self.panel_right_triangle[i] - 1
                    if self.panel_right_triangle[i] == 0:
                        self.nb_pan_lentgh_right_triangle -= 1
                    if self.panel_right_triangle[i] > self.nb_panel_width:
                        self.panel_right_triangle[i] = self.nb_panel_width

                self.panel_right_triangle[i] = 0

            if implantation.panel_implantation_id == 3:
                for i in range(1, self.nb_pan_lentgh_left_triangle + 1):
                    while (
                        self.panel_left_triangle[i] * self.panel_width
                        + self.vertical_pose * (self.panel_left_triangle[i] - 1)
                    ) > (
                        (
                            (
                                self.centering
                                - implantation.abergement_left
                                + ((self.panel_length + self.horizontal_pose) * (i - 1))
                            )
                            * math.tan(self.side_angle)
                        )
                        - implantation.abergement_bottom
                        - implantation.distance_bottom
                        - implantation.abergement_top
                        - self.vert_centering
                    ):
                        self.panel_left_triangle[i] = self.panel_left_triangle[i] - 1
                    while (
                        self.panel_left_triangle[i] * self.panel_width
                        + self.vertical_pose * (self.panel_left_triangle[i] - 1)
                    ) < (
                        (
                            (
                                self.centering
                                - implantation.abergement_left
                                + ((self.panel_length + self.horizontal_pose) * (i - 1))
                            )
                            * math.tan(self.side_angle)
                        )
                        - implantation.abergement_bottom
                        - implantation.distance_bottom
                        - implantation.abergement_top
                        - self.vert_centering
                    ):
                        self.panel_left_triangle[i] = self.panel_left_triangle[i] + 1

                    self.panel_left_triangle[i] = self.panel_left_triangle[i] - 1
                    if self.panel_left_triangle[i] > self.nb_panel_width:
                        self.panel_left_triangle[i] = self.nb_panel_width
                    if self.panel_left_triangle[i] <= 0:
                        self.nb_pan_lentgh_left_triangle -= 1
                        A += 1

                self.right_rest = (
                    roof.bottom_length
                    - self.centering
                    - (
                        (self.nb_pan_lentgh_left_triangle + self.nb_panel_length)
                        * (self.panel_length + self.horizontal_pose)
                    )
                )

                for i in range(1, self.nb_pan_lentgh_right_triangle + 1):
                    while (
                        self.panel_right_triangle[i] * self.panel_width
                        + self.vertical_pose * (self.panel_right_triangle[i] - 1)
                    ) > (
                        (
                            (
                                self.right_rest
                                - implantation.abergement_right
                                - ((self.panel_length + self.horizontal_pose) * (i - 1))
                                - self.panel_length
                            )
                            * math.tan(self.side_angle)
                        )
                        - implantation.abergement_bottom
                        - implantation.distance_bottom
                        - implantation.abergement_top
                        - self.vert_centering
                    ):
                        self.panel_right_triangle[i] = self.panel_right_triangle[i] - 1
                    while (
                        self.panel_right_triangle[i] * self.panel_width
                        + self.vertical_pose * (self.panel_right_triangle[i] - 1)
                    ) < (
                        (
                            (
                                self.right_rest
                                - implantation.abergement_right
                                - ((self.panel_length + self.horizontal_pose) * (i - 1))
                                - self.panel_length
                            )
                            * math.tan(self.side_angle)
                        )
                        - implantation.abergement_bottom
                        - implantation.distance_bottom
                        - implantation.abergement_top
                        - self.vert_centering
                    ):
                        self.panel_right_triangle[i] = self.panel_right_triangle[i] + 1

                    self.panel_right_triangle[i] = self.panel_right_triangle[i] - 1
                    if self.panel_right_triangle[i] == 0:
                        self.nb_pan_lentgh_right_triangle -= 1
                    if self.panel_right_triangle[i] > self.nb_panel_width:
                        self.panel_right_triangle[i] = self.nb_panel_width
                self.panel_right_triangle[i] = 0

            if (self.nb_panel_length <= 0) or (self.nb_panel_width <= 0):
                self.nb_pan_lentgh_right_triangle = 0
                self.nb_pan_lentgh_left_triangle = 0

        if roof.roof_type_id_id == 3:
            if implantation.panel_implantation_id == 2:
                for i in range(1, self.nb_pan_lentgh_left_triangle + 1):
                    self.vert_centering = (
                        (
                            (
                                self.centering
                                - implantation.abergement_left
                                + ((self.panel_length + self.horizontal_pose) * (i - 1))
                            )
                            * math.tan(self.side_angle)
                        )
                        - implantation.abergement_bottom
                        - implantation.distance_bottom
                        - implantation.abergement_top
                    )
                    if (
                        roof.height
                        - implantation.distance_top
                        - implantation.distance_bottom
                        - implantation.abergement_top
                        - implantation.abergement_bottom
                    ) > self.vert_centering:
                        while (
                            self.panel_left_triangle[i] * self.panel_width
                            + self.vertical_pose * (self.panel_left_triangle[i] - 1)
                        ) < self.vert_centering:
                            self.panel_left_triangle[i] = (
                                self.panel_left_triangle[i] + 1
                            )
                        while (
                            self.panel_left_triangle[i] * self.panel_width
                            + self.vertical_pose * (self.panel_left_triangle[i] - 1)
                        ) > self.vert_centering:
                            self.panel_left_triangle[i] = (
                                self.panel_left_triangle[i] - 1
                            )

                        if self.panel_left_triangle[i] <= 0:
                            self.nb_pan_lentgh_left_triangle -= 1
                    else:
                        while (
                            self.panel_left_triangle[i] * self.panel_width
                            + self.vertical_pose * (self.panel_left_triangle[i] - 1)
                        ) < (
                            roof.height
                            - implantation.distance_top
                            - implantation.distance_bottom
                            - implantation.abergement_top
                            - implantation.abergement_bottom
                        ):
                            self.panel_left_triangle[i] = (
                                self.panel_left_triangle[i] + 1
                            )
                        while (
                            self.panel_left_triangle[i] * self.panel_width
                            + self.vertical_pose * (self.panel_left_triangle[i] - 1)
                        ) > (
                            roof.height
                            - implantation.distance_top
                            - implantation.distance_bottom
                            - implantation.abergement_top
                            - implantation.abergement_bottom
                        ):
                            self.panel_left_triangle[i] = (
                                self.panel_left_triangle[i] - 1
                            )
                        if self.panel_left_triangle[i] <= 0:
                            self.nb_pan_lentgh_left_triangle -= 1
                            A += 1

                for i in range(0, A):
                    for i in range(1, self.panel_left_triangle.Length - 1):
                        self.panel_left_triangle[i] = self.panel_left_triangle[i + 1]

                for i in range(1, self.nb_pan_lentgh_right_triangle + 1):
                    self.vert_centering = (
                        (
                            roof.bottom_length
                            - self.centering
                            - (
                                (self.panel_length + self.horizontal_pose)
                                * self.nb_pan_lentgh_left_triangle
                            )
                            - implantation.abergement_right
                            - ((self.panel_length + self.horizontal_pose) * (i - 1))
                            - self.panel_length
                        )
                        * math.tan(self.side_angle)
                        - implantation.abergement_top
                        - implantation.abergement_bottom
                        - implantation.distance_bottom
                    )
                    if (
                        roof.height
                        - implantation.distance_top
                        - implantation.distance_bottom
                        - implantation.abergement_top
                        - implantation.abergement_bottom
                    ) > self.vert_centering:
                        while (
                            self.panel_right_triangle[i] * self.panel_width
                            + self.vertical_pose * (self.panel_right_triangle[i] - 1)
                        ) < self.vert_centering:
                            self.panel_right_triangle[i] = (
                                self.panel_right_triangle[i] + 1
                            )
                        while (
                            self.panel_right_triangle[i] * self.panel_width
                            + self.vertical_pose * (self.panel_right_triangle[i] - 1)
                        ) > self.vert_centering:
                            self.panel_right_triangle[i] = (
                                self.panel_right_triangle[i] - 1
                            )
                        if self.panel_right_triangle[i] == 0:
                            self.nb_pan_lentgh_right_triangle -= 1
                    else:
                        while (
                            self.panel_right_triangle[i] * self.panel_width
                            + self.vertical_pose * (self.panel_right_triangle[i] - 1)
                        ) < (
                            roof.height
                            - implantation.distance_top
                            - implantation.distance_bottom
                            - implantation.abergement_top
                            - implantation.abergement_bottom
                        ):
                            self.panel_right_triangle[i] = (
                                self.panel_right_triangle[i] + 1
                            )
                        while (
                            self.panel_right_triangle[i] * self.panel_width
                            + self.vertical_pose * (self.panel_right_triangle[i] - 1)
                        ) > (
                            roof.height
                            - implantation.distance_top
                            - implantation.distance_bottom
                            - implantation.abergement_top
                            - implantation.abergement_bottom
                        ):
                            self.panel_right_triangle[i] = (
                                self.panel_right_triangle[i] - 1
                            )
                        if self.panel_right_triangle[i] == 0:
                            self.nb_pan_lentgh_right_triangle -= 1

                i += 1
                self.panel_right_triangle[i] = 0

            if implantation.panel_implantation_id == 3:
                for i in range(1, self.nb_pan_lentgh_left_triangle + 1):
                    self.vert_centering = (
                        (
                            (
                                self.centering
                                - implantation.abergement_left
                                + ((self.panel_length + self.horizontal_pose) * (i - 1))
                            )
                            * math.tan(self.side_angle)
                        )
                        - implantation.abergement_bottom
                        - implantation.distance_bottom
                        - implantation.abergement_top
                    )
                    if (
                        roof.height
                        - implantation.distance_top
                        - implantation.distance_bottom
                        - implantation.abergement_top
                        - implantation.abergement_bottom
                    ) > self.vert_centering:
                        while (
                            self.panel_left_triangle[i] * self.panel_width
                            + self.vertical_pose * (self.panel_left_triangle[i] - 1)
                        ) > self.vert_centering:
                            self.panel_left_triangle[i] = (
                                self.panel_left_triangle[i] - 1
                            )
                        while (
                            self.panel_left_triangle[i] * self.panel_width
                            + self.vertical_pose * (self.panel_left_triangle[i] - 1)
                        ) < self.vert_centering:
                            self.panel_left_triangle[i] = (
                                self.panel_left_triangle[i] + 1
                            )
                        self.panel_left_triangle[i] = self.panel_left_triangle[i] - 1

                        if self.panel_left_triangle[i] <= 0:
                            self.nb_pan_lentgh_left_triangle -= 1
                            A += 1
                    else:
                        while (
                            (
                                self.panel_left_triangle[i] * self.panel_width
                                + self.vertical_pose * (self.panel_left_triangle[i] - 1)
                            )
                            > roof.height
                            - implantation.distance_top
                            - implantation.distance_bottom
                            - implantation.abergement_top
                            - implantation.abergement_bottom
                        ):
                            self.panel_left_triangle[i] = (
                                self.panel_left_triangle[i] - 1
                            )
                        while (
                            (
                                self.panel_left_triangle[i] * self.panel_width
                                + self.vertical_pose * (self.panel_left_triangle[i] - 1)
                            )
                            < roof.height
                            - implantation.distance_top
                            - implantation.distance_bottom
                            - implantation.abergement_top
                            - implantation.abergement_bottom
                        ):
                            self.panel_left_triangle[i] = (
                                self.panel_left_triangle[i] + 1
                            )
                        self.panel_left_triangle[i] = self.panel_left_triangle[i] - 1

                        if self.panel_left_triangle[i] <= 0:
                            self.nb_pan_lentgh_left_triangle -= 1
                            A += 1

                for i in range(0, A):
                    for i in range(1, self.panel_left_triangle.Length - 1):
                        self.panel_left_triangle[i] = self.panel_left_triangle[i + 1]

                for i in range(1, self.nb_pan_lentgh_right_triangle + 1):
                    self.vert_centering = (
                        (
                            roof.bottom_length
                            - self.centering
                            - (
                                (self.panel_length + self.horizontal_pose)
                                * self.nb_pan_lentgh_left_triangle
                            )
                            - implantation.abergement_right
                            - ((self.panel_length + self.horizontal_pose) * (i - 1))
                            - self.panel_length
                        )
                        * math.tan(self.side_angle)
                        - implantation.abergement_top
                        - implantation.abergement_bottom
                        - implantation.distance_bottom
                    )
                    if (
                        roof.height
                        - implantation.distance_top
                        - implantation.distance_bottom
                        - implantation.abergement_top
                        - implantation.abergement_bottom
                    ) > self.vert_centering:
                        while (
                            self.panel_right_triangle[i] * self.panel_width
                            + self.vertical_pose * (self.panel_right_triangle[i] - 1)
                        ) > self.vert_centering:
                            self.panel_right_triangle[i] = (
                                self.panel_right_triangle[i] - 1
                            )
                        while (
                            self.panel_right_triangle[i] * self.panel_width
                            + self.vertical_pose * (self.panel_right_triangle[i] - 1)
                        ) < self.vert_centering:
                            self.panel_right_triangle[i] = (
                                self.panel_right_triangle[i] + 1
                            )
                        self.panel_right_triangle[i] = self.panel_right_triangle[i] - 1

                        if self.panel_right_triangle[i] == 0:
                            self.nb_pan_lentgh_right_triangle -= 1
                    else:
                        while (
                            self.panel_right_triangle[i] * self.panel_width
                            + self.vertical_pose * (self.panel_right_triangle[i] - 1)
                        ) > (
                            roof.height
                            - implantation.distance_top
                            - implantation.distance_bottom
                            - implantation.abergement_top
                            - implantation.abergement_bottom
                        ):
                            self.panel_right_triangle[i] = (
                                self.panel_right_triangle[i] - 1
                            )
                        while (
                            self.panel_right_triangle[i] * self.panel_width
                            + self.vertical_pose * (self.panel_right_triangle[i] - 1)
                        ) < (
                            roof.height
                            - implantation.distance_top
                            - implantation.distance_bottom
                            - implantation.abergement_top
                            - implantation.abergement_bottom
                        ):
                            self.panel_right_triangle[i] = (
                                self.panel_right_triangle[i] + 1
                            )
                        self.panel_right_triangle[i] = self.panel_right_triangle[i] - 1

                        if self.panel_right_triangle[i] == 0:
                            self.nb_pan_lentgh_right_triangle -= 1

                i += 1
                self.panel_right_triangle[i] = 0

    def set_pose(self, implantation):
        if implantation.panel_implantation_id == 1:
            self.horizontal_pose = 0
            self.vertical_pose = 0
        if implantation.panel_implantation_id == 2:
            self.vertical_pose = implantation.vertical_spacing
            self.horizontal_pose = implantation.horizontal_spacing
        if implantation.panel_implantation_id == 3:
            self.vertical_pose = 0 - implantation.vertical_overlapping
            self.horizontal_pose = 0 - implantation.horizontal_overlapping

    def update_roof_available_size(self, roof, implantation):
        if (implantation.panel_implantation_id == 2) or (
            implantation.panel_implantation_id == 3
        ):
            if (roof.roof_type_id_id == 1) or (roof.roof_type_id_id == 2):
                self.temp_pan_width = (
                    self.nb_panel_width * self.panel_width
                    + self.vertical_pose * (self.nb_panel_width - 1)
                )
                self.temp_pan_length = (
                    self.nb_panel_length * self.panel_length
                    + self.horizontal_pose * (self.nb_panel_length - 1)
                )

    def pan_in_width(self, roof):
        if roof.roof_type_id_id == 1:
            self.nb_panel_width = int(self.width / self.panel_width)
        elif roof.roof_type_id_id == 2:
            self.nb_panel_width = int(self.height / self.panel_width)

    def pan_in_length(self, roof):
        if roof.roof_type_id_id == 1:
            self.nb_panel_length = int(self.bottom_length / self.panel_length)
        elif roof.roof_type_id_id == 2:
            self.nb_panel_length = int(self.top_length / self.panel_length)

    def set_pan_in_width(self, roof, implantation):
        if implantation.panel_implantation_id == 2:
            if roof.roof_type_id_id == 1:
                while self.temp_pan_width > self.width:
                    self.nb_panel_width = self.nb_panel_width - 1
                    self.update_roof_available_size(roof, implantation)
            if roof.roof_type_id_id == 2:
                while self.temp_pan_width < self.height:
                    self.nb_panel_width = self.nb_panel_width + 1
                    self.update_roof_available_size(roof, implantation)
                while self.temp_pan_width > self.height:
                    self.nb_panel_width = self.nb_panel_width - 1
                    self.update_roof_available_size(roof, implantation)

        if implantation.panel_implantation_id == 3:
            if roof.roof_type_id_id == 1:
                while self.temp_pan_width < self.width:
                    self.nb_panel_width = self.nb_panel_width + 1
                    self.update_roof_available_size(roof, implantation)
                self.nb_panel_width = self.nb_panel_width - 1
            if roof.roof_type_id_id == 2:
                while self.temp_pan_width > self.height:
                    self.nb_panel_width = self.nb_panel_width - 1
                    self.update_roof_available_size(roof, implantation)
                while self.temp_pan_width < self.height:
                    self.nb_panel_width = self.nb_panel_width + 1
                    self.update_roof_available_size(roof, implantation)
                self.nb_panel_width = self.nb_panel_width - 1

    def set_pan_in_length(self, roof, implantation):
        if implantation.panel_implantation_id == 2:
            if roof.roof_type_id_id == 1:
                while self.temp_pan_length > self.bottom_length:
                    self.nb_panel_length = self.nb_panel_length - 1
                    self.update_roof_available_size(roof, implantation)
            if roof.roof_type_id_id == 2:
                while self.temp_pan_length < self.top_length:
                    self.nb_panel_length = self.nb_panel_length + 1
                    self.update_roof_available_size(roof, implantation)
                while self.temp_pan_length > self.top_length:
                    self.nb_panel_length = self.nb_panel_length - 1
                    self.update_roof_available_size(roof, implantation)

        if implantation.panel_implantation_id == 3:
            if roof.roof_type_id_id == 1:
                while self.temp_pan_length < self.bottom_length:
                    self.nb_panel_length = self.nb_panel_length + 1
                    self.update_roof_available_size(roof, implantation)
                self.nb_panel_length = self.nb_panel_length - 1
            if roof.roof_type_id_id == 2:
                while self.temp_pan_length > self.top_length:
                    self.nb_panel_length = self.nb_panel_length - 1
                    self.update_roof_available_size(roof, implantation)
                while self.temp_pan_length < self.top_length:
                    self.nb_panel_length = self.nb_panel_length + 1
                    self.update_roof_available_size(roof, implantation)
                self.nb_panel_length = self.nb_panel_length - 1

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def plot_data(self, roof, implantation):
        # region toit 1
        M = 0
        N = 0
        A = 0
        B = 0
        C = 0
        D = 0
        pan_num = 0
        j = []
        abergement_length = 0
        abergement_height = 0

        if roof.roof_type_id_id == 1:
            for i in range(0, self.nb_panel_length):
                for i1 in range(0, self.nb_panel_width):
                    if i1 == self.nb_panel_width - 1:
                        if i == 0:
                            x = (
                                self.left_rest
                                - self.abergement_left
                                + N * (self.panel_length + self.horizontal_pose)
                            )
                            abergement_length = (
                                self.panel_length
                                + self.abergement_left
                                + self.horizontal_pose
                            )
                        else:
                            x = self.left_rest + N * (
                                self.panel_length + self.horizontal_pose
                            )
                            if i == self.nb_panel_length - 1:
                                abergement_length = (
                                    self.panel_length + self.abergement_right
                                )
                            else:
                                abergement_length = (
                                    self.panel_length + self.horizontal_pose
                                )
                        y = (
                            self.top_rest
                            + M * (self.panel_width + self.vertical_pose)
                            + self.panel_width
                        )
                        self.abergement.append(
                            [x, y, abergement_length, self.abergement_bottom]
                        )
                        A += 1
                    if i1 == 0:
                        if i == 0:
                            x = (
                                self.left_rest
                                - self.abergement_left
                                + N * (self.panel_length + self.horizontal_pose)
                            )
                            abergement_length = (
                                self.panel_length
                                + self.abergement_left
                                + self.horizontal_pose
                            )
                        else:
                            x = self.left_rest + N * (
                                self.panel_length + self.horizontal_pose
                            )
                            if i == self.nb_panel_length - 1:
                                abergement_length = (
                                    self.panel_length + self.abergement_right
                                )
                            else:
                                abergement_length = (
                                    self.panel_length + self.horizontal_pose
                                )
                        y = (
                            self.top_rest
                            - self.abergement_top
                            + M * (self.panel_width + self.vertical_pose)
                        )
                        self.abergement.append(
                            [x, y, abergement_length, self.abergement_top,]
                        )
                        B += 1
                    if i == 0:
                        x = self.left_rest - self.abergement_left
                        y = self.top_rest + M * (self.panel_width + self.vertical_pose)
                        abergement_height = self.panel_width + self.vertical_pose
                        if i1 == self.nb_panel_width - 1:
                            abergement_height = self.panel_width
                        self.abergement.append(
                            [x, y, self.abergement_left, abergement_height,]
                        )
                        C += 1
                    if i == (self.nb_panel_length - 1):
                        x = (
                            self.left_rest
                            + N * (self.panel_length + self.horizontal_pose)
                            + self.panel_length
                        )
                        y = self.top_rest + M * (self.panel_width + self.vertical_pose)
                        abergement_height = self.panel_width + self.vertical_pose
                        if i1 == self.nb_panel_width - 1:
                            abergement_height = self.panel_width
                        self.abergement.append(
                            [x, y, self.abergement_right, abergement_height,]
                        )
                        D += 1

                    self.panel.append(
                        [
                            self.left_rest
                            + N * (self.panel_length + self.horizontal_pose),
                            self.top_rest + M * (self.panel_width + self.vertical_pose),
                            self.panel_length,
                            self.panel_width,
                        ]
                    )
                    M += 1
                M = 0
                N += 1
        # endregion

        region toit 2 & 3
        if roof.roof_type_id_id == 2 or roof.roof_type_id_id == 3:
            for i in range(
                0,
                self.nb_panel_length
                + self.nb_pan_lentgh_right_triangle
                + self.nb_pan_lentgh_left_triangle,
            ):
                if i < self.nb_pan_lentgh_left_triangle:
                    j[i] = self.panel_left_triangle[i + 1]
                if i >= self.nb_pan_lentgh_left_triangle:
                    j[i] = self.nb_panel_width
                if i >= (self.nb_pan_lentgh_left_triangle + self.nb_panel_length):
                    j[i] = self.panel_right_triangle[
                        i - self.nb_pan_lentgh_left_triangle - self.nb_panel_length + 1
                    ]

                for i1 in range(0, j[i]):
                    if i1 == 0:
                        aberbasx.Add(
                            self.centering
                            + N * (self.panel_length + self.horizontal_pose)
                        )
                        aberbasy.Add(self.bottom_rest)
                        if i == 0:
                            abergauchex.Add(self.centering - self.abergement_left)
                            abergauchey.Add(self.bottom_rest + self.panel_width)
                            C += 1

                        A += 1

                    if i > 0 and i < self.nb_pan_lentgh_left_triangle:
                        if i1 >= j[i - 1]:
                            abergauchex.Add(
                                self.centering
                                + N * (self.panel_length + self.horizontal_pose)
                                - self.abergement_left
                            )
                            abergauchey.Add(
                                self.panel_width
                                + self.bottom_rest
                                + M * (self.panel_width + self.vertical_pose)
                            )
                            C += 1

                    if i == 0:
                        if i1 > 0:
                            abergauchex.Add(self.centering - self.abergement_left)
                            abergauchey.Add(
                                self.panel_width
                                + self.bottom_rest
                                + M * (self.panel_width + self.vertical_pose)
                            )
                            C += 1

                    if (
                        i == self.nb_pan_lentgh_left_triangle
                        and self.nb_pan_lentgh_left_triangle != 0
                    ):
                        if i1 >= j[self.nb_pan_lentgh_left_triangle - 1]:
                            abergauchex.Add(
                                self.centering
                                + N * (self.panel_length + self.horizontal_pose)
                                - self.abergement_left
                            )
                            abergauchey.Add(
                                self.panel_width
                                + self.bottom_rest
                                + M * (self.panel_width + self.vertical_pose)
                            )
                            C += 1

                    if i1 == (j[i] - 1):
                        if i >= self.nb_pan_lentgh_left_triangle + self.nb_panel_length:
                            aberhautx.Add(
                                self.centering
                                + (N - 1) * (self.panel_length + self.horizontal_pose)
                                + self.panel_length
                            )
                            aberhauty.Add(
                                self.panel_width
                                + self.bottom_rest
                                + M * (self.panel_width + self.vertical_pose)
                                + self.abergement_top
                            )
                        else:
                            aberhautx.Add(
                                self.centering
                                - self.abergement_left
                                + N * (self.panel_length + self.horizontal_pose)
                            )
                            aberhauty.Add(
                                self.panel_width
                                + self.bottom_rest
                                + M * (self.panel_width + self.vertical_pose)
                                + self.abergement_top
                            )

                        B += 1

                    if (
                        i - self.nb_pan_lentgh_left_triangle - self.nb_panel_length + 1
                    ) >= 0:
                        if i1 >= (
                            self.panel_right_triangle[
                                i
                                - self.nb_pan_lentgh_left_triangle
                                - self.nb_panel_length
                                + 2
                            ]
                        ):
                            if (
                                i
                                >= self.nb_pan_lentgh_left_triangle
                                + self.nb_panel_length
                                - 1
                            ):
                                aberdroitx.Add(
                                    self.centering
                                    + N * (self.panel_length + self.horizontal_pose)
                                    + self.panel_length
                                )
                                aberdroity.Add(
                                    self.panel_width
                                    + self.bottom_rest
                                    + M * (self.panel_width + self.vertical_pose)
                                )
                                D += 1

                    self.panel
                    NewPan["Coordg"] = self.centering + N * (
                        self.panel_length + self.horizontal_pose
                    )
                    NewPan["Coordd"] = (
                        self.centering
                        + N * (self.panel_length + self.horizontal_pose)
                        + self.panel_length
                    )
                    NewPan["Coordh"] = (
                        self.panel_width
                        + self.bottom_rest
                        + M * (self.panel_width + self.vertical_pose)
                        + self.panel_width
                    )
                    NewPan["Coordb"] = (
                        self.panel_width
                        + self.bottom_rest
                        + M * (self.panel_width + self.vertical_pose)
                    )

                    M = M + 1
                M = 0
                N = N + 1
        endregion
