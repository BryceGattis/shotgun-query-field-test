import shotgun_query_field_test.shotgun
import shotgun_api3


def test_sg_instance_created():
    sg = shotgun_query_field_test.shotgun.get_shotgun_instance()
    assert isinstance(sg, shotgun_api3.Shotgun)


def test_get_query_field_value_average():
    # This test is volatile since it's referencing a real DB whose values can change at any time.
    qf_value = shotgun_query_field_test.shotgun.get_query_field_value('Sequence', 'sg_cut_duration', 40)
    assert qf_value == 17


def test_get_query_field_value_record_count():
    # This test is volatile since it's referencing a real DB whose values can change at any time.
    qf_value = shotgun_query_field_test.shotgun.get_query_field_value('Sequence', 'sg_ip_versions', 40)
    assert qf_value == 11

