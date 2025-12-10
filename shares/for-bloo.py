FEET_TO_MILES_RATIO = 5280


def miles_to_feet(x):
    return FEET_TO_MILES_RATIO * x


class RectangularArea:

    def __init__(self, length, width):
        self.length = length
        self.width = width

    @property
    def area(self):
        return self.length * self.width

    def wall_area(self, thickness=0):
        """
        Given the thickness of a wall enclosing this area,
        with the outer surface of the wall situated
        at the boundary of the area,
        calculate what area of the ground its foundation would occupy
        """

        #
        # the "inner area" here is the area
        # that is actually enclosed by the wall
        # it is doubled,
        # since the wall encroaches on both sides, like so:
        #
        # -----------------
        # -----------------
        # | |           | |
        # | |inner area | |
        # | |           | |
        # | |           | |
        # -----------------
        # -----------------
        #
        inner_rectangle_length = self.length - (2 * thickness)
        inner_rectangle_width = self.width - (2 * thickness)
        inner_rectangle_area = RectangularArea(
            length=inner_rectangle_length, width=inner_rectangle_width
        )

        # the footprint of the wall as it covers the ground, not including the height
        return self.area - inner_rectangle_area.area


class RectangularVolume:

    def __init__(self, length, width, height):
        self.length = length
        self.width = width
        self.height = height

    @property
    def volume(self):
        return self.length * self.width * self.height


def calculate_wall_volume(length=0, width=0, height=0, wall_thickness=0):
    assumed_structure_area = RectangularArea(length, width)
    return height * assumed_structure_area.wall_area(thickness=wall_thickness)


def calculate_solution(
    structure_length=0,
    structure_width=0,
    structure_height=0,
    wall_thickness=0,
    material_recovery_rate=0,
    excavation_length=0,
    excavation_width=0,
    excavation_depth=0,
):

    structure_length = miles_to_feet(1928)
    structure_width = miles_to_feet(1928)
    structure_height = 700
    assumed_wall_thickness = 300

    assumed_recovery_rate = 0.3

    spec = {
        "length": structure_length,
        "width": structure_width,
        "height": structure_height,
        "wall_thickness": wall_thickness,
    }

    wall_volume = calculate_wall_volume(**spec)

    assumed_excavation_volume = RectangularVolume(
        excavation_length, excavation_width, excavation_depth
    )

    return assumed_excavation_volume.volume * assumed_recovery_rate


def test__wall_area__correct():
    expected_wall_area = 16 - 4

    actual_wall_area = RectangularArea(4, 4).wall_area(thickness=1)

    assert expected_wall_area == actual_wall_area


if __name__ == "__main__":
    test__wall_area__correct()

    scenario_spec = {
        "structure_length": miles_to_feet(1928),
        "structure_width": miles_to_feet(1928),
        "structure_height": 700,
        "wall_thickness": 300,
        "excavation_length": miles_to_feet(5525),
        "excavation_width": miles_to_feet(1),
        "excavation_depth": miles_to_feet(0.5),
        "material_recovery_rate": 0.3,
    }

    concrete_needed_cubic_feet = calculate_solution(**scenario_spec)

    formatted_output = "{:,}".format(int(concrete_needed_cubic_feet))
    print(
        f"Bloo's structure would contain {formatted_output} cubic feet of concrete, given the assumptions"
    )
